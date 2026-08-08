"""Cliente directo a Electrs (protocolo Electrum) — se salta Mempool.

POR QUÉ EXISTE
Mempool hacía de traductor entre el bot y Electrs, y ese eslabón se rompe bajo
carga: aguanta unos minutos y luego deja de responder a direcciones y ya no
reconecta (medido el 2026-08-06: 24/24 en reposo, 0/20 con el bot trabajando).
Electrs, en cambio, responde en 0,06 s y nunca falló. Así que hablamos con él.

CÓMO ENCAJA SIN REESCRIBIR EL BOT
`NodeHTTP` imita a `httpx.AsyncClient`: tiene `.get(url)` y devuelve algo con
`.json()` y `.text`. Las rutas de direcciones y transacciones las resuelve por
Electrum; cualquier otra URL (precio, fees, listas) sale por httpx como siempre.
Así los módulos que ya existen no cambian una línea de su lógica.

LO QUE DEVUELVE
Reproduce la forma de la API de mempool/esplora, que es la que el bot ya sabe
leer: `chain_stats`, `mempool_stats`, `vin[].prevout`, `vout[]`, `status`.

Identidad útil que ahorra trabajo: *total enviado = total recibido − saldo*.
Por eso solo hay que sumar las salidas hacia la dirección, no resolver todas
sus entradas gastadas.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os

# El .env se carga aquí también, para que este módulo funcione se importe en el
# orden que se importe (incluido suelto, desde un test).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# Direcciones que ya tumbaron el índice: no se vuelven a pedir al nodo mientras
# viva el proceso. Se aprende del golpe una sola vez.
_DEMASIADO_GRANDES: set[str] = set()

# Megadirecciones famosas, las que la gente pega "a ver qué sale". Tienen
# decenas de miles de transacciones y atascarían el índice del nodo durante
# minutos, tumbando de paso las consultas de TODOS los usuarios. Van por la API
# pública: son entidades públicas y de sobra conocidas, no wallets de nadie.
# Esta lista es la primera barrera; _DEMASIADO_GRANDES aprende de las que falten.
GIGANTES_CONOCIDAS = {
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",   # Satoshi, bloque génesis
    "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo",   # Binance (cold)
    "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97",  # Bitfinex
    "bc1ql49ydapnjafl5t2cp9zqpjwe6pdgmxy98859v2",  # Robinhood
    "bc1qa5wkgaew2dkv56kfvj49j0av5nml45x9ek9hz6",  # Gobierno EE.UU. (Silk Road)
    "3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6",   # Binance (hot)
    "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ",   # Bitfinex (antigua)
    "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h",  # Kraken
    "3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb",   # Binance
    "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF",   # ballena histórica
}

# ⚠️ ESTE REPO ES PÚBLICO: aquí NO va ningún dato de la infraestructura real.
# El servidor se configura por variables de entorno, que viven solo en el .env
# del servidor (y el .env está en .gitignore). Sin ELECTRS_HOST no hay nodo y
# el bot usa la API pública, que es justo lo que debe hacer quien clone el repo.
def _destino() -> tuple[str, int]:
    """Servidor Electrs, leído EN EL MOMENTO DE CONECTAR, no al importar.

    Leerlo al importar reintroduce el bug de orden de carga: si este módulo se
    importa antes de que el .env esté cargado, el host queda vacío y la conexión
    se va a localhost sin avisar. Leerlo aquí lo hace inmune a ese orden.
    """
    host = os.getenv("ELECTRS_HOST", "").strip()
    if not host:
        raise RuntimeError("ELECTRS_HOST no configurado: no hay nodo al que conectarse")
    return host, int(os.getenv("ELECTRS_PORT", "50001"))  # 50001 = puerto Electrum

POOL = 4          # conexiones en paralelo: Electrs va a 0,06 s, 4 bastan de sobra
TX_PAGE = 25      # transacciones por página, igual que esplora
MAX_SUM_TX = 200  # tope al sumar el histórico: por encima el análisis no aporta
MAX_VIN = 100     # entradas a resolver por tx (ver _esplora_tx: las hay con miles)
HIST_TIMEOUT = 12  # corte para historiales gigantes (ver _historial)
MAX_LINEA = 32 * 1024 * 1024  # una respuesta puede ser enorme (tx con cientos de entradas)


# ─── Dirección -> scripthash (lo que entiende el protocolo Electrum) ──────────
def script_pubkey(addr: str) -> bytes:
    """scriptPubKey de una dirección Bitcoin. ValueError si no es válida."""
    import addr_utils
    from bip_utils import P2PKHAddrDecoder, P2SHAddrDecoder
    a = addr.strip()
    if a[:1] == "1":
        h = P2PKHAddrDecoder.DecodeAddr(a, net_ver=b"\x00")
        return b"\x76\xa9\x14" + h + b"\x88\xac"
    if a[:1] == "3":
        h = P2SHAddrDecoder.DecodeAddr(a, net_ver=b"\x05")
        return b"\xa9\x14" + h + b"\x87"
    if a.lower().startswith("bc1"):
        witver, prog = addr_utils._decode_segwit("bc", a)
        prog = bytes(prog)
        op = b"\x00" if witver == 0 else bytes([0x50 + witver])
        return op + bytes([len(prog)]) + prog
    raise ValueError("dirección no reconocida")


def scripthash(addr: str) -> str:
    """sha256(scriptPubKey) invertido, en hex — la clave que usa Electrum."""
    return hashlib.sha256(script_pubkey(addr)).digest()[::-1].hex()


# ─── Conexión ────────────────────────────────────────────────────────────────
class _Conn:
    """Una conexión TCP a Electrs. Serializa sus peticiones con un cerrojo."""

    def __init__(self, timeout: float):
        self.timeout = timeout
        self._r = self._w = None
        self._lock = asyncio.Lock()
        self._id = 0

    async def _ensure(self):
        if self._w is None or self._w.is_closing():
            # limit= es imprescindible: readline() de asyncio corta a 64 KB por
            # defecto y una transacción con muchas entradas pasa de eso, así que
            # reventaba justo en las transacciones que más importan.
            self._r, self._w = await asyncio.wait_for(
                asyncio.open_connection(*_destino(), limit=MAX_LINEA), timeout=self.timeout)

    async def call(self, method: str, params: list, timeout: float | None = None):
        tope = timeout or self.timeout
        async with self._lock:
            for intento in (1, 2):   # una reconexión silenciosa si la conexión murió
                try:
                    await self._ensure()
                    self._id += 1
                    req = json.dumps({"jsonrpc": "2.0", "id": self._id,
                                      "method": method, "params": params}) + "\n"
                    self._w.write(req.encode())
                    await self._w.drain()
                    linea = await asyncio.wait_for(self._r.readline(), timeout=tope)
                    if not linea:
                        raise ConnectionError("Electrs cerró la conexión")
                    resp = json.loads(linea)
                    if "error" in resp and resp["error"]:
                        raise RuntimeError(f"Electrs: {resp['error']}")
                    return resp.get("result")
                except (asyncio.TimeoutError, TimeoutError):
                    # CRÍTICO: al agotarse el tiempo la respuesta sigue de camino.
                    # Si dejáramos la conexión abierta, la siguiente petición leería
                    # esa respuesta atrasada y todo quedaría desfasado un turno: un
                    # solo timeout envenenaría la conexión para siempre. Se cierra.
                    await self.close()
                    raise
                except (ConnectionError, asyncio.IncompleteReadError, json.JSONDecodeError, ValueError):
                    await self.close()
                    if intento == 2:
                        raise

    async def close(self):
        if self._w is not None:
            try:
                self._w.close()
            except Exception:
                pass
            self._r = self._w = None


class Pool:
    """Varias conexiones para poder pedir en paralelo sin pisarse."""

    def __init__(self, timeout: float, size: int = POOL):
        self._conns = [_Conn(timeout) for _ in range(size)]
        self._free: asyncio.Queue = asyncio.Queue()
        for c in self._conns:
            self._free.put_nowait(c)

    async def call(self, method: str, params: list, timeout: float | None = None):
        c = await self._free.get()
        try:
            return await c.call(method, params, timeout)
        finally:
            self._free.put_nowait(c)

    async def close(self):
        await asyncio.gather(*(c.close() for c in self._conns), return_exceptions=True)



# ─── Piscina compartida por todo el proceso ──────────────────────────────────
# Mantener las conexiones abiertas entre consultas es lo que hace que el nodo
# responda tan rápido como una API pública: el saludo TCP se paga una vez, no
# en cada pregunta. Si una conexión muere, `_Conn.call` la rehace sola.
_POOL: "Pool | None" = None


def pool_compartido(timeout: float = 20) -> "Pool":
    global _POOL
    if _POOL is None:
        _POOL = Pool(timeout)
    return _POOL


# ─── Traducción a la forma de mempool/esplora ────────────────────────────────
def _btc_a_sats(v) -> int:
    return int(round(float(v) * 100_000_000))


class Node:
    """Consultas de alto nivel, ya con la forma que el bot espera leer."""

    def __init__(self, timeout: float = 20, pool: "Pool | None" = None):
        # Las CONEXIONES se comparten entre consultas (ahorra el saludo TCP cada
        # vez, ~0,15 s). Las CACHÉS no: son de esta consulta y mueren con ella,
        # o el bot acabaría enseñando saldos viejos.
        self._propia = pool is None
        self.pool = pool if pool is not None else Pool(timeout)
        self._tx_cache: dict[str, dict] = {}
        self._hist_cache: dict[str, list] = {}

    async def close(self):
        # Solo se cierra la piscina si es nuestra. La compartida sigue viva
        # para la siguiente consulta.
        if self._propia:
            await self.pool.close()

    async def tip_height(self) -> int:
        r = await self.pool.call("blockchain.headers.subscribe", [])
        return int(r["height"])

    async def raw_tx(self, txid: str) -> dict:
        """Transacción descodificada por bitcoind (cacheada por instancia)."""
        if txid in self._tx_cache:
            return self._tx_cache[txid]
        tx = await self.pool.call("blockchain.transaction.get", [txid, True])
        self._tx_cache[txid] = tx
        return tx

    async def _historial(self, addr: str) -> list[dict]:
        """Historial de una dirección, cacheado por instancia.

        El protocolo Electrum NO pagina: pide el historial entero o nada. Para
        una dirección normal son milisegundos, pero las megadirecciones (Satoshi,
        wallets frías de exchange, decenas de miles de tx) no llegan ni en dos
        minutos. Por eso se corta pronto: mejor un "no disponible" en 12 s que
        un usuario mirando una rueda girar.
        """
        if addr in self._hist_cache:
            return self._hist_cache[addr]
        sh = scripthash(addr)
        try:
            hist = await self.pool.call(
                "blockchain.scripthash.get_history", [sh], timeout=HIST_TIMEOUT) or []
        except (asyncio.TimeoutError, TimeoutError):
            # Recordarla: pedirla otra vez volvería a atascar el índice para TODOS
            # los usuarios durante minutos. Una vez basta para aprender.
            _DEMASIADO_GRANDES.add(addr)
            raise TimeoutError(
                "dirección demasiado grande para el índice del nodo "
                "(el protocolo Electrum no pagina el historial)") from None
        self._hist_cache[addr] = hist
        return hist

    async def _salidas_hacia(self, txid: str, addr: str) -> int:
        """Sats que esta tx pagó a la dirección."""
        tx = await self.raw_tx(txid)
        total = 0
        for o in tx.get("vout", []):
            spk = o.get("scriptPubKey") or {}
            if spk.get("address") == addr or addr in (spk.get("addresses") or []):
                total += _btc_a_sats(o.get("value", 0))
        return total

    async def address_stats(self, addr: str) -> dict:
        """Equivalente a GET /address/{addr} de mempool."""
        sh = scripthash(addr)
        bal, hist = await asyncio.gather(
            self.pool.call("blockchain.scripthash.get_balance", [sh]),
            self._historial(addr),
        )
        confirmadas = [h for h in hist if (h.get("height") or 0) > 0]
        pendientes = [h for h in hist if (h.get("height") or 0) <= 0]
        saldo_conf = int(bal.get("confirmed", 0))
        saldo_mp = int(bal.get("unconfirmed", 0))

        # Total recibido: sumar las salidas hacia la dirección. Total enviado sale
        # solo, por identidad: enviado = recibido − saldo. Así nos ahorramos
        # resolver todas las entradas gastadas, que sería mucho más caro.
        recibido = 0
        if len(confirmadas) <= MAX_SUM_TX:
            sumas = await asyncio.gather(
                *(self._salidas_hacia(h["tx_hash"], addr) for h in confirmadas),
                return_exceptions=True)
            # Si UNA sola suma falla, el total queda por debajo del real y el bot
            # enseñaría un saldo falso. Preferimos romper y decir "no disponible".
            fallos = [s for s in sumas if isinstance(s, BaseException)]
            if fallos:
                raise fallos[0]
            recibido = sum(sumas)
            enviado = max(0, recibido - saldo_conf)
        else:
            # Demasiadas transacciones para sumarlas sin castigar al nodo.
            # El saldo sigue siendo exacto; recibido/enviado se dejan al mínimo
            # coherente en vez de inventar una cifra.
            recibido, enviado = saldo_conf, 0

        return {
            "address": addr,
            "chain_stats": {
                "funded_txo_sum": recibido,
                "spent_txo_sum": enviado,
                "tx_count": len(confirmadas),
                "funded_txo_count": 0,
                "spent_txo_count": 0,
            },
            "mempool_stats": {
                "funded_txo_sum": max(0, saldo_mp),
                "spent_txo_sum": max(0, -saldo_mp),
                "tx_count": len(pendientes),
                "funded_txo_count": 0,
                "spent_txo_count": 0,
            },
        }

    async def _esplora_tx(self, txid: str, tip: int) -> dict:
        """Transacción con la forma de esplora: vin[].prevout y vout[] resueltos."""
        tx = await self.raw_tx(txid)

        async def prevout(vin):
            if "txid" not in vin:            # coinbase
                return None
            try:
                padre = await self.raw_tx(vin["txid"])
                o = padre["vout"][vin["vout"]]
                spk = o.get("scriptPubKey") or {}
                return {"scriptpubkey_address": spk.get("address"),
                        "value": _btc_a_sats(o.get("value", 0))}
            except Exception:
                return None

        # Tope de entradas a resolver. Una consolidación puede tener MILES (la del
        # robo tiene 1.212) y cada una obliga a traer su transacción padre entera.
        # Lo que se pierde al recortar es solo el detalle de esta tx concreta; el
        # saldo, el total recibido y el nº de transacciones de la dirección salen
        # de otro camino (get_balance/get_history) y siguen siendo EXACTOS.
        vins = tx.get("vin", [])[:MAX_VIN]
        prevs = await asyncio.gather(*(prevout(v) for v in vins),
                                     return_exceptions=True)
        vin = [{"prevout": p} for p in prevs if isinstance(p, dict)]
        vout = [{"scriptpubkey_address": (o.get("scriptPubKey") or {}).get("address"),
                 "value": _btc_a_sats(o.get("value", 0))} for o in tx.get("vout", [])]

        confs = int(tx.get("confirmations") or 0)
        altura = (tip - confs + 1) if confs > 0 else None
        entradas = sum(v["prevout"]["value"] for v in vin)
        salidas = sum(o["value"] for o in vout)
        return {
            "txid": txid,
            "vin": vin,
            "vout": vout,
            "fee": max(0, entradas - salidas) if vin else 0,
            "status": {"confirmed": confs > 0, "block_height": altura,
                       "block_time": tx.get("blocktime")},
        }

    async def address_txs(self, addr: str) -> list[dict]:
        """Equivalente a GET /address/{addr}/txs (las TX_PAGE más recientes)."""
        hist = await self._historial(addr)
        # get_history llega en orden ascendente; el bot espera las últimas primero.
        # Las pendientes (height <= 0) van arriba del todo.
        pend = [h for h in hist if (h.get("height") or 0) <= 0]
        conf = [h for h in hist if (h.get("height") or 0) > 0]
        ordenadas = pend + list(reversed(conf))
        elegidas = ordenadas[:TX_PAGE]
        tip = await self.tip_height()
        txs = await asyncio.gather(
            *(self._esplora_tx(h["tx_hash"], tip) for h in elegidas),
            return_exceptions=True)
        return [t for t in txs if isinstance(t, dict)]

    async def tx(self, txid: str) -> dict:
        tip = await self.tip_height()
        return await self._esplora_tx(txid, tip)


# ─── Fachada que imita a httpx.AsyncClient ───────────────────────────────────
class _Resp:
    """Respuesta mínima: lo que usan los módulos es .json(), .text y raise_for_status()."""

    def __init__(self, data, texto: str | None = None, status: int = 200):
        self._data = data
        self.text = texto if texto is not None else json.dumps(data)
        self.status_code = status

    def json(self):
        return self._data

    def raise_for_status(self):
        return None


class NodeHTTP:
    """Se usa igual que httpx.AsyncClient, pero las consultas de direcciones y
    transacciones las resuelve Electrs. El resto de URLs siguen saliendo por HTTP."""

    def __init__(self, timeout: float = 20):
        self.timeout = timeout
        self.node = Node(timeout, pool=pool_compartido(timeout))
        self._http = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    async def aclose(self):
        await self.node.close()
        if self._http is not None:
            await self._http.aclose()

    async def _fuera(self, url, **kw):
        """URL que no es del nodo (precio, fees, listas): httpx normal."""
        import httpx
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=self.timeout)
        return await self._http.get(url, **kw)

    # Categorías de ballena que SIEMPRE son megadirecciones. Consultarlas contra
    # el índice del nodo lo deja atascado minutos y tumba a todos los usuarios de
    # paso: fue justo lo que hizo fracasar la primera migración.
    # Las de categoría 'hack' NO entran aquí: suelen ser recientes y pequeñas
    # (las 7 del robo tienen 45 tx), así que el nodo las sirve de sobra.
    _CATEGORIAS_ENORMES = {"exchange", "gobierno", "icono", "minero"}

    @classmethod
    def _es_entidad_publica(cls, addr: str) -> bool:
        """¿Es una entidad pública gigante que conviene NO pedirle al nodo?

        No rompe la privacidad: son entidades curadas por el admin (Binance, el
        Gobierno de EE.UU., Satoshi), no wallets de usuarios. La regla de "sin
        fallback" existe para proteger a la gente, no a un exchange.
        """
        if addr in GIGANTES_CONOCIDAS:
            return True
        try:  # en Guardian existe la tabla de ballenas; en el bot gratis no
            import db
            wh = db.whale_by_address(addr)
            return bool(wh) and (wh["category"] in cls._CATEGORIAS_ENORMES)
        except Exception:
            return False

    async def get(self, url: str, **kw):
        ruta = url.split("/api", 1)[1] if "/api" in url else ""
        partes = [p for p in ruta.split("/") if p]

        if partes[:1] == ["address"] and len(partes) >= 2:
            addr = partes[1]
            if addr in _DEMASIADO_GRANDES:
                # Ya nos tumbó el índice una vez: no se vuelve a intentar. Y NO se
                # cae a la API pública, que filtraría la dirección de un usuario.
                raise TimeoutError("dirección demasiado grande para el índice del nodo")
            if self._es_entidad_publica(addr):
                import sources
                # Se reconstruye la URL desde la ruta en vez de sustituir texto:
                # así funciona venga como venga escrita la base.
                return await self._fuera(f"{sources.API_PUBLICA}{ruta}", **kw)
        try:
            if partes[:1] == ["address"] and len(partes) == 2:
                try:
                    return _Resp(await self.node.address_stats(partes[1]))
                except ValueError:
                    # Dirección mal escrita: se devuelve 400 como haría la API REST,
                    # para que el bot enseñe "dirección no válida" y no "error de red".
                    return _Resp({"error": "dirección no válida"}, status=400)
            if partes[:1] == ["address"] and partes[2:3] == ["txs"]:
                return _Resp(await self.node.address_txs(partes[1]))
            if partes[:1] == ["tx"] and len(partes) == 2:
                return _Resp(await self.node.tx(partes[1]))
            if partes[:3] == ["blocks", "tip", "height"]:
                h = await self.node.tip_height()
                return _Resp(h, str(h))
        except Exception as e:
            logger.warning("electrs %s: %s", partes[:1], e)
            raise
        return await self._fuera(url, **kw)
