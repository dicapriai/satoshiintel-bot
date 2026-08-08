"""Límite de consultas caras — protege el bot de sus propios usuarios.

DOS PROBLEMAS DISTINTOS, DOS DEFENSAS

1. Una persona acapara el bot.
   python-telegram-bot atiende las actualizaciones de una en una, y una consulta
   al nodo puede tardar hasta 12 s (el tope para direcciones enormes). Alguien
   pegando direcciones sin parar deja al bot mudo para todos los demás. Se
   resuelve con `permitido()`: cada usuario tiene su propio cupo.

2. Entre todos ahogan el nodo.
   Aunque cada uno respete su cupo, veinte a la vez saturan el índice. Se
   resuelve con `nodo`: como mucho N consultas simultáneas, el resto espera en
   cola ordenada en vez de avalanzarse.

QUÉ SE LIMITA Y QUÉ NO
Solo lo caro: direcciones y transacciones. Los menús, la educación, el
diccionario y las citas no tocan el nodo y deben seguir siendo instantáneos —
quien navega por las lecciones no debería toparse nunca con esto.

POR USUARIO, NUNCA GLOBAL
Un límite global se lo comerían los bucles de fondo del propio bot (alertas,
precio), que se bloquearían a sí mismos. Cada quien con su cupo.

Todo vive en memoria: si el bot se reinicia, todos empiezan de cero y no pasa
nada. No merece una tabla en la base de datos.
"""
from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque

# Cupo por persona. 10 por minuto es invisible para quien explora de verdad
# (tres o cuatro consultas) y frena en seco a quien machaca el bot.
MAX_POR_VENTANA = 10
VENTANA = 60.0  # segundos

# Consultas simultáneas al nodo, sumando TODOS los usuarios. Electrs responde en
# 0,06 s, así que 4 en paralelo van sobradas; más solo sirve para atascarlo.
MAX_SIMULTANEAS = 4

_historial: dict[int, deque] = defaultdict(deque)

# El semáforo se crea al primer uso: si se creara al importar, quedaría atado a
# un bucle de eventos que quizá aún no existe.
_semaforo: asyncio.Semaphore | None = None


def permitido(user_id: int, ahora: float | None = None) -> tuple[bool, int]:
    """¿Puede este usuario hacer otra consulta cara?

    Devuelve (permitido, segundos_para_reintentar). Cuando se permite, la
    consulta queda anotada: llamar a esta función consume cupo, así que se llama
    UNA vez por consulta, justo antes de hacerla.
    """
    t = time.monotonic() if ahora is None else ahora
    q = _historial[user_id]
    while q and t - q[0] >= VENTANA:   # fuera las que ya no cuentan
        q.popleft()
    if len(q) >= MAX_POR_VENTANA:
        espera = VENTANA - (t - q[0])
        return False, max(1, int(espera) + 1)
    q.append(t)
    return True, 0


def aviso(lang: str, segundos: int) -> str:
    """Lo que ve quien se pasa de cupo.

    Ni silencio ni "error": eso parece que el bot está roto. Se le dice qué pasa
    y cuándo volver, sin regañar a nadie.
    """
    if lang == "es":
        return (f"⏳ *Vas muy rápido.*\n\n"
                f"Espera {segundos} segundos y vuelve a intentarlo.\n\n"
                f"_Es para que el bot siga rápido para todos._")
    return (f"⏳ *You're going too fast.*\n\n"
            f"Wait {segundos} seconds and try again.\n\n"
            f"_This keeps the bot fast for everyone._")


def nodo() -> asyncio.Semaphore:
    """Tope de consultas simultáneas al nodo. Uso:

        async with ratelimit.nodo():
            ...consulta...
    """
    global _semaforo
    if _semaforo is None:
        _semaforo = asyncio.Semaphore(MAX_SIMULTANEAS)
    return _semaforo


def _reset() -> None:
    """Solo para los tests."""
    _historial.clear()
    global _semaforo
    _semaforo = None
