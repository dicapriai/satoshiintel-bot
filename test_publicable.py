"""Que el repositorio se pueda publicar sin filtrar nada.

QUÉ MIRA — Y POR QUÉ ASÍ
Solo los archivos que **git publicaría** (`git ls-files`). Mirar el disco entero
da falsas alarmas con lo que ya está en .gitignore, y una alarma falsa repetida
acaba haciendo que se ignoren las de verdad.

Este test nació de una fuga real: al escribir `test_censura.py` se coló dentro
el nombre del tailnet de verdad. Un test no necesita datos reales para
demostrar que algo se tacha.
"""
import pathlib
import re
import subprocess

# La xpub del vector de prueba 1 de BIP32: está publicada en la propia
# especificación, la usa medio mundo en sus tests y no es de nadie.
XPUB_DEL_ESTANDAR = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8Nqtwy"

PATRONES = {
    "token de Telegram":  re.compile(r"\b\d{9,10}:[A-Za-z0-9_-]{35}\b"),
    "clave Fernet":       re.compile(r"\b[A-Za-z0-9_-]{43}=\B"),
    "IP de Tailscale":    re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+\b"),
    # Un tailnet de verdad es hexadecimal al azar (tail6ae859) y nunca lleva
    # "ejemplo" ni "prueba" dentro; los ejemplos de los tests sí.
    "host .ts.net":       re.compile(
        r"\b(?!(?:[\w.-]*(?:ejemplo|example|prueba|test|demo)))[\w.-]+\.ts\.net"),
    "nombre del tailnet": re.compile(r"\btail[0-9a-f]{8,}\b"),
    "el servidor":        re.compile(r"\bsrv\d{6,}\b"),
    # El nombre del usuario NO se escribe aquí (este archivo también se
    # publica): se saca de la carpeta personal en tiempo de ejecución.
    "el equipo personal": re.compile(
        rf"{re.escape(pathlib.Path.home().name)}|umbrel\.local", re.I),
    # Se descartan los ejemplos y las variables de shell: una alarma falsa
    # repetida acaba haciendo que se ignoren las de verdad.
    "cadena de Postgres": re.compile(
        r"postgres(?:ql)?://(?!usuario|user|USER|\$)[^\s:$]+:(?!password|PASSWORD|\$)[^\s@$]+@"),
    "xpub de alguien":    re.compile(r"\b[xyz]pub[1-9A-HJ-NP-Za-km-z]{100,}\b"),
}


def demo():
    salida = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    archivos = [a for a in salida.stdout.splitlines() if a.strip()]
    assert archivos, "no pude listar los archivos del repositorio"

    hallazgos = []
    for nombre in archivos:
        f = pathlib.Path(nombre)
        if not f.is_file() or f.suffix in (".png", ".jpg", ".jpeg", ".ico", ".pdf"):
            continue
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for etiqueta, patron in PATRONES.items():
            for encontrado in patron.findall(txt):
                trozo = encontrado if isinstance(encontrado, str) else str(encontrado)
                if XPUB_DEL_ESTANDAR in trozo:
                    continue
                hallazgos.append(f"{nombre}: {etiqueta} -> {trozo[:40]}")

    assert not hallazgos, "NO PUBLICAR — se filtraría:\n  " + "\n  ".join(hallazgos)
    print(f"OK  los {len(archivos)} archivos publicables no filtran nada")

    # Lo privado tiene que seguir estando excluido
    # Lo que NUNCA puede estar dentro, valga el proyecto que valga
    ignorados = pathlib.Path(".gitignore").read_text().split()
    for imprescindible in (".env", "*.db"):
        assert imprescindible in ignorados, f".gitignore debe excluir {imprescindible}"
    seguidos = set(archivos)
    prohibidos = [a for a in seguidos
                  if a == ".env" or a.endswith("/.env") or a.endswith(".db")
                  or a.endswith(".key")]
    assert not prohibidos, f"¡esto está dentro del repositorio!: {prohibidos}"
    print("OK  ni .env, ni bases de datos, ni llaves dentro del repositorio")

    print("\nOK ✅ publicable: se puede abrir el código sin filtrar nada tuyo")


if __name__ == "__main__":
    demo()
