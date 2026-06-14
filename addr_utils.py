"""Detección y validación del tipo de dirección Bitcoin.

Base58 (1.../3...) se valida con bip_utils.
Bech32/Bech32m (bc1...) con la implementación de referencia BIP173/BIP350.
"""
from bip_utils import P2PKHAddrDecoder, P2SHAddrDecoder

# ─── Bech32 / Bech32m (referencia BIP173 + BIP350) ──────────────────────────────
_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if ((b >> i) & 1) else 0
    return chk


def _hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _verify_checksum(hrp, data):
    const = _polymod(_hrp_expand(hrp) + data)
    if const == 1:
        return "bech32"
    if const == 0x2bc830a3:
        return "bech32m"
    return None


def _bech32_decode(addr):
    if any(ord(x) < 33 or ord(x) > 126 for x in addr):
        return (None, None, None)
    if addr.lower() != addr and addr.upper() != addr:
        return (None, None, None)
    addr = addr.lower()
    pos = addr.rfind("1")
    if pos < 1 or pos + 7 > len(addr) or len(addr) > 90:
        return (None, None, None)
    hrp = addr[:pos]
    data = []
    for x in addr[pos + 1:]:
        d = _CHARSET.find(x)
        if d == -1:
            return (None, None, None)
        data.append(d)
    spec = _verify_checksum(hrp, data)
    if spec is None:
        return (None, None, None)
    return (hrp, data[:-6], spec)


def _convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def _decode_segwit(hrp_expected, addr):
    hrp, data, spec = _bech32_decode(addr)
    if hrp != hrp_expected or data is None or len(data) < 1:
        return (None, None)
    witver = data[0]
    prog = _convertbits(data[1:], 5, 8, False)
    if prog is None or len(prog) < 2 or len(prog) > 40 or witver > 16:
        return (None, None)
    if witver == 0 and len(prog) not in (20, 32):
        return (None, None)
    if witver == 0 and spec != "bech32":
        return (None, None)
    if witver != 0 and spec != "bech32m":
        return (None, None)
    return (witver, prog)


def detect_address_type(addr):
    """Devuelve la clave del tipo (legacy/p2sh/p2wpkh/p2wsh/p2tr/segwit_other) o None si no es válida."""
    a = addr.strip()
    if not a:
        return None
    if a[0] == "1":
        try:
            P2PKHAddrDecoder.DecodeAddr(a, net_ver=b"\x00")
            return "legacy"
        except Exception:
            return None
    if a[0] == "3":
        try:
            P2SHAddrDecoder.DecodeAddr(a, net_ver=b"\x05")
            return "p2sh"
        except Exception:
            return None
    if a.lower().startswith("bc1"):
        witver, prog = _decode_segwit("bc", a)
        if witver is None:
            return None
        if witver == 0 and len(prog) == 20:
            return "p2wpkh"
        if witver == 0 and len(prog) == 32:
            return "p2wsh"
        if witver == 1 and len(prog) == 32:
            return "p2tr"
        return "segwit_other"
    return None


# ─── Explicaciones (ES / EN) ─────────────────────────────────────────────────────
ADDR_TYPES = {
    "legacy": {
        "es": """🏷️ *Legacy (P2PKH)*

El tipo más antiguo de Bitcoin. Empieza con *1*. Funciona en todas las wallets, pero paga las *comisiones más altas*.

👤 Es de *una sola firma* (single-sig).""",
        "en": """🏷️ *Legacy (P2PKH)*

Bitcoin's oldest address type. Starts with *1*. Works in every wallet, but pays the *highest fees*.

👤 It's *single-sig* (one signature).""",
        "short_es": "Legacy (1) — una firma",
        "short_en": "Legacy (1) — single-sig",
    },
    "p2sh": {
        "es": """🏷️ *P2SH (empieza con 3)*

Una dirección de _script_. Puede ser *SegWit anidado* (una firma) *o multisig* (varias firmas). Desde la dirección sola NO se puede saber cuál de los dos.

🔐 Se usa a menudo para *multisig*.""",
        "en": """🏷️ *P2SH (starts with 3)*

A _script_ address. It can be *Nested SegWit* (single-sig) *or multisig* (several signatures). From the address alone you can't tell which.

🔐 Often used for *multisig*.""",
        "short_es": "P2SH (3) — anidada o multisig",
        "short_en": "P2SH (3) — nested or multisig",
    },
    "p2wpkh": {
        "es": """🏷️ *Native SegWit (P2WPKH)*

La más usada hoy. Empieza con *bc1q* (corta). Tiene *comisiones más baratas* que Legacy.

👤 Es de *una sola firma* (single-sig).""",
        "en": """🏷️ *Native SegWit (P2WPKH)*

The most used type today. Starts with *bc1q* (short). *Cheaper fees* than Legacy.

👤 It's *single-sig* (one signature).""",
        "short_es": "Native SegWit (bc1q) — una firma",
        "short_en": "Native SegWit (bc1q) — single-sig",
    },
    "p2wsh": {
        "es": """🏷️ *Native SegWit Script (P2WSH)*

Empieza con *bc1q* pero es más *larga*. Es una dirección de _script_, usada *a menudo para multisig* (varias firmas).

🔐 Comisiones baratas + scripts avanzados.""",
        "en": """🏷️ *Native SegWit Script (P2WSH)*

Starts with *bc1q* but is *longer*. It's a _script_ address, *often used for multisig*.

🔐 Cheap fees + advanced scripts.""",
        "short_es": "Native SegWit Script (bc1q) — a menudo multisig",
        "short_en": "Native SegWit Script (bc1q) — often multisig",
    },
    "p2tr": {
        "es": """🏷️ *Taproot (P2TR)*

Lo más nuevo (activado en 2021). Empieza con *bc1p*. Mejora *privacidad y eficiencia*.

🌳 Puede esconder multisig o scripts complejos sin que se note. Desde fuera NO se sabe si es de una o varias firmas.""",
        "en": """🏷️ *Taproot (P2TR)*

The newest type (activated 2021). Starts with *bc1p*. Improves *privacy and efficiency*.

🌳 It can hide multisig or complex scripts. From outside you can't tell if it's single or multisig.""",
        "short_es": "Taproot (bc1p)",
        "short_en": "Taproot (bc1p)",
    },
    "segwit_other": {
        "es": """🏷️ *SegWit (versión futura)*

Empieza con *bc1* pero usa una versión de testigo nueva o futura. Es válida, pero todavía poco común.""",
        "en": """🏷️ *SegWit (future version)*

Starts with *bc1* but uses a new or future witness version. Valid, but still uncommon.""",
        "short_es": "SegWit (versión futura)",
        "short_en": "SegWit (future version)",
    },
}


def addr_type_card(key, lg):
    info = ADDR_TYPES.get(key)
    if not info:
        return None
    return info["es"] if lg == "es" else info["en"]


def addr_type_short(key, lg):
    info = ADDR_TYPES.get(key)
    if not info:
        return "?"
    return info["short_es"] if lg == "es" else info["short_en"]
