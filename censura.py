"""Tacha datos sensibles antes de que lleguen al registro.

POR QUÉ NO BASTA CON "NO ESCRIBIR DIRECCIONES EN LOS LOGS"
El código no escribía ninguna a mano — había hasta comentarios diciéndolo. Pero
`raise_for_status()` de httpx construye su mensaje con la URL entera, y esa URL
lleva dentro la dirección del usuario. Al registrar la excepción con `%s`, la
dirección acababa en el journal igual, y con ella el nombre del nodo en la
tailnet.

Ese es el patrón: la fuga no viene de lo que escribes, viene de lo que ARRASTRA
un objeto que no fabricaste tú. Revisar cada `logger.warning` no sirve, porque
mañana alguien registra otra excepción distinta.

POR ESO SE FILTRA A LA SALIDA
Un filtro en la raíz del logging ve TODO lo que se va a escribir, venga de donde
venga, y tacha lo que no puede salir. Es el único punto por el que pasa todo.

QUÉ SE TACHA
  · Direcciones Bitcoin (bc1..., 1..., 3...)
  · Llaves públicas extendidas (xpub, ypub, zpub, tpub...)
  · Identificadores de transacción (64 hex)
  · El nombre y la IP del nodo propio

Lo que queda es útil para depurar ("no pude conectar", "404") sin decir de quién
era la consulta.
"""
from __future__ import annotations

import logging
import os
import re

# Direcciones: legacy (1/3), y bech32 (bc1). Se piden longitudes realistas para
# no tachar por accidente cualquier palabra que empiece por 1 o 3.
_PATRONES = [
    (re.compile(r'\bbc1[a-z0-9]{25,87}\b', re.I), "«dirección»"),
    (re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'), "«dirección»"),
    (re.compile(r'\b[xyztuv]pub[1-9A-HJ-NP-Za-km-z]{50,}\b'), "«xpub»"),
    (re.compile(r'\b[0-9a-f]{64}\b', re.I), "«txid»"),
]


def _patrones_del_nodo() -> list[tuple[re.Pattern, str]]:
    """El nodo se saca del entorno: nunca escrito en el código, que es público."""
    fuera = []
    for var in ("ELECTRS_HOST", "MEMPOOL_BASE", "BITCOIN_RPC_HOST"):
        val = (os.getenv(var) or "").strip()
        if not val:
            continue
        val = val.replace("https://", "").replace("http://", "").split("/")[0]
        host = val.split(":")[0]
        if len(host) > 3:
            fuera.append((re.compile(re.escape(host), re.I), "«nodo»"))
    return fuera


class Censor(logging.Filter):
    """Tacha lo sensible de cada línea antes de escribirla."""

    def __init__(self):
        super().__init__()
        self.patrones = _PATRONES + _patrones_del_nodo()

    def _limpiar(self, texto: str) -> str:
        for patron, reemplazo in self.patrones:
            texto = patron.sub(reemplazo, texto)
        return texto

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            # getMessage() ya junta el mensaje con sus argumentos: es el texto
            # final, el mismo que se escribiría. Se limpia y se deja fijado, así
            # los args no vuelven a interpolarse sucios más adelante.
            mensaje = record.getMessage()
        except Exception:
            return True
        limpio = self._limpiar(mensaje)
        if limpio != mensaje:
            record.msg, record.args = limpio, ()
        if record.exc_info:
            # El texto de la excepción se escribe aparte, por otro camino, y
            # arrastra la URL completa. Sin esto la fuga seguiría viva.
            record.exc_text = self._limpiar(
                logging.Formatter().formatException(record.exc_info))
            record.exc_info = None
        return True


def instalar() -> None:
    """Engancha el filtro a todo lo que escriba. Se llama al arrancar el bot."""
    censor = Censor()
    raiz = logging.getLogger()
    raiz.addFilter(censor)
    for h in raiz.handlers:
        h.addFilter(censor)
    # Un handler añadido después (por otra librería) se saltaría el filtro si
    # solo lo pusiéramos en los de ahora.
    original = logging.Logger.addHandler

    def addHandler(self, hdlr):          # noqa: N802  (nombre de la stdlib)
        hdlr.addFilter(censor)
        return original(self, hdlr)

    logging.Logger.addHandler = addHandler
