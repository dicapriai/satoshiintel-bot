"""Self-check de la migración al nodo propio (bot gratis).

Comprueba las tres cosas que importan:
  1. Las consultas de DIRECCIONES no salen nunca a un tercero cuando hay nodo.
  2. Los datos que devuelve el nodo son correctos.
  3. Los textos dicen la fuente REAL, sin mentirle al usuario.

Corre (con el .env del servidor cargado):  .venv/bin/python test_nodo.py
"""
import asyncio
import os

import sources

ADDR = "bc1qtfrwa4j6rmj9rsgspv6a0yjumkg39js2numu75"
TXID = "a52d7cac2ff46972eaeb19cece7985a6e261b664d8e4ef181bfdf21dd60d8049"


async def demo() -> None:
    con_nodo = sources.USANDO_NODO_PROPIO
    print(f"modo: {'NODO PROPIO' if con_nodo else 'API pública'}  ->  {sources.API}")

    # ── 1. Privacidad: con nodo, las direcciones no pueden salir fuera ──
    if con_nodo:
        assert "mempool.space" not in sources.API
        assert "blockstream" not in sources.API
        # Los datos públicos SÍ admiten respaldo; las direcciones no.
        assert len(sources.urls_publicas("/v1/fees/recommended")) == 2, "fees: con respaldo"
        print("OK  privacidad: direcciones al nodo, sin respaldo a terceros")

    # ── 2. Los textos dicen la verdad ──
    es, en = sources.fuente("es"), sources.fuente("en")
    if con_nodo:
        assert "mempool" not in es.lower() and "mempool" not in en.lower(), \
            "con nodo, los textos NO pueden seguir citando mempool.space"
        assert "nodo" in es.lower() and "node" in en.lower()
    else:
        assert "mempool.space" in es and "mempool.space" in en
    print(f'OK  textos: "Datos en vivo {es}." / "Live data {en}."')

    # ── 3. Los datos son correctos ──
    import bot
    txt = await bot.lookup_address(ADDR, "es")
    assert "45.9" in txt.replace(",", "."), f"saldo inesperado:\n{txt}"
    assert sources.fuente("es") in txt, "el mensaje debe declarar su fuente"
    print(f"OK  dirección: {txt.splitlines()[0][:60]}")

    txt = await bot.lookup_tx(TXID, "es")
    assert "vBytes" in txt, f"transacción no resuelta:\n{txt}"
    print(f"OK  transacción: {txt.splitlines()[0][:60]}")

    h = await bot.get_block_height()
    assert h and h > 900_000, f"altura rara: {h}"
    print(f"OK  altura de bloque: {h:,}")

    fees, count = await bot.get_mempool_data()
    assert fees and "halfHourFee" in fees
    print(f"OK  comisiones: {fees['halfHourFee']} sat/vB · mempool {count:,} tx")

    # ── 4. Dirección inválida: mensaje correcto, no "error de red" ──
    txt = await bot.lookup_address("no-soy-una-direccion", "es")
    assert "no válida" in txt.lower(), f"debería decir que no es válida:\n{txt}"
    print("OK  dirección inválida: mensaje correcto")

    print("\nOK ✅ bot gratis: migración al nodo verificada")


if __name__ == "__main__":
    if not os.getenv("MEMPOOL_BASE"):
        print("aviso: sin MEMPOOL_BASE -> probando el modo API pública\n")
    asyncio.run(demo())
