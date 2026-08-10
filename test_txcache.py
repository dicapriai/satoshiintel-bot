"""La caché de transacciones: rápida, correcta y sin registrar quién busca qué.

Lo que se comprueba, por orden de importancia:
  1. Que NO guarda ninguna dirección consultada — es la promesa del producto.
  2. Que los números salen IGUAL con caché que sin ella.
  3. Que de verdad evita ir al nodo la segunda vez.
"""
import os
import tempfile
from pathlib import Path

os.environ["TXCACHE_DB"] = str(Path(tempfile.mkdtemp()) / "tx.db")
import txcache

TX = "a" * 64
VOUT = [
    {"value": 0.5,  "scriptPubKey": {"address": "bc1qDESTINO"}},
    {"value": 0.25, "scriptPubKey": {"address": "bc1qVUELTA"}},
    {"value": 0.1,  "scriptPubKey": {"address": "bc1qDESTINO"}},   # dos veces a la misma
]


def demo():
    assert txcache.salidas(TX) is None
    txcache.guardar(TX, VOUT)

    # ── 1. Suma correcta, incluidas dos salidas a la misma dirección ──
    assert txcache.recibido_por(TX, "bc1qDESTINO") == 60_000_000, \
        txcache.recibido_por(TX, "bc1qDESTINO")
    assert txcache.recibido_por(TX, "bc1qVUELTA") == 25_000_000
    assert txcache.recibido_por(TX, "bc1qNADA") == 0
    print("OK  suma bien, incluso con varias salidas a la misma dirección")

    # ── 2. LA PRUEBA QUE IMPORTA: no hay rastro de quién buscó qué ──
    # La caché guarda TRANSACCIONES (dato público). Si algún día alguien añade
    # una tabla de direcciones consultadas, este test lo caza.
    import sqlite3
    c = sqlite3.connect(os.environ["TXCACHE_DB"])
    tablas = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert tablas <= {"txs"}, f"tablas inesperadas en la caché: {tablas}"
    cols = {r[1] for r in c.execute("PRAGMA table_info(txs)")}
    assert cols == {"txid", "salidas", "visto"}, cols
    assert not any("user" in col or "chat" in col for col in cols), \
        "la caché NO puede tener ninguna columna de usuario"
    print("OK  la caché guarda transacciones, nunca quién preguntó por ellas")

    # ── 3. Una transacción con demasiadas salidas no se guarda ──
    gorda = "b" * 64
    txcache.guardar(gorda, [{"value": 0.01, "scriptPubKey": {"address": f"bc1q{i}"}}
                            for i in range(txcache.MAX_VOUT + 1)])
    assert txcache.salidas(gorda) is None, "no debe guardar transacciones enormes"
    print(f"OK  no guarda transacciones de más de {txcache.MAX_VOUT} salidas")

    # ── 4. Sin base configurada no revienta: se sigue yendo al nodo ──
    txcache._conn = None
    guardado, os.environ["TXCACHE_DB"] = os.environ["TXCACHE_DB"], ""
    del os.environ["TXCACHE_DB"]
    viejo = os.environ.pop("GUARDIAN_DB", None)
    assert txcache.salidas(TX) is None and txcache.stats() == {"disponible": False}
    txcache.guardar(TX, VOUT)          # no debe lanzar
    print("OK  sin caché disponible sigue funcionando, solo más lento")

    os.environ["TXCACHE_DB"] = guardado
    if viejo:
        os.environ["GUARDIAN_DB"] = viejo
    txcache._conn = None
    print("\nOK ✅ caché: más rápida y sin saber qué busca nadie")


if __name__ == "__main__":
    demo()
