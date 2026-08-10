"""Caché en disco de transacciones ya descargadas del nodo.

POR QUÉ EXISTE
Para decir cuánto ha recibido una dirección hay que sumar las salidas de TODAS
sus transacciones, y el protocolo Electrum obliga a pedirlas una a una. Una
dirección con 113 movimientos son 113 idas y vueltas: 5 segundos. mempool.space
lo tiene precalculado en su índice; un nodo doméstico no.

QUÉ SE GUARDA Y QUÉ NO — ESTO IMPORTA
Se guarda **la transacción, por su txid**. Una transacción es dato público de la
cadena: cualquiera la tiene. Lo que NO se guarda es qué dirección consultó nadie.

La tentación era cachear «dirección → total recibido», que sería más rápido y
más simple. Se descartó a propósito: esa tabla SERÍA un registro de lo que la
gente busca, exactamente lo que el bot promete no tener. La promesa de
privacidad no es una opción de configuración, es la razón de ser del producto.

POR QUÉ ES SEGURO CACHEAR PARA SIEMPRE
Una transacción confirmada no cambia nunca. Lo único que puede cambiar es si
sigue confirmada, y de eso ya se encarga el historial, que se pide siempre
fresco. Por eso solo se guardan las confirmadas.
"""
from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path

logger = logging.getLogger(__name__)

MAX_VOUT = 200          # una tx con más salidas ocupa mucho y se repite poco
MAX_FILAS = 200_000     # tope de la caché; al pasarse se tira lo más viejo
_conn: sqlite3.Connection | None = None


def _db() -> sqlite3.Connection | None:
    """La caché vive en su PROPIO archivo, separada de los datos de usuarios.

    Así se puede borrar entera sin tocar nada importante, y ninguna consulta a
    la base de usuarios puede tropezarse con ella por accidente.
    """
    global _conn
    if _conn is not None:
        return _conn
    import os
    ruta = os.getenv("TXCACHE_DB")
    if not ruta:
        base = os.getenv("GUARDIAN_DB")
        if not base:
            return None
        ruta = str(Path(base).with_name("txcache.db"))
    try:
        c = sqlite3.connect(ruta, check_same_thread=False)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("""CREATE TABLE IF NOT EXISTS txs (
                        txid   TEXT PRIMARY KEY,
                        salidas TEXT,      -- [[direccion, sats], ...]
                        visto  INTEGER
                     )""")
        c.commit()
        _conn = c
        return c
    except Exception as e:
        logger.warning("caché de transacciones no disponible: %s", e)
        return None


def salidas(txid: str) -> list | None:
    """Salidas guardadas de esta transacción, o None si no está."""
    c = _db()
    if c is None:
        return None
    try:
        fila = c.execute("SELECT salidas FROM txs WHERE txid = ?", (txid,)).fetchone()
        return json.loads(fila["salidas"]) if fila else None
    except Exception:
        return None


def guardar(txid: str, vout: list) -> None:
    """Guarda solo lo que hace falta para sumar: (dirección, sats) por salida."""
    c = _db()
    if c is None or len(vout) > MAX_VOUT:
        return
    datos = []
    for o in vout:
        spk = o.get("scriptPubKey") or {}
        addr = spk.get("address") or next(iter(spk.get("addresses") or []), None)
        if addr:
            datos.append([addr, int(round(float(o.get("value", 0)) * 1e8))])
    try:
        c.execute("INSERT OR REPLACE INTO txs (txid, salidas, visto) VALUES (?,?,?)",
                  (txid, json.dumps(datos), int(time.time())))
        c.commit()
    except Exception:
        pass


def recibido_por(txid: str, addr: str) -> int | None:
    """Sats que esa transacción pagó a esa dirección, si la tenemos guardada."""
    datos = salidas(txid)
    if datos is None:
        return None
    return sum(sats for a, sats in datos if a == addr)


def podar() -> int:
    """Tira lo más viejo si la caché se pasó de tamaño. Devuelve cuántas borró."""
    c = _db()
    if c is None:
        return 0
    try:
        total = c.execute("SELECT count(*) FROM txs").fetchone()[0]
        if total <= MAX_FILAS:
            return 0
        sobran = total - MAX_FILAS
        c.execute("DELETE FROM txs WHERE txid IN "
                  "(SELECT txid FROM txs ORDER BY visto ASC LIMIT ?)", (sobran,))
        c.commit()
        return sobran
    except Exception:
        return 0


def stats() -> dict:
    c = _db()
    if c is None:
        return {"disponible": False}
    try:
        return {"disponible": True,
                "transacciones": c.execute("SELECT count(*) FROM txs").fetchone()[0]}
    except Exception:
        return {"disponible": False}
