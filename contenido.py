"""Contenido editable desde el panel, sin tocar código ni desplegar.

MISMA IDEA QUE EN GUARDIAN, PERO CON POSTGRES
El bot pide un texto y se mira en dos sitios, por orden:
  1. ¿Hay una versión editada en la base de datos?  -> esa
  2. Si no                                          -> la del código

Qué es editable aquí: las 30 lecciones, los 90 términos del diccionario, el
quiz y las citas. Las claves llevan su origen dentro:

    edu.edu_a1.btn · edu.edu_a1.texto
    dic.t_gen_bitcoin.btn · dic.t_gen_bitcoin.texto
    quiz.3.q · cita.7

LA CARGA ES SÍNCRONA A PROPÓSITO
El bot pide textos en sitios donde no puede esperar (dentro de bucles que
construyen menús). Se refresca en segundo plano cada TTL y se lee de memoria,
así consultar un texto nunca bloquea.
"""
from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)

TTL = 20.0
_cache: dict[str, str] = {}
_pool = None


def usar_pool(pool) -> None:
    """El bot pasa aquí su conexión al arrancar."""
    global _pool
    _pool = pool


def texto(clave: str, lang: str, original: str) -> str:
    """Versión editada, o el original si nadie la tocó. Lectura de memoria."""
    return _cache.get(f"{clave}|{lang}", original)


async def refrescar() -> None:
    """Relee los textos editados. Se llama sola desde el bucle de fondo."""
    global _cache
    if _pool is None:
        return
    try:
        async with _pool.acquire() as c:
            filas = await c.fetch("SELECT clave, lang, texto FROM contenido")
        _cache = {f"{f['clave']}|{f['lang']}": f["texto"] for f in filas}
    except Exception:
        pass    # la tabla puede no existir aún; se siguen usando los textos del código


async def bucle() -> None:
    """Comprueba cada TTL si el panel publicó algo nuevo."""
    while True:
        await refrescar()
        await asyncio.sleep(TTL)


async def crear_tabla(pool) -> None:
    """La crea el bot al arrancar, para que el panel tenga dónde escribir."""
    async with pool.acquire() as c:
        await c.execute("""
            CREATE TABLE IF NOT EXISTS contenido (
                clave       TEXT,
                lang        TEXT,
                texto       TEXT,
                editado_en  TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (clave, lang)
            )
        """)


# ─── Atajos por tipo de contenido ────────────────────────────────────────────
def leccion_btn(mid: str, lang: str, original: str) -> str:
    return texto(f"edu.{mid}.btn", lang, original)


def leccion(mid: str, lang: str, original: str) -> str:
    return texto(f"edu.{mid}.texto", lang, original)


def termino_btn(tid: str, lang: str, original: str) -> str:
    return texto(f"dic.{tid}.btn", lang, original)


def termino(tid: str, lang: str, original: str) -> str:
    return texto(f"dic.{tid}.texto", lang, original)
