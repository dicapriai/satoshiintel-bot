"""Que nada sensible llegue al registro, venga por donde venga.

LA FUGA QUE MOTIVÓ ESTO
El código no escribía direcciones en los logs — había hasta comentarios que lo
afirmaban. Pero `raise_for_status()` de httpx construye su mensaje con la URL
completa, y esa URL lleva la dirección del usuario. Al registrar la excepción
con %s acababa en el journal la dirección Y el nombre del nodo en la tailnet.

La lección: la fuga no venía de lo que el código escribe, sino de lo que
arrastra un objeto ajeno. Por eso se filtra a la SALIDA, no en cada llamada.
"""
import io
import logging
import os

os.environ["ELECTRS_HOST"] = "nodo-ejemplo.tailnet-de-prueba.ts.net"
import censura

SENSIBLES = {
    "dirección bech32": "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq",
    "dirección legacy": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "dirección P2SH": "3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5",
    "xpub": ("xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKk"
             "NAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"),
    "txid": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "nombre del nodo": "nodo-ejemplo.tailnet-de-prueba.ts.net",
}


def _capturar(emitir) -> str:
    cap = io.StringIO()
    raiz = logging.getLogger()
    viejos = raiz.handlers[:]
    raiz.handlers = []
    h = logging.StreamHandler(cap)
    h.setFormatter(logging.Formatter("%(message)s"))
    raiz.addHandler(h)
    raiz.setLevel(logging.DEBUG)
    censura.instalar()
    try:
        emitir(logging.getLogger("prueba"))
    finally:
        raiz.handlers = viejos
    return cap.getvalue()


def demo():
    # ── 1. Escrito directamente en el mensaje ──
    for nombre, valor in SENSIBLES.items():
        out = _capturar(lambda lg, v=valor: lg.warning("fallo con %s", v))
        assert valor not in out, f"se coló {nombre} en el log: {out.strip()[:80]}"
    print(f"OK  los {len(SENSIBLES)} datos sensibles se tachan en el mensaje")

    # ── 2. Dentro del TEXTO DE UNA EXCEPCIÓN (el caso real) ──
    addr = SENSIBLES["dirección bech32"]
    def emitir(lg):
        try:
            raise ValueError(f"Client error '404' for url "
                             f"'http://nodo-ejemplo.tailnet-de-prueba.ts.net:3006/api/address/{addr}'")
        except ValueError as e:
            lg.warning("summary error: %s", e)
    out = _capturar(emitir)
    assert addr not in out and "tailnet-de-prueba" not in out, out
    print("OK  se tacha aunque venga dentro del texto de una excepción")

    # ── 3. Y en el rastro completo (exc_info), que se escribe por otro camino ──
    def emitir_traza(lg):
        try:
            raise ValueError(f"url http://nodo-ejemplo.tailnet-de-prueba.ts.net/api/address/{addr}")
        except ValueError:
            lg.exception("reventó")
    out = _capturar(emitir_traza)
    assert addr not in out and "tailnet-de-prueba" not in out, out[:200]
    print("OK  se tacha también en el rastro completo del error")

    # ── 4. Lo que NO debe tacharse: el log tiene que seguir sirviendo ──
    out = _capturar(lambda lg: lg.warning(
        "timeout tras 12s conectando (intento 2 de 3), código 429"))
    for trozo in ("timeout", "12s", "429", "intento 2"):
        assert trozo in out, f"se cargó información útil: falta {trozo!r}"
    print("OK  no tacha de más: el log sigue sirviendo para depurar")

    print("\nOK ✅ censura: el journal no delata a nadie")


if __name__ == "__main__":
    demo()
