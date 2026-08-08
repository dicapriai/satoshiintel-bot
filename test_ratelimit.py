"""Self-check del límite de consultas. Corre: .venv/bin/python test_ratelimit.py

Comprueba lo que de verdad importa: que frena al que abusa, que NO molesta al
que usa el bot con normalidad, y que un usuario no puede gastar el cupo de otro.
"""
import asyncio

import ratelimit


def demo() -> None:
    ratelimit._reset()
    ANA, BOB = 111, 222

    # ── Uso normal: nadie debería toparse nunca con esto ──
    # Alguien explorando hace 3-4 consultas seguidas.
    for i in range(4):
        ok, _ = ratelimit.permitido(ANA, ahora=100.0 + i)
        assert ok, f"el uso normal no puede bloquearse (consulta {i+1})"
    print("OK  uso normal (4 consultas): no molesta")

    # ── Abuso: al pasar del cupo, se corta ──
    ratelimit._reset()
    for i in range(ratelimit.MAX_POR_VENTANA):
        ok, _ = ratelimit.permitido(ANA, ahora=100.0)
        assert ok, f"las primeras {ratelimit.MAX_POR_VENTANA} deben pasar"
    ok, espera = ratelimit.permitido(ANA, ahora=100.0)
    assert not ok, "la que pasa del cupo debe frenarse"
    assert 1 <= espera <= ratelimit.VENTANA + 1, f"espera rara: {espera}"
    print(f"OK  abuso: la nº {ratelimit.MAX_POR_VENTANA + 1} se frena, avisa de {espera}s")

    # ── El cupo es POR PERSONA: Ana no puede dejar sin bot a Bob ──
    ok, _ = ratelimit.permitido(BOB, ahora=100.0)
    assert ok, "un usuario no puede consumir el cupo de otro"
    print("OK  aislamiento: el cupo de uno no afecta al de otro")

    # ── La ventana se abre sola al pasar el tiempo ──
    ok, _ = ratelimit.permitido(ANA, ahora=100.0 + ratelimit.VENTANA + 1)
    assert ok, "pasada la ventana debe volver a permitir"
    print("OK  recuperación: pasado el minuto, vuelve a dejar")

    # ── El aviso es claro, bilingüe y no parece un error ──
    for lg in ("es", "en"):
        t = ratelimit.aviso(lg, 12)
        assert "12" in t, "debe decir cuánto esperar"
        assert t.count("*") % 2 == 0, "asteriscos sin cerrar romperían el mensaje"
        assert "error" not in t.lower(), "no debe parecer que el bot está roto"
    print("OK  aviso: bilingüe, con la espera y sin parecer un fallo")

    # ── El tope de consultas simultáneas al nodo ──
    async def simultaneas():
        ratelimit._reset()
        sem = ratelimit.nodo()
        assert sem is ratelimit.nodo(), "debe ser el mismo semáforo siempre"
        a_la_vez = 0
        pico = 0

        async def consulta():
            nonlocal a_la_vez, pico
            async with ratelimit.nodo():
                a_la_vez += 1
                pico = max(pico, a_la_vez)
                await asyncio.sleep(0.05)
                a_la_vez -= 1

        await asyncio.gather(*(consulta() for _ in range(20)))
        assert pico <= ratelimit.MAX_SIMULTANEAS, \
            f"llegaron {pico} a la vez, el tope es {ratelimit.MAX_SIMULTANEAS}"
        return pico

    pico = asyncio.run(simultaneas())
    print(f"OK  nodo: 20 consultas a la vez -> nunca más de {pico} simultáneas")

    print("\nOK ✅ ratelimit: frena el abuso sin molestar al uso normal")


if __name__ == "__main__":
    demo()
