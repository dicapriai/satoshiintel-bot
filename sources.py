"""Fuente de datos on-chain — un solo interruptor para toda la app.

Sin `MEMPOOL_BASE` en el entorno usa la API pública (desarrollo en el Mac).
Con ella apunta a un nodo propio (se configura en el .env del servidor,
que nunca entra en el repositorio):

    MEMPOOL_BASE=http://TU-NODO:3006
    ELECTRS_HOST=TU-NODO

REGLA DE FALLBACK DIFERENCIADO — la parte importante de este archivo:

  • Datos PÚBLICOS y anónimos (comisiones, altura de bloque, mempool):
    si el nodo no responde, se puede caer a la API pública. Preguntar
    "¿a cuánto están las fees?" no revela nada de nadie.

  • Direcciones y transacciones: **SIN FALLBACK NUNCA**. Preferimos responder
    "no disponible ahora mismo" antes que filtrar en silencio la dirección de
    un usuario a un tercero. Un fallback silencioso aquí convertiría una caída
    del nodo en una fuga de privacidad que el usuario jamás vería.
"""
import os

# Se carga el .env AQUÍ, al importar, no en bot.py. Motivo: varios módulos leen
# os.environ en el momento de importarse, es decir ANTES de que bot.py llame a
# load_dotenv(). Cargarlo aquí evita esa clase de bug entera.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MEMPOOL_BASE = os.getenv("MEMPOOL_BASE", "https://mempool.space")
API = f"{MEMPOOL_BASE}/api"
FEES_URL = f"{API}/v1/fees/recommended"

# ¿Estamos sirviendo desde el nodo del usuario o desde la API pública?
USANDO_NODO_PROPIO = "mempool.space" not in MEMPOOL_BASE

# Respaldo público. SOLO para datos anónimos. Nunca para /address ni /tx.
API_PUBLICA = "https://mempool.space/api"

# Con nodo propio, las direcciones se consultan hablando Electrum DIRECTAMENTE
# con Electrs en vez de pasar por la API REST de Mempool. Motivo medido el
# 2026-08-06: Mempool pierde su conexión con Electrs bajo carga y no reconecta
# (0/20 consultas en 5 min con el bot trabajando), mientras que Electrs responde
# en 0,06 s sin fallar. Poner ELECTRS=0 en el entorno vuelve a la vía Mempool.
# Requiere ELECTRS_HOST explícito: si nadie lo configura (por ejemplo, alguien
# que clone este repo público), no se intenta hablar con ningún nodo y todo va
# por la API pública, como siempre.
USAR_ELECTRS = os.getenv("ELECTRS", "1") != "0" and bool(os.getenv("ELECTRS_HOST"))

# Timeout de cortesía: el nodo está en una casa, no en un centro de datos.
TIMEOUT = 12


def urls_publicas(path: str) -> list[str]:
    """URLs a probar en orden para un dato PÚBLICO (fees, altura, mempool).

    Contra el nodo propio devuelve [nodo, API pública]; en desarrollo, solo la
    pública. Usar únicamente con rutas que no contengan datos de un usuario.
    """
    if USANDO_NODO_PROPIO:
        return [f"{API}{path}", f"{API_PUBLICA}{path}"]
    return [f"{API}{path}"]


async def get_publico(client, path: str):
    """GET de un dato público con respaldo. None si fallan todas las fuentes."""
    for url in urls_publicas(path):
        try:
            r = await client.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            return r
        except Exception:
            continue
    return None


def cliente(timeout: float = 15):
    """Devuelve el cliente correcto para consultar la cadena.

    Con nodo propio -> habla Electrum DIRECTAMENTE con Electrs (`electrs.NodeHTTP`),
    saltándose Mempool, que se rompe bajo carga. Sin nodo -> `httpx` de siempre.

    Ambos se usan igual (`async with ... as c: await c.get(url)`), así que los
    módulos que consultan direcciones no cambian su lógica.
    """
    if USANDO_NODO_PROPIO and USAR_ELECTRS:
        import electrs
        return electrs.NodeHTTP(timeout)
    import httpx
    return httpx.AsyncClient(timeout=timeout)


def fuente(lang: str = "es") -> str:
    """De dónde salen los datos, para decírselo al usuario sin mentirle.

    Devuelve un complemento que encaja detrás de "Datos" / "Live data", para
    poder incrustarlo tal cual en los mensajes sin romper la frase.
    """
    if USANDO_NODO_PROPIO:
        return ("verificados por mi propio nodo Bitcoin" if lang == "es"
                else "verified by my own Bitcoin node")
    return "de mempool.space" if lang == "es" else "from mempool.space"
