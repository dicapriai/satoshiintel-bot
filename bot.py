from __future__ import annotations

import os
import io
import re
import logging
import time
import random
import httpx
import qrcode
from bip_utils import Bip32Slip10Secp256k1, P2WPKHAddr

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

import content_edu_a, content_edu_b, content_edu_c, content_edu_d
import content_quotes
import content_dict_a, content_dict_b, content_dict_c, content_dict_d, content_dict_e
import content_quiz
import addr_utils

try:
    from dotenv import load_dotenv
    load_dotenv()  # carga el archivo .env si existe (solo local)
except ImportError:
    pass

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Config ─────────────────────────────────────────────────────────────────────
# Crea tu bot con @BotFather y pon el token en la variable de entorno
# TELEGRAM_BOT_TOKEN, o pégalo abajo.
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

SATS_PER_BTC = 100_000_000
# ─── Donaciones (xpub PÚBLICA desde variable de entorno; el repo es público) ────
DONATION_XPUB = os.environ.get("DONATION_XPUB", "")
DONATION_POOL = 20          # rota entre 20 direcciones (dentro del gap limit de Sparrow)
_donation_counter = 0
# ─── Canal y soporte ────────────────────────────────────────────────────────────
CHANNEL_URL = "https://t.me/SatoshiIntel"
CHANNEL_HANDLE = "@SatoshiIntel"
SUPPORT_EMAIL = "SatoshiIntelbot@proton.me"
HALVING_INTERVAL = 210_000
BLOCK_MINUTES = 10
PRICE_CACHE_TTL = 60
HEIGHT_CACHE_TTL = 60
_price_cache = {"usd": None, "ts": 0.0}
_height_cache = {"height": None, "ts": 0.0}

# ─── Estados ────────────────────────────────────────────────────────────────────
(
    LANG_SELECT,
    MAIN_MENU,
    TOOLS_MENU,
    EDU_MENU,
    EDU_CAT,
    TOOL_INPUT,
    SCAM_QUIZ,
    DICT_MENU,
    DICT_CAT,
    DICT_SEARCH,
    BIP39_MENU,
    BIP39_INPUT,
    QUIZ,
    EXPLORER_INPUT,
    ADDRTYPE_INPUT,
) = range(15)

# ─── Registro de educación (carga dinámica) ────────────────────────────────────
EDU_CATS = [content_edu_a, content_edu_b, content_edu_c, content_edu_d]
CAT_BY_KEY = {m.CATEGORY["key"]: m for m in EDU_CATS}
MODULE_TO_CAT = {}
for _m in EDU_CATS:
    for _k in _m.ORDER:
        MODULE_TO_CAT[_k] = _m

# ─── Registro del diccionario (carga dinámica) ──────────────────────────────────
DICT_CATS = []
for _mod in (content_dict_a, content_dict_b, content_dict_c, content_dict_d, content_dict_e):
    DICT_CATS.extend(_mod.CATEGORIES)
DCAT_BY_KEY = {c["key"]: c for c in DICT_CATS}
TERM_TO_CAT = {}        # term_key -> category dict
for _c in DICT_CATS:
    for _tk in _c["order"]:
        TERM_TO_CAT[_tk] = _c

# ─── Lista BIP39 (2048 palabras oficiales) ──────────────────────────────────────
BIP39_PER_PAGE = 50
try:
    _bip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bip39_english.txt")
    with open(_bip_path, encoding="utf-8") as _f:
        BIP39_WORDS = [w.strip() for w in _f if w.strip()]
except Exception as _e:
    BIP39_WORDS = []
    logging.getLogger(__name__).warning("No pude cargar BIP39: %s", _e)
BIP39_SET = {w: i + 1 for i, w in enumerate(BIP39_WORDS)}
BIP39_PAGES = (len(BIP39_WORDS) + BIP39_PER_PAGE - 1) // BIP39_PER_PAGE


# ─── Helpers ────────────────────────────────────────────────────────────────────
def lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "es")


def fmt_usd(v: float) -> str:
    return f"${v:,.2f}"


def fmt_sats(v: float) -> str:
    return f"{v:,.0f}"


def fmt_btc(v: float) -> str:
    return f"{v:.8f}"


async def edit_md(query, text, kb):
    try:
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
    except Exception:
        try:
            await query.edit_message_text(text, reply_markup=kb)
        except Exception as e:
            logger.warning("edit_md fallo: %s", e)


async def reply_md(update, text, kb):
    try:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
    except Exception:
        await update.message.reply_text(text, reply_markup=kb)


# ─── APIs (precio y altura de bloque, gratis sin key) ───────────────────────────
async def get_btc_price() -> float | None:
    now = time.time()
    if _price_cache["usd"] is not None and (now - _price_cache["ts"]) < PRICE_CACHE_TTL:
        return _price_cache["usd"]
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(url)
            r.raise_for_status()
            price = float(r.json()["bitcoin"]["usd"])
            _price_cache.update(usd=price, ts=now)
            return price
    except Exception as e:
        logger.warning("precio BTC: %s", e)
        return _price_cache["usd"]


async def get_block_height() -> int | None:
    now = time.time()
    if _height_cache["height"] is not None and (now - _height_cache["ts"]) < HEIGHT_CACHE_TTL:
        return _height_cache["height"]
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://mempool.space/api/blocks/tip/height")
            r.raise_for_status()
            h = int(r.text.strip())
            _height_cache.update(height=h, ts=now)
            return h
    except Exception as e:
        logger.warning("altura bloque: %s", e)
        return _height_cache["height"]


async def get_mempool_data():
    """Devuelve (fees_dict, count) de mempool.space. None si falla."""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r1 = await c.get("https://mempool.space/api/v1/fees/recommended")
            r1.raise_for_status()
            fees = r1.json()
            count = None
            try:
                r2 = await c.get("https://mempool.space/api/mempool")
                r2.raise_for_status()
                count = r2.json().get("count")
            except Exception:
                pass
            return fees, count
    except Exception as e:
        logger.warning("mempool: %s", e)
        return None, None


async def mempool_text(lg):
    fees, count = await get_mempool_data()
    if not fees:
        return ("⚠️ No pude obtener el estado de la red. Intenta de nuevo."
                if lg == "es" else "⚠️ Couldn't fetch network status. Try again.")
    fast = fees.get("fastestFee", 0)
    half = fees.get("halfHourFee", 0)
    hour = fees.get("hourFee", 0)
    eco = fees.get("economyFee", 0)
    # costo de una transacción típica (~140 vBytes) a la tarifa rápida
    price = await get_btc_price()
    vbytes = 140
    cost_sats = fast * vbytes
    cost_usd = (cost_sats / SATS_PER_BTC * price) if price else None
    # semáforo según tarifa rápida
    if fast <= 10:
        sem = "🟢"; estado_es = "Despejada (barato enviar)"; estado_en = "Clear (cheap to send)"
    elif fast <= 50:
        sem = "🟡"; estado_es = "Moderada"; estado_en = "Moderate"
    else:
        sem = "🔴"; estado_es = "Congestionada (caro enviar)"; estado_en = "Congested (expensive)"
    count_line_es = f"📥 En espera: *{count:,}* transacciones\n" if count else ""
    count_line_en = f"📥 Waiting: *{count:,}* transactions\n" if count else ""
    cost_es = f"≈ {fmt_usd(cost_usd)}" if cost_usd is not None else f"{cost_sats:,} sats"
    cost_en = cost_es
    if lg == "es":
        return ("🌐 *Mempool en vivo — estado de la red*\n\n"
                f"{sem} Red: *{estado_es}*\n"
                f"{count_line_es}\n"
                "💸 *Comisiones (sats/vByte):*\n"
                f"• ⚡ Rápida (~10 min): *{fast}*\n"
                f"• 🕐 Media (~30 min): *{half}*\n"
                f"• 🐢 1 hora: *{hour}*\n"
                f"• 💲 Económica: *{eco}*\n\n"
                f"Enviar una transacción típica costaría {cost_es}\n\n"
                "_Datos en vivo de mempool.space._")
    return ("🌐 *Live Mempool — network status*\n\n"
            f"{sem} Network: *{estado_en}*\n"
            f"{count_line_en}\n"
            "💸 *Fees (sats/vByte):*\n"
            f"• ⚡ Fast (~10 min): *{fast}*\n"
            f"• 🕐 Medium (~30 min): *{half}*\n"
            f"• 🐢 1 hour: *{hour}*\n"
            f"• 💲 Economy: *{eco}*\n\n"
            f"A typical transaction would cost {cost_en}\n\n"
            "_Live data from mempool.space._")


# ─── Teclados ───────────────────────────────────────────────────────────────────
def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
    ]])


def main_menu_keyboard(lg):
    if lg == "es":
        rows = [
            [InlineKeyboardButton("🧮 Herramientas", callback_data="tools")],
            [InlineKeyboardButton("📚 Educación", callback_data="education")],
            [InlineKeyboardButton("📖 Diccionario Bitcoin", callback_data="dictionary")],
            [InlineKeyboardButton("🧠 Quiz Bitcoin", callback_data="quiz")],
            [InlineKeyboardButton("🔤 Lista BIP39", callback_data="bip39")],
            [InlineKeyboardButton("💰 Precio de Bitcoin ahora", callback_data="price_now")],
            [InlineKeyboardButton("💬 Cita del día", callback_data="cita")],
            [InlineKeyboardButton("🧡 Apoya el proyecto", callback_data="donate")],
            [InlineKeyboardButton("📢 Únete al canal", url=CHANNEL_URL)],
            [InlineKeyboardButton("📧 Soporte", callback_data="support")],
            [InlineKeyboardButton("🌎 Cambiar idioma", callback_data="change_lang")],
        ]
    else:
        rows = [
            [InlineKeyboardButton("🧮 Tools", callback_data="tools")],
            [InlineKeyboardButton("📚 Education", callback_data="education")],
            [InlineKeyboardButton("📖 Bitcoin Dictionary", callback_data="dictionary")],
            [InlineKeyboardButton("🧠 Bitcoin Quiz", callback_data="quiz")],
            [InlineKeyboardButton("🔤 BIP39 Wordlist", callback_data="bip39")],
            [InlineKeyboardButton("💰 Bitcoin Price Now", callback_data="price_now")],
            [InlineKeyboardButton("💬 Quote of the day", callback_data="cita")],
            [InlineKeyboardButton("🧡 Support the project", callback_data="donate")],
            [InlineKeyboardButton("📢 Join our channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("📧 Support", callback_data="support")],
            [InlineKeyboardButton("🌎 Change language", callback_data="change_lang")],
        ]
    return InlineKeyboardMarkup(rows)


def tools_keyboard(lg):
    if lg == "es":
        rows = [
            [InlineKeyboardButton("💰 Precio de Bitcoin ahora", callback_data="price_now")],
            [InlineKeyboardButton("💵 USD → BTC / SAT", callback_data="conv_usd")],
            [InlineKeyboardButton("⚡ SATS → USD / BTC", callback_data="conv_sat")],
            [InlineKeyboardButton("₿ BTC → USD / SAT", callback_data="conv_btc")],
            [InlineKeyboardButton("🟧 Apila Sats (DCA)", callback_data="dca")],
            [InlineKeyboardButton("📈 Ganancia / Profit", callback_data="profit")],
            [InlineKeyboardButton("🏖️ Retiro (ahorro futuro)", callback_data="retirement")],
            [InlineKeyboardButton("⏳ Cuenta regresiva al halving", callback_data="halving")],
            [InlineKeyboardButton("🌐 Mempool en vivo", callback_data="mempool")],
            [InlineKeyboardButton("🔎 Explorador de TX / dirección", callback_data="explorer")],
            [InlineKeyboardButton("🏷️ ¿Qué tipo de dirección es?", callback_data="addrtype")],
            [InlineKeyboardButton("🧮 ¿UTXO gastable o polvo?", callback_data="utxo")],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="back_main")],
        ]
    else:
        rows = [
            [InlineKeyboardButton("💰 Bitcoin Price Now", callback_data="price_now")],
            [InlineKeyboardButton("💵 USD → BTC / SAT", callback_data="conv_usd")],
            [InlineKeyboardButton("⚡ SATS → USD / BTC", callback_data="conv_sat")],
            [InlineKeyboardButton("₿ BTC → USD / SAT", callback_data="conv_btc")],
            [InlineKeyboardButton("🟧 Stack Sats (DCA)", callback_data="dca")],
            [InlineKeyboardButton("📈 Profit calculator", callback_data="profit")],
            [InlineKeyboardButton("🏖️ Retirement (future savings)", callback_data="retirement")],
            [InlineKeyboardButton("⏳ Halving countdown", callback_data="halving")],
            [InlineKeyboardButton("🌐 Live Mempool", callback_data="mempool")],
            [InlineKeyboardButton("🔎 TX / address explorer", callback_data="explorer")],
            [InlineKeyboardButton("🏷️ What address type is it?", callback_data="addrtype")],
            [InlineKeyboardButton("🧮 UTXO spendable or dust?", callback_data="utxo")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")],
        ]
    return InlineKeyboardMarkup(rows)


def tools_back_keyboard(lg):
    label = "🔙 Herramientas" if lg == "es" else "🔙 Tools"
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data="tools")]])


def education_keyboard(lg):
    rows = []
    for m in EDU_CATS:
        label = m.CATEGORY["btn_es"] if lg == "es" else m.CATEGORY["btn_en"]
        rows.append([InlineKeyboardButton(label, callback_data=m.CATEGORY["key"])])
    rows.append([InlineKeyboardButton("🔙 Menú Principal" if lg == "es" else "🔙 Main Menu",
                                      callback_data="back_main")])
    return InlineKeyboardMarkup(rows)


def category_keyboard(cat_mod, lg):
    rows = []
    for k in cat_mod.ORDER:
        mod = cat_mod.MODULES[k]
        label = mod["btn_es"] if lg == "es" else mod["btn_en"]
        rows.append([InlineKeyboardButton(label, callback_data=k)])
    rows.append([InlineKeyboardButton("🔙 Educación" if lg == "es" else "🔙 Education",
                                      callback_data="education")])
    return InlineKeyboardMarkup(rows)


def module_keyboard(cat_mod, lg):
    cat_label = cat_mod.CATEGORY["btn_es"] if lg == "es" else cat_mod.CATEGORY["btn_en"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔙 {cat_label}", callback_data=cat_mod.CATEGORY["key"])],
        [InlineKeyboardButton("📚 Educación" if lg == "es" else "📚 Education", callback_data="education")],
    ])


# ─── /start, /menu, /idioma, /precio ────────────────────────────────────────────
async def start(update, context):
    context.user_data.clear()
    await update.message.reply_text(
        "₿ *Bienvenido a SatoshiIntel*\n"
        "Tu guía Bitcoin de bolsillo.\n"
        "Aprende, calcula y vuélvete soberano.\n"
        "🔐 _No confíes, verifica._\n\n"
        "🇬🇧 _Your pocket Bitcoin guide. Learn, calculate, become sovereign. Don't trust, verify._\n\n"
        "Elige tu idioma / Choose your language:",
        parse_mode="Markdown", reply_markup=lang_keyboard()
    )
    return LANG_SELECT


async def lang_select(update, context):
    query = update.callback_query
    await query.answer()
    lg = "es" if query.data == "lang_es" else "en"
    context.user_data["lang"] = lg
    await edit_md(query, main_title(lg), main_menu_keyboard(lg))
    return MAIN_MENU


def main_title(lg):
    return "📋 *Menú Principal* — elige una opción:" if lg == "es" else "📋 *Main Menu* — choose an option:"


async def menu_command(update, context):
    lg = lang(context)
    await update.message.reply_text(main_title(lg), parse_mode="Markdown", reply_markup=main_menu_keyboard(lg))
    return MAIN_MENU


async def idioma_command(update, context):
    await update.message.reply_text("🌎 Elige tu idioma / Choose your language:", reply_markup=lang_keyboard())
    return LANG_SELECT


async def precio_command(update, context):
    lg = lang(context)
    price = await get_btc_price()
    await reply_md(update, price_text(lg, price), main_menu_keyboard(lg))
    return MAIN_MENU


# ─── Precio / cita ──────────────────────────────────────────────────────────────
def price_text(lg, price):
    if not price:
        return ("⚠️ No pude obtener el precio ahora. Intenta de nuevo en un momento."
                if lg == "es" else "⚠️ Couldn't fetch the price right now. Try again shortly.")
    spd = SATS_PER_BTC / price
    if lg == "es":
        return ("💰 *Precio de Bitcoin ahora*\n\n"
                f"1 BTC = *{fmt_usd(price)}*\n"
                f"1 USD = *{fmt_sats(spd)} sats*\n"
                "100,000,000 sats = 1 BTC\n\n_Fuente: CoinGecko (en vivo)_")
    return ("💰 *Bitcoin Price Now*\n\n"
            f"1 BTC = *{fmt_usd(price)}*\n"
            f"1 USD = *{fmt_sats(spd)} sats*\n"
            "100,000,000 sats = 1 BTC\n\n_Source: CoinGecko (live)_")


def cita_text(lg):
    q = random.choice(content_quotes.QUOTES)
    header = "💬 *Cita del día*" if lg == "es" else "💬 *Quote of the day*"
    body = q["es"] if lg == "es" else q["en"]
    return f"{header}\n\n_{body}_\n\n— {q['author']}"


def support_text(lg):
    if lg == "es":
        return ("📧 *Soporte y contacto*\n\n"
                "¿Dudas, ideas o algún problema? Escríbenos:\n\n"
                f"`{SUPPORT_EMAIL}`\n\n"
                f"📢 Síguenos en el canal: {CHANNEL_HANDLE}\n\n"
                "¡Gracias por usar SatoshiIntel! 🟠\n"
                "_No confíes, verifica._")
    return ("📧 *Support & contact*\n\n"
            "Questions, ideas or a problem? Write to us:\n\n"
            f"`{SUPPORT_EMAIL}`\n\n"
            f"📢 Follow our channel: {CHANNEL_HANDLE}\n\n"
            "Thanks for using SatoshiIntel! 🟠\n"
            "_Don't trust, verify._")


# ─── Menú principal ─────────────────────────────────────────────────────────────
async def main_menu_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data

    if data == "tools":
        title = "🧮 *Herramientas* — elige una:" if lg == "es" else "🧮 *Tools* — choose one:"
        await edit_md(query, title, tools_keyboard(lg))
        return TOOLS_MENU
    if data == "education":
        title = "📚 *Educación* — elige una categoría:" if lg == "es" else "📚 *Education* — choose a category:"
        await edit_md(query, title, education_keyboard(lg))
        return EDU_MENU
    if data == "dictionary":
        await edit_md(query, dict_menu_title(lg), dictionary_keyboard(lg))
        return DICT_MENU
    if data == "bip39":
        await edit_md(query, bip39_menu_text(lg), bip39_keyboard(lg))
        return BIP39_MENU
    if data == "quiz":
        return await start_quiz(query, context, lg)
    if data == "donate":
        return await send_donation(query, lg)
    if data == "support":
        await edit_md(query, support_text(lg), main_menu_keyboard(lg))
        return MAIN_MENU
    if data == "price_now":
        price = await get_btc_price()
        await edit_md(query, price_text(lg, price), main_menu_keyboard(lg))
        return MAIN_MENU
    if data == "cita":
        await edit_md(query, cita_text(lg), main_menu_keyboard(lg))
        return MAIN_MENU
    if data == "change_lang":
        await edit_md(query, "🌎 Elige tu idioma / Choose your language:", lang_keyboard())
        return LANG_SELECT
    return MAIN_MENU


async def show_main_menu(query, lg):
    await edit_md(query, main_title(lg), main_menu_keyboard(lg))
    return MAIN_MENU


# ─── Educación ──────────────────────────────────────────────────────────────────
async def education_menu_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data

    if data == "back_main":
        return await show_main_menu(query, lg)
    if data == "education":
        title = "📚 *Educación* — elige una categoría:" if lg == "es" else "📚 *Education* — choose a category:"
        await edit_md(query, title, education_keyboard(lg))
        return EDU_MENU
    if data in CAT_BY_KEY:
        cat = CAT_BY_KEY[data]
        label = cat.CATEGORY["btn_es"] if lg == "es" else cat.CATEGORY["btn_en"]
        title = (f"{label}\n\nElige un tema:" if lg == "es" else f"{label}\n\nChoose a topic:")
        await edit_md(query, title, category_keyboard(cat, lg))
        return EDU_CAT
    return EDU_MENU


async def edu_cat_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data

    if data == "back_main":
        return await show_main_menu(query, lg)
    if data == "education":
        title = "📚 *Educación* — elige una categoría:" if lg == "es" else "📚 *Education* — choose a category:"
        await edit_md(query, title, education_keyboard(lg))
        return EDU_MENU
    if data in CAT_BY_KEY:
        cat = CAT_BY_KEY[data]
        label = cat.CATEGORY["btn_es"] if lg == "es" else cat.CATEGORY["btn_en"]
        title = (f"{label}\n\nElige un tema:" if lg == "es" else f"{label}\n\nChoose a topic:")
        await edit_md(query, title, category_keyboard(cat, lg))
        return EDU_CAT
    if data in MODULE_TO_CAT:
        cat = MODULE_TO_CAT[data]
        text = cat.MODULES[data][lg]
        await edit_md(query, text, module_keyboard(cat, lg))
        return EDU_CAT
    return EDU_CAT


# ─── Herramientas: flujos numéricos ─────────────────────────────────────────────
# Cada flujo es una lista de pasos (clave, prompt_es, prompt_en).
TOOL_FLOWS = {
    "conv_usd": [("usd",
                  "💵 Escribe cuántos *dólares (USD)* tienes:\n\n_Ejemplo: 100_",
                  "💵 Type how many *USD* you have:\n\n_Example: 100_")],
    "conv_sat": [("sat",
                  "⚡ Escribe cuántos *satoshis* tienes:\n\n_Ejemplo: 50000_",
                  "⚡ Type how many *satoshis* you have:\n\n_Example: 50000_")],
    "conv_btc": [("btc",
                  "₿ Escribe cuántos *bitcoins (BTC)* tienes:\n\n_Ejemplo: 0.05_",
                  "₿ Type how many *bitcoins (BTC)* you have:\n\n_Example: 0.05_")],
    "dca": [
        ("aporte", "🟧 *Apila Sats (DCA)*\n\n¿Cuánto invertirías cada semana en USD? (ej. 20):",
                   "🟧 *Stack Sats (DCA)*\n\nHow much would you invest each week in USD? (e.g. 20):"),
        ("anios", "¿Durante cuántos años? (ej. 4):",
                  "For how many years? (e.g. 4):"),
    ],
    "profit": [
        ("compra", "📈 *Calculadora de Ganancia*\n\n¿A qué precio compraste 1 BTC? en USD (ej. 30000):",
                   "📈 *Profit Calculator*\n\nAt what price did you buy 1 BTC? in USD (e.g. 30000):"),
        ("invertido", "¿Cuánto dinero invertiste en total? en USD (ej. 500):",
                      "How much money did you invest in total? in USD (e.g. 500):"),
    ],
    "retirement": [
        ("mensual", "🏖️ *Calculadora de Retiro*\n\n¿Cuánto ahorrarías cada mes en USD? (ej. 100):",
                    "🏖️ *Retirement Calculator*\n\nHow much would you save each month in USD? (e.g. 100):"),
        ("anios", "¿Durante cuántos años? (ej. 20):",
                  "For how many years? (e.g. 20):"),
        ("crecimiento", "¿Qué crecimiento anual esperas del precio de BTC en %? (ej. 20):",
                        "What annual BTC price growth do you expect in %? (e.g. 20):"),
    ],
    "utxo": [
        ("sats", "🧮 *¿UTXO gastable o polvo?*\n\n¿Cuántos *sats* tiene ese pedacito de bitcoin? (ej. 1000):",
                 "🧮 *UTXO spendable or dust?*\n\nHow many *sats* is that bitcoin chunk? (e.g. 1000):"),
    ],
}


def parse_number(text):
    cleaned = text.strip().replace(",", "").replace("$", "").replace("%", "").replace(" ", "")
    try:
        v = float(cleaned)
        return v if v >= 0 else None
    except ValueError:
        return None


async def start_flow(query, context, tool, lg):
    context.user_data["flow"] = {"tool": tool, "step": 0, "data": {}}
    prompt = TOOL_FLOWS[tool][0][1] if lg == "es" else TOOL_FLOWS[tool][0][2]
    await edit_md(query, prompt, tools_back_keyboard(lg))
    return TOOL_INPUT


async def tool_input(update, context):
    lg = lang(context)
    flow = context.user_data.get("flow")
    if not flow:
        await reply_md(update, "Usa /menu", main_menu_keyboard(lg))
        return MAIN_MENU

    tool = flow["tool"]
    steps = TOOL_FLOWS[tool]
    value = parse_number(update.message.text)
    if value is None:
        msg = "❌ Escribe solo un número válido." if lg == "es" else "❌ Type a valid number only."
        await reply_md(update, msg, tools_back_keyboard(lg))
        return TOOL_INPUT

    key = steps[flow["step"]][0]
    flow["data"][key] = value
    flow["step"] += 1

    if flow["step"] < len(steps):
        prompt = steps[flow["step"]][1] if lg == "es" else steps[flow["step"]][2]
        await reply_md(update, prompt, tools_back_keyboard(lg))
        return TOOL_INPUT

    text = await compute_tool(tool, flow["data"], lg)
    context.user_data.pop("flow", None)
    await reply_md(update, text, tools_keyboard(lg))
    return TOOLS_MENU


async def compute_tool(tool, d, lg):
    if tool in ("conv_usd", "conv_sat", "conv_btc"):
        price = await get_btc_price()
        if not price:
            return "⚠️ No pude obtener el precio. Intenta de nuevo." if lg == "es" else "⚠️ Couldn't fetch the price. Try again."
        if tool == "conv_usd":
            usd = d["usd"]; btc = usd / price; sats = btc * SATS_PER_BTC
        elif tool == "conv_sat":
            sats = d["sat"]; btc = sats / SATS_PER_BTC; usd = btc * price
        else:
            btc = d["btc"]; sats = btc * SATS_PER_BTC; usd = btc * price
        if lg == "es":
            return ("✅ *Resultado*\n\n"
                    f"💵 USD: *{fmt_usd(usd)}*\n"
                    f"₿ BTC: *{fmt_btc(btc)}*\n"
                    f"⚡ Satoshis: *{fmt_sats(sats)} sats*\n\n"
                    f"_Precio: 1 BTC = {fmt_usd(price)} (CoinGecko en vivo)_")
        return ("✅ *Result*\n\n"
                f"💵 USD: *{fmt_usd(usd)}*\n"
                f"₿ BTC: *{fmt_btc(btc)}*\n"
                f"⚡ Satoshis: *{fmt_sats(sats)} sats*\n\n"
                f"_Price: 1 BTC = {fmt_usd(price)} (CoinGecko live)_")

    if tool == "inflation":
        monto = d["monto"]; i = d["infl"] / 100.0; n = d["anios"]
        real = monto / ((1 + i) ** n)
        perdida = monto - real
        pct = (1 - 1 / ((1 + i) ** n)) * 100
        if lg == "es":
            return ("📉 *Pérdida de poder adquisitivo*\n\n"
                    f"Hoy tienes: *{fmt_usd(monto)}*\n"
                    f"Con {d['infl']:.1f}% de inflación anual, en {n:.0f} años\n"
                    f"valdrán como: *{fmt_usd(real)}* de hoy\n\n"
                    f"Pierdes: *{fmt_usd(perdida)}* (*{pct:.1f}%*) 😮\n\n"
                    "_El dinero fiat no tiene tope; Bitcoin sí: 21,000,000._\n"
                    "_\"Bitcoin son matemáticas, el dinero fiat es humo.\"_")
        return ("📉 *Purchasing power loss*\n\n"
                f"Today you have: *{fmt_usd(monto)}*\n"
                f"At {d['infl']:.1f}% annual inflation, in {n:.0f} years\n"
                f"it will feel like: *{fmt_usd(real)}* of today\n\n"
                f"You lose: *{fmt_usd(perdida)}* (*{pct:.1f}%*) 😮\n\n"
                "_Fiat has no cap; Bitcoin does: 21,000,000._")

    if tool == "dca":
        price = await get_btc_price()
        if not price:
            return "⚠️ No pude obtener el precio. Intenta de nuevo." if lg == "es" else "⚠️ Couldn't fetch the price. Try again."
        aporte = d["aporte"]; anios = d["anios"]; weeks = anios * 52
        invertido = aporte * weeks
        sats = (aporte / price) * SATS_PER_BTC * weeks
        btc = sats / SATS_PER_BTC
        if lg == "es":
            return ("🟧 *Apila Sats (DCA)*\n\n"
                    f"Inviertes *{fmt_usd(aporte)}/semana* durante *{anios:.0f} años*\n"
                    f"({weeks:.0f} compras)\n\n"
                    f"Total invertido: *{fmt_usd(invertido)}*\n"
                    f"Acumularías ≈ *{fmt_sats(sats)} sats* (*{fmt_btc(btc)} BTC*)\n\n"
                    f"_Estimación al precio de hoy ({fmt_usd(price)}). El precio real varía cada semana._\n"
                    "_DCA elimina las emociones de miedo y avaricia._")
        return ("🟧 *Stack Sats (DCA)*\n\n"
                f"You invest *{fmt_usd(aporte)}/week* for *{anios:.0f} years*\n"
                f"({weeks:.0f} buys)\n\n"
                f"Total invested: *{fmt_usd(invertido)}*\n"
                f"You'd stack ≈ *{fmt_sats(sats)} sats* (*{fmt_btc(btc)} BTC*)\n\n"
                f"_Estimate at today's price ({fmt_usd(price)}). Real price varies weekly._")

    if tool == "profit":
        price = await get_btc_price()
        if not price:
            return "⚠️ No pude obtener el precio. Intenta de nuevo." if lg == "es" else "⚠️ Couldn't fetch the price. Try again."
        compra = d["compra"]; invertido = d["invertido"]
        if compra <= 0:
            return "❌ El precio de compra debe ser mayor que 0." if lg == "es" else "❌ Buy price must be greater than 0."
        btc = invertido / compra
        sats = btc * SATS_PER_BTC
        valor = btc * price
        ganancia = valor - invertido
        pct = (price / compra - 1) * 100
        emoji = "🟢📈" if ganancia >= 0 else "🔴📉"
        if lg == "es":
            etiqueta = "Ganancia" if ganancia >= 0 else "Pérdida"
            return ("📈 *Calculadora de Ganancia*\n\n"
                    f"Invertiste: *{fmt_usd(invertido)}* a *{fmt_usd(compra)}*/BTC\n"
                    f"Compraste: *{fmt_btc(btc)} BTC* ({fmt_sats(sats)} sats)\n\n"
                    f"Precio hoy: *{fmt_usd(price)}*\n"
                    f"Valor actual: *{fmt_usd(valor)}*\n"
                    f"{emoji} {etiqueta}: *{fmt_usd(ganancia)}* (*{pct:+.1f}%*)\n\n"
                    "_No es consejo financiero. El precio de BTC es volátil._")
        etiqueta = "Profit" if ganancia >= 0 else "Loss"
        return ("📈 *Profit Calculator*\n\n"
                f"You invested: *{fmt_usd(invertido)}* at *{fmt_usd(compra)}*/BTC\n"
                f"You bought: *{fmt_btc(btc)} BTC* ({fmt_sats(sats)} sats)\n\n"
                f"Price today: *{fmt_usd(price)}*\n"
                f"Current value: *{fmt_usd(valor)}*\n"
                f"{emoji} {etiqueta}: *{fmt_usd(ganancia)}* (*{pct:+.1f}%*)\n\n"
                "_Not financial advice. BTC price is volatile._")

    if tool == "retirement":
        price = await get_btc_price()
        if not price:
            return "⚠️ No pude obtener el precio. Intenta de nuevo." if lg == "es" else "⚠️ Couldn't fetch the price. Try again."
        mensual = d["mensual"]; anios = d["anios"]; g = d["crecimiento"] / 100.0
        months = anios * 12
        invertido = mensual * months
        sats = (mensual / price) * SATS_PER_BTC * months
        btc = sats / SATS_PER_BTC
        future_price = price * ((1 + g) ** anios)
        valor_futuro = btc * future_price
        if lg == "es":
            return ("🏖️ *Calculadora de Retiro*\n\n"
                    f"Ahorras *{fmt_usd(mensual)}/mes* durante *{anios:.0f} años*\n"
                    f"({months:.0f} aportes)\n\n"
                    f"Total invertido: *{fmt_usd(invertido)}*\n"
                    f"Acumularías ≈ *{fmt_sats(sats)} sats* (*{fmt_btc(btc)} BTC*)\n\n"
                    f"Si BTC crece {d['crecimiento']:.0f}%/año, en {anios:.0f} años\n"
                    f"1 BTC valdría ≈ *{fmt_usd(future_price)}*\n"
                    f"Tu cartera valdría ≈ *{fmt_usd(valor_futuro)}* 🤯\n\n"
                    "_Proyección estimada, NO es consejo financiero. BTC es volátil y nadie sabe el precio futuro._")
        return ("🏖️ *Retirement Calculator*\n\n"
                f"You save *{fmt_usd(mensual)}/month* for *{anios:.0f} years*\n"
                f"({months:.0f} contributions)\n\n"
                f"Total invested: *{fmt_usd(invertido)}*\n"
                f"You'd stack ≈ *{fmt_sats(sats)} sats* (*{fmt_btc(btc)} BTC*)\n\n"
                f"If BTC grows {d['crecimiento']:.0f}%/yr, in {anios:.0f} years\n"
                f"1 BTC would be ≈ *{fmt_usd(future_price)}*\n"
                f"Your stack would be ≈ *{fmt_usd(valor_futuro)}* 🤯\n\n"
                "_Estimated projection, NOT financial advice. BTC is volatile._")

    if tool == "utxo":
        sats = d["sats"]
        input_vb = 68  # tamaño típico de un input Native SegWit (vBytes)
        fees, _ = await get_mempool_data()
        rate = fees.get("fastestFee") if fees else None
        breakeven = sats / input_vb  # comisión (sats/vByte) a la que mover cuesta = valor
        if lg == "es":
            txt = ("🧮 *¿UTXO gastable o polvo?*\n\n"
                   f"Tu pedacito: *{fmt_sats(sats)} sats*\n"
                   f"Mover un UTXO ocupa ~{input_vb} vBytes.\n\n"
                   f"⚖️ Punto de equilibrio: si la comisión sube de *{breakeven:.1f} sats/vByte*, "
                   "mover esto cuesta más de lo que vale.\n")
            if rate is not None:
                cost = input_vb * rate
                if sats > cost:
                    txt += (f"\n🟢 *Gastable ahora.* Comisión actual: {rate} sats/vByte → "
                            f"mover cuesta ~{fmt_sats(cost)} sats (menos que su valor).")
                else:
                    txt += (f"\n🔴 *Es polvo ahora.* Comisión actual: {rate} sats/vByte → "
                            f"mover cuesta ~{fmt_sats(cost)} sats (más que su valor).")
            txt += "\n\n_Estimación con un input típico. Lo \"avanzado\" es el concepto, no el cálculo._"
            return txt
        txt = ("🧮 *UTXO spendable or dust?*\n\n"
               f"Your chunk: *{fmt_sats(sats)} sats*\n"
               f"Spending a UTXO takes ~{input_vb} vBytes.\n\n"
               f"⚖️ Break-even: above *{breakeven:.1f} sats/vByte*, moving it costs more than it's worth.\n")
        if rate is not None:
            cost = input_vb * rate
            if sats > cost:
                txt += (f"\n🟢 *Spendable now.* Current fee: {rate} sats/vByte → "
                        f"moving costs ~{fmt_sats(cost)} sats (less than its value).")
            else:
                txt += (f"\n🔴 *It's dust now.* Current fee: {rate} sats/vByte → "
                        f"moving costs ~{fmt_sats(cost)} sats (more than its value).")
        txt += "\n\n_Estimate with a typical input._"
        return txt

    return "?"


# ─── Herramienta: halving / % minado ────────────────────────────────────────────
async def halving_text(lg):
    h = await get_block_height()
    if not h:
        return "⚠️ No pude obtener la altura de bloque. Intenta de nuevo." if lg == "es" else "⚠️ Couldn't fetch block height. Try again."
    epoch = h // HALVING_INTERVAL
    reward = 50 / (2 ** epoch)
    next_h = (epoch + 1) * HALVING_INTERVAL
    blocks_left = next_h - h
    minutes_left = blocks_left * BLOCK_MINUTES
    days_left = minutes_left / 1440
    next_reward = reward / 2
    # suministro minado
    mined = 0.0
    for e in range(epoch):
        mined += HALVING_INTERVAL * (50 / (2 ** e))
    mined += (h - epoch * HALVING_INTERVAL) * reward
    pct = mined / 21_000_000 * 100
    if lg == "es":
        return ("⏳ *Cuenta regresiva al halving*\n\n"
                f"Bloque actual: *{h:,}*\n"
                f"Recompensa hoy: *{reward:g} BTC* por bloque\n"
                f"Próximo halving en el bloque: *{next_h:,}*\n"
                f"Faltan: *{blocks_left:,} bloques* (≈ *{days_left:.0f} días*)\n"
                f"Nueva recompensa: *{next_reward:g} BTC*\n\n"
                f"Ya se minó el *{pct:.2f}%* de los 21,000,000 ₿\n"
                f"(*{fmt_sats(mined)} BTC* en circulación)\n\n"
                "_Cada 210,000 bloques (~4 años) la emisión se reduce a la mitad._")
    return ("⏳ *Halving countdown*\n\n"
            f"Current block: *{h:,}*\n"
            f"Reward today: *{reward:g} BTC* per block\n"
            f"Next halving at block: *{next_h:,}*\n"
            f"Remaining: *{blocks_left:,} blocks* (≈ *{days_left:.0f} days*)\n"
            f"New reward: *{next_reward:g} BTC*\n\n"
            f"Already mined: *{pct:.2f}%* of 21,000,000 ₿\n"
            f"(*{fmt_sats(mined)} BTC* in circulation)\n\n"
            "_Every 210,000 blocks (~4 years) issuance halves._")


# ─── Herramienta: detector de estafas ──────────────────────────────────────────
SCAM_QUESTIONS = [
    ("¿Te piden tu frase semilla o tus claves privadas?",
     "Do they ask for your seed phrase or private keys?"),
    ("¿Te garantizan ganancias o rendimientos fijos?",
     "Do they guarantee profits or fixed returns?"),
    ("¿Te ofrecen una moneda que será 'el próximo Bitcoin'?",
     "Do they offer a coin that will be 'the next Bitcoin'?"),
    ("¿Te meten prisa o urgencia (FOMO)?",
     "Are they rushing you or creating urgency (FOMO)?"),
    ("¿Te lo ofreció un desconocido por DM o un 'regalo cripto'?",
     "Did a stranger offer it via DM or a 'crypto giveaway'?"),
    ("¿Te piden enviar bitcoin primero para 'recibir el doble'?",
     "Do they ask you to send bitcoin first to 'get double back'?"),
]


def scam_q_keyboard(lg):
    yes = "✅ Sí" if lg == "es" else "✅ Yes"
    no = "❌ No"
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(yes, callback_data="scam_yes"),
        InlineKeyboardButton(no, callback_data="scam_no"),
    ]])


async def start_scam(query, context, lg):
    context.user_data["scam"] = {"idx": 0, "score": 0}
    q = SCAM_QUESTIONS[0][0] if lg == "es" else SCAM_QUESTIONS[0][1]
    head = "🚩 *Detector de estafas* (1/6)\n\n" if lg == "es" else "🚩 *Scam detector* (1/6)\n\n"
    await edit_md(query, head + q, scam_q_keyboard(lg))
    return SCAM_QUIZ


async def scam_quiz_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data

    if data == "tools":
        title = "🧮 *Herramientas* — elige una:" if lg == "es" else "🧮 *Tools* — choose one:"
        await edit_md(query, title, tools_keyboard(lg))
        return TOOLS_MENU

    st = context.user_data.get("scam", {"idx": 0, "score": 0})
    if data == "scam_yes":
        st["score"] += 1
    st["idx"] += 1

    if st["idx"] < len(SCAM_QUESTIONS):
        q = SCAM_QUESTIONS[st["idx"]][0] if lg == "es" else SCAM_QUESTIONS[st["idx"]][1]
        head = (f"🚩 *Detector de estafas* ({st['idx']+1}/6)\n\n" if lg == "es"
                else f"🚩 *Scam detector* ({st['idx']+1}/6)\n\n")
        context.user_data["scam"] = st
        await edit_md(query, head + q, scam_q_keyboard(lg))
        return SCAM_QUIZ

    score = st["score"]
    context.user_data.pop("scam", None)
    if score == 0:
        verdict = ("🟢 *Riesgo bajo.* No vimos banderas rojas claras, pero mantén la guardia: "
                   "nunca compartas tu frase semilla."
                   if lg == "es" else
                   "🟢 *Low risk.* No clear red flags, but stay alert: never share your seed phrase.")
    elif score <= 2:
        verdict = ("🟡 *Cuidado.* Hay señales sospechosas. Verifica, no confíes. "
                   "Si algo suena demasiado bueno para ser verdad, probablemente lo es."
                   if lg == "es" else
                   "🟡 *Caution.* Some suspicious signs. Verify, don't trust.")
    else:
        verdict = ("🔴 *ALTA probabilidad de estafa.* Detente. "
                   "Nadie legítimo te pide tu frase semilla ni garantiza ganancias. "
                   "No envíes nada."
                   if lg == "es" else
                   "🔴 *HIGH scam probability.* Stop. Nobody legitimate asks for your seed phrase or guarantees profits.")
    head = "🚩 *Resultado*" if lg == "es" else "🚩 *Result*"
    extra = (f"\n\nBanderas rojas: *{score}/6*" if lg == "es" else f"\n\nRed flags: *{score}/6*")
    await edit_md(query, f"{head}{extra}\n\n{verdict}", tools_keyboard(lg))
    return TOOLS_MENU


# ─── Menú de herramientas ───────────────────────────────────────────────────────
async def tools_menu_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data

    if data == "back_main":
        return await show_main_menu(query, lg)
    if data == "tools":
        title = "🧮 *Herramientas* — elige una:" if lg == "es" else "🧮 *Tools* — choose one:"
        await edit_md(query, title, tools_keyboard(lg))
        return TOOLS_MENU
    if data == "price_now":
        price = await get_btc_price()
        await edit_md(query, price_text(lg, price), tools_keyboard(lg))
        return TOOLS_MENU
    if data == "halving":
        await edit_md(query, await halving_text(lg), tools_keyboard(lg))
        return TOOLS_MENU
    if data == "mempool":
        await edit_md(query, await mempool_text(lg), tools_keyboard(lg))
        return TOOLS_MENU
    if data == "explorer":
        msg = ("🔎 *Explorador*\n\nPega un *TXID* (64 caracteres) o una *dirección* "
               "Bitcoin (bc1.../1.../3...) y te muestro su info:"
               if lg == "es" else
               "🔎 *Explorer*\n\nPaste a *TXID* (64 chars) or a Bitcoin *address* "
               "(bc1.../1.../3...) and I'll show its info:")
        await edit_md(query, msg, tools_back_keyboard(lg))
        return EXPLORER_INPUT
    if data == "addrtype":
        msg = ("🏷️ *¿Qué tipo de dirección es?*\n\nPega una dirección Bitcoin "
               "(bc1.../1.../3...) y te digo qué tipo es y qué significa:"
               if lg == "es" else
               "🏷️ *What address type is it?*\n\nPaste a Bitcoin address "
               "(bc1.../1.../3...) and I'll tell you its type and what it means:")
        await edit_md(query, msg, tools_back_keyboard(lg))
        return ADDRTYPE_INPUT
    if data in TOOL_FLOWS:
        return await start_flow(query, context, data, lg)
    return TOOLS_MENU


async def cancel(update, context):
    lg = lang(context)
    msg = "Cancelado. Usa /menu para volver." if lg == "es" else "Cancelled. Use /menu to return."
    await update.message.reply_text(msg)
    return ConversationHandler.END


# ─── Diccionario Bitcoin ────────────────────────────────────────────────────────
def dict_menu_title(lg):
    return ("📖 *Diccionario Bitcoin*\n\nElige una categoría o busca un término:"
            if lg == "es" else
            "📖 *Bitcoin Dictionary*\n\nChoose a category or search a term:")


def dictionary_keyboard(lg):
    rows = []
    for c in DICT_CATS:
        label = c["btn_es"] if lg == "es" else c["btn_en"]
        rows.append([InlineKeyboardButton(label, callback_data=c["key"])])
    rows.append([InlineKeyboardButton("🔍 Buscar término" if lg == "es" else "🔍 Search term",
                                      callback_data="dict_search")])
    rows.append([InlineKeyboardButton("🔙 Menú Principal" if lg == "es" else "🔙 Main Menu",
                                      callback_data="back_main")])
    return InlineKeyboardMarkup(rows)


def dict_category_keyboard(cat, lg):
    rows = []
    for tk in cat["order"]:
        term = cat["terms"][tk]
        label = term["btn_es"] if lg == "es" else term["btn_en"]
        rows.append([InlineKeyboardButton(label, callback_data=tk)])
    rows.append([InlineKeyboardButton("🔙 Diccionario" if lg == "es" else "🔙 Dictionary",
                                      callback_data="dictionary")])
    return InlineKeyboardMarkup(rows)


def dict_term_keyboard(cat, lg):
    cat_label = cat["btn_es"] if lg == "es" else cat["btn_en"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔙 {cat_label}", callback_data=cat["key"])],
        [InlineKeyboardButton("📖 Diccionario" if lg == "es" else "📖 Dictionary", callback_data="dictionary"),
         InlineKeyboardButton("🔍 Buscar" if lg == "es" else "🔍 Search", callback_data="dict_search")],
    ])


def dict_search_results_keyboard(keys, lg):
    rows = []
    for tk in keys[:12]:
        cat = TERM_TO_CAT[tk]
        term = cat["terms"][tk]
        label = term["btn_es"] if lg == "es" else term["btn_en"]
        rows.append([InlineKeyboardButton(label, callback_data=tk)])
    rows.append([InlineKeyboardButton("🔍 Buscar otro" if lg == "es" else "🔍 Search again", callback_data="dict_search"),
                 InlineKeyboardButton("📖 Diccionario" if lg == "es" else "📖 Dictionary", callback_data="dictionary")])
    return InlineKeyboardMarkup(rows)


def search_terms(qtext):
    q = qtext.strip().lower()
    if not q:
        return []
    starts, contains = [], []
    for tk, cat in TERM_TO_CAT.items():
        term = cat["terms"][tk]
        # nombre sin emojis: quita el primer token si es un emoji/símbolo
        name_es = term["btn_es"].lower()
        name_en = term["btn_en"].lower()
        haystacks = [name_es, name_en, tk.replace("_", " ")]
        if any(h.lstrip("🔸🔑⚡🔐🟠📖🔢🟧⏳🚩💵📚📖🕶️🏛️🏦⛏️🧠🌎🟠 ").startswith(q) for h in haystacks):
            starts.append(tk)
        elif any(q in h for h in haystacks):
            contains.append(tk)
    seen, result = set(), []
    for tk in starts + contains:
        if tk not in seen:
            seen.add(tk); result.append(tk)
    return result


async def show_term(query, lg, tk):
    cat = TERM_TO_CAT[tk]
    text = cat["terms"][tk][lg]
    await edit_md(query, text, dict_term_keyboard(cat, lg))
    return DICT_CAT


async def dictionary_menu_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data
    if data == "back_main":
        return await show_main_menu(query, lg)
    if data == "dictionary":
        await edit_md(query, dict_menu_title(lg), dictionary_keyboard(lg))
        return DICT_MENU
    if data == "dict_search":
        msg = ("🔍 Escribe el término que buscas (ej: taproot, seed, halving):"
               if lg == "es" else "🔍 Type the term you're looking for (e.g. taproot, seed, halving):")
        back = InlineKeyboardMarkup([[InlineKeyboardButton(
            "🔙 Diccionario" if lg == "es" else "🔙 Dictionary", callback_data="dictionary")]])
        await edit_md(query, msg, back)
        return DICT_SEARCH
    if data in DCAT_BY_KEY:
        cat = DCAT_BY_KEY[data]
        label = cat["btn_es"] if lg == "es" else cat["btn_en"]
        title = (f"{label}\n\nElige un término:" if lg == "es" else f"{label}\n\nChoose a term:")
        await edit_md(query, title, dict_category_keyboard(cat, lg))
        return DICT_CAT
    return DICT_MENU


async def dict_cat_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data
    if data == "back_main":
        return await show_main_menu(query, lg)
    if data == "dictionary":
        await edit_md(query, dict_menu_title(lg), dictionary_keyboard(lg))
        return DICT_MENU
    if data == "dict_search":
        msg = ("🔍 Escribe el término que buscas (ej: taproot, seed, halving):"
               if lg == "es" else "🔍 Type the term you're looking for (e.g. taproot, seed, halving):")
        back = InlineKeyboardMarkup([[InlineKeyboardButton(
            "🔙 Diccionario" if lg == "es" else "🔙 Dictionary", callback_data="dictionary")]])
        await edit_md(query, msg, back)
        return DICT_SEARCH
    if data in DCAT_BY_KEY:
        cat = DCAT_BY_KEY[data]
        label = cat["btn_es"] if lg == "es" else cat["btn_en"]
        title = (f"{label}\n\nElige un término:" if lg == "es" else f"{label}\n\nChoose a term:")
        await edit_md(query, title, dict_category_keyboard(cat, lg))
        return DICT_CAT
    if data in TERM_TO_CAT:
        return await show_term(query, lg, data)
    return DICT_CAT


async def dict_search_input(update, context):
    lg = lang(context)
    keys = search_terms(update.message.text)
    if not keys:
        msg = ("❌ No encontré ese término. Prueba otra palabra (ej: nodo, utxo, lightning)."
               if lg == "es" else "❌ Term not found. Try another word (e.g. node, utxo, lightning).")
        back = InlineKeyboardMarkup([[InlineKeyboardButton(
            "🔙 Diccionario" if lg == "es" else "🔙 Dictionary", callback_data="dictionary")]])
        await reply_md(update, msg, back)
        return DICT_SEARCH
    if len(keys) == 1:
        tk = keys[0]
        cat = TERM_TO_CAT[tk]
        await reply_md(update, cat["terms"][tk][lg], dict_term_keyboard(cat, lg))
        return DICT_CAT
    head = (f"🔍 Encontré {len(keys)} resultados:" if lg == "es" else f"🔍 Found {len(keys)} results:")
    await reply_md(update, head, dict_search_results_keyboard(keys, lg))
    return DICT_CAT


# ─── Explorador BIP39 ───────────────────────────────────────────────────────────
def bip39_menu_text(lg):
    if lg == "es":
        return ("🔤 *Lista BIP39* — las 2048 palabras\n\n"
                "Es el estándar que convierte tu semilla en 12 o 24 palabras.\n\n"
                "⚠️ Esta lista es pública y sirve para *aprender*. "
                "NUNCA generes tu frase semilla a mano ni la escribas en Telegram.")
    return ("🔤 *BIP39 Wordlist* — the 2048 words\n\n"
            "It's the standard that turns your seed into 12 or 24 words.\n\n"
            "⚠️ This list is public and for *learning*. "
            "NEVER create your seed phrase by hand or type it in Telegram.")


def bip39_keyboard(lg):
    if lg == "es":
        rows = [
            [InlineKeyboardButton("ℹ️ ¿Qué es BIP39?", callback_data="bip_what")],
            [InlineKeyboardButton("🔎 Buscar palabra", callback_data="bip_word")],
            [InlineKeyboardButton("🔢 Buscar por número", callback_data="bip_num")],
            [InlineKeyboardButton("📄 Ver lista", callback_data="bip_page_1")],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="back_main")],
        ]
    else:
        rows = [
            [InlineKeyboardButton("ℹ️ What is BIP39?", callback_data="bip_what")],
            [InlineKeyboardButton("🔎 Search word", callback_data="bip_word")],
            [InlineKeyboardButton("🔢 Search by number", callback_data="bip_num")],
            [InlineKeyboardButton("📄 View list", callback_data="bip_page_1")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")],
        ]
    return InlineKeyboardMarkup(rows)


def bip39_what_text(lg):
    if lg == "es":
        return ("ℹ️ *¿Qué es BIP39?*\n\n"
                "BIP39 (_Bitcoin Improvement Proposal 39_) convierte un número aleatorio "
                "(_entropy_) en una frase de 12 o 24 palabras fáciles de anotar: tu *frase semilla*.\n\n"
                "📊 *Datos rápidos:*\n"
                "• Publicado en 2013\n"
                "• Lista fija de 2048 palabras en inglés\n"
                "• Cada palabra representa 11 bits de información\n"
                "• Puedes añadir una _passphrase_ extra\n\n"
                "🔗 Relacionado: Seed Phrase · BIP32 · Passphrase · Entropy")
    return ("ℹ️ *What is BIP39?*\n\n"
            "BIP39 (_Bitcoin Improvement Proposal 39_) turns a random number (_entropy_) "
            "into a 12 or 24 word phrase that's easy to write down: your *seed phrase*.\n\n"
            "📊 *Quick facts:*\n"
            "• Published in 2013\n"
            "• Fixed list of 2048 English words\n"
            "• Each word encodes 11 bits of information\n"
            "• You can add an extra _passphrase_\n\n"
            "🔗 Related: Seed Phrase · BIP32 · Passphrase · Entropy")


def bip39_page_text(page, lg):
    total = len(BIP39_WORDS)
    start = (page - 1) * BIP39_PER_PAGE
    end = min(start + BIP39_PER_PAGE, total)
    head = (f"📄 *Lista BIP39* — palabras {start+1}–{end} de {total}  (pág. {page}/{BIP39_PAGES})\n\n"
            if lg == "es" else
            f"📄 *BIP39 Wordlist* — words {start+1}–{end} of {total}  (page {page}/{BIP39_PAGES})\n\n")
    lines = [f"{i+1}. {BIP39_WORDS[i]}" for i in range(start, end)]
    return head + "\n".join(lines)


def bip39_page_keyboard(page, lg):
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("◀️", callback_data=f"bip_page_{page-1}"))
    if page < BIP39_PAGES:
        nav.append(InlineKeyboardButton("▶️", callback_data=f"bip_page_{page+1}"))
    rows = []
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton("🔙 BIP39", callback_data="bip39"),
                 InlineKeyboardButton("🔙 Menú" if lg == "es" else "🔙 Menu", callback_data="back_main")])
    return InlineKeyboardMarkup(rows)


def bip39_back_keyboard(lg):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BIP39", callback_data="bip39")]])


async def bip39_menu_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data
    if data == "back_main":
        return await show_main_menu(query, lg)
    if data == "bip39":
        await edit_md(query, bip39_menu_text(lg), bip39_keyboard(lg))
        return BIP39_MENU
    if data == "bip_what":
        await edit_md(query, bip39_what_text(lg), bip39_back_keyboard(lg))
        return BIP39_MENU
    if data == "bip_word":
        context.user_data["bip_mode"] = "word"
        msg = ("🔎 Escribe una palabra en inglés para ver si está en la lista BIP39 (ej: abandon):"
               if lg == "es" else "🔎 Type an English word to check if it's in the BIP39 list (e.g. abandon):")
        await edit_md(query, msg, bip39_back_keyboard(lg))
        return BIP39_INPUT
    if data == "bip_num":
        context.user_data["bip_mode"] = "num"
        msg = ("🔢 Escribe un número del 1 al 2048 para ver su palabra:"
               if lg == "es" else "🔢 Type a number from 1 to 2048 to see its word:")
        await edit_md(query, msg, bip39_back_keyboard(lg))
        return BIP39_INPUT
    if data.startswith("bip_page_"):
        try:
            page = int(data.rsplit("_", 1)[1])
        except ValueError:
            page = 1
        page = max(1, min(page, BIP39_PAGES))
        await edit_md(query, bip39_page_text(page, lg), bip39_page_keyboard(page, lg))
        return BIP39_MENU
    return BIP39_MENU


async def bip39_input(update, context):
    lg = lang(context)
    mode = context.user_data.get("bip_mode", "word")
    txt = update.message.text.strip()
    if mode == "word":
        w = txt.lower()
        if w in BIP39_SET:
            idx = BIP39_SET[w]
            msg = (f"✅ *{w}* SÍ está en la lista BIP39.\nEs la palabra *#{idx}* de 2048."
                   if lg == "es" else
                   f"✅ *{w}* IS in the BIP39 list.\nIt's word *#{idx}* of 2048.")
        else:
            msg = (f"❌ *{w}* no está en la lista BIP39.\nLas palabras BIP39 son en inglés y específicas."
                   if lg == "es" else
                   f"❌ *{w}* is not in the BIP39 list.\nBIP39 words are specific English words.")
        await reply_md(update, msg, bip39_keyboard(lg))
        return BIP39_MENU
    # mode num
    cleaned = txt.replace(",", "").replace(".", "")
    if not cleaned.isdigit():
        msg = "❌ Escribe un número del 1 al 2048." if lg == "es" else "❌ Type a number from 1 to 2048."
        await reply_md(update, msg, bip39_back_keyboard(lg))
        return BIP39_INPUT
    n = int(cleaned)
    if 1 <= n <= len(BIP39_WORDS):
        word = BIP39_WORDS[n - 1]
        msg = (f"🔢 La palabra *#{n}* de la lista BIP39 es:\n\n*{word}*"
               if lg == "es" else f"🔢 Word *#{n}* of the BIP39 list is:\n\n*{word}*")
        await reply_md(update, msg, bip39_keyboard(lg))
        return BIP39_MENU
    msg = "❌ Debe ser un número del 1 al 2048." if lg == "es" else "❌ It must be a number from 1 to 2048."
    await reply_md(update, msg, bip39_back_keyboard(lg))
    return BIP39_INPUT


# ─── Quiz Bitcoin ───────────────────────────────────────────────────────────────
QUIZ_LEN = 5


def quiz_q_text(qidx, i, n, lg):
    q = content_quiz.QUESTIONS[qidx]
    head = (f"🧠 *Quiz Bitcoin* ({i+1}/{n})\n\n" if lg == "es"
            else f"🧠 *Bitcoin Quiz* ({i+1}/{n})\n\n")
    return head + (q["q_es"] if lg == "es" else q["q_en"])


def quiz_options_keyboard(q, lg):
    opts = q["options_es"] if lg == "es" else q["options_en"]
    letters = "ABCD"
    rows = [[InlineKeyboardButton(f"{letters[i]}) {opts[i]}", callback_data=f"quiz_ans_{i}")]
            for i in range(len(opts))]
    rows.append([InlineKeyboardButton("🔙 Menú" if lg == "es" else "🔙 Menu", callback_data="back_main")])
    return InlineKeyboardMarkup(rows)


async def start_quiz(query, context, lg):
    n = min(QUIZ_LEN, len(content_quiz.QUESTIONS))
    order = random.sample(range(len(content_quiz.QUESTIONS)), n)
    context.user_data["quiz"] = {"order": order, "i": 0, "score": 0}
    q = content_quiz.QUESTIONS[order[0]]
    await edit_md(query, quiz_q_text(order[0], 0, n, lg), quiz_options_keyboard(q, lg))
    return QUIZ


async def quiz_callback(update, context):
    query = update.callback_query
    await query.answer()
    lg = lang(context)
    data = query.data
    if data == "back_main":
        context.user_data.pop("quiz", None)
        return await show_main_menu(query, lg)
    if data == "quiz":
        return await start_quiz(query, context, lg)
    st = context.user_data.get("quiz")
    if not st:
        return await start_quiz(query, context, lg)
    n = len(st["order"])
    letters = "ABCD"

    if data.startswith("quiz_ans_"):
        ans = int(data.rsplit("_", 1)[1])
        q = content_quiz.QUESTIONS[st["order"][st["i"]]]
        opts = q["options_es"] if lg == "es" else q["options_en"]
        exp = q["exp_es"] if lg == "es" else q["exp_en"]
        if ans == q["correct"]:
            st["score"] += 1
            head = "✅ *¡Correcto!*" if lg == "es" else "✅ *Correct!*"
        else:
            head = (f"❌ *Incorrecto.* Era *{letters[q['correct']]}) {opts[q['correct']]}*"
                    if lg == "es" else
                    f"❌ *Wrong.* It was *{letters[q['correct']]}) {opts[q['correct']]}*")
        last = st["i"] >= n - 1
        nextbtn = (("🏁 Ver resultado" if lg == "es" else "🏁 See result") if last
                   else ("Siguiente ▶️" if lg == "es" else "Next ▶️"))
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(nextbtn, callback_data="quiz_next")]])
        await edit_md(query, f"{head}\n\n_{exp}_", kb)
        return QUIZ

    if data == "quiz_next":
        st["i"] += 1
        if st["i"] >= n:
            score = st["score"]
            context.user_data.pop("quiz", None)
            if lg == "es":
                verdict = ("🏆 ¡Excelente! Eres un bitcoiner." if score == n else
                           "👏 ¡Bien! Sigue aprendiendo." if score >= n / 2 else
                           "📚 Sigue estudiando en la sección Educación.")
                msg = f"🧠 *Resultado:* {score}/{n}\n\n{verdict}"
            else:
                verdict = ("🏆 Excellent! You're a bitcoiner." if score == n else
                           "👏 Good! Keep learning." if score >= n / 2 else
                           "📚 Keep studying in the Education section.")
                msg = f"🧠 *Result:* {score}/{n}\n\n{verdict}"
            kb = InlineKeyboardMarkup([[
                InlineKeyboardButton("🔁 Repetir" if lg == "es" else "🔁 Retry", callback_data="quiz"),
                InlineKeyboardButton("🔙 Menú" if lg == "es" else "🔙 Menu", callback_data="back_main")]])
            await edit_md(query, msg, kb)
            return QUIZ
        qidx = st["order"][st["i"]]
        await edit_md(query, quiz_q_text(qidx, st["i"], n, lg),
                      quiz_options_keyboard(content_quiz.QUESTIONS[qidx], lg))
        return QUIZ

    return QUIZ


# ─── Explorador de transacciones / direcciones ──────────────────────────────────
async def explorer_input(update, context):
    lg = lang(context)
    q = update.message.text.strip()
    if re.fullmatch(r"[0-9a-fA-F]{64}", q):
        text = await lookup_tx(q, lg)
    elif re.fullmatch(r"(bc1[a-z0-9]{8,87}|[13][a-km-zA-HJ-NP-Z1-9]{25,39})", q):
        text = await lookup_address(q, lg)
    else:
        text = ("❌ No reconozco eso. Pega un *TXID* (64 caracteres) o una *dirección* "
                "(bc1.../1.../3...)." if lg == "es" else
                "❌ Not recognized. Paste a *TXID* (64 chars) or an *address* (bc1.../1.../3...).")
        await reply_md(update, text, tools_back_keyboard(lg))
        return EXPLORER_INPUT
    await reply_md(update, text, tools_keyboard(lg))
    return TOOLS_MENU


async def lookup_tx(txid, lg):
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"https://mempool.space/api/tx/{txid}")
            if r.status_code == 404:
                return "❌ No encontré esa transacción." if lg == "es" else "❌ Transaction not found."
            r.raise_for_status()
            d = r.json()
    except Exception:
        return "⚠️ Error consultando la red. Intenta de nuevo." if lg == "es" else "⚠️ Network error. Try again."
    st = d.get("status", {})
    fee = d.get("fee", 0)
    vsize = d.get("vsize") or d.get("size") or 1
    total_out = sum(v.get("value", 0) for v in d.get("vout", []))
    feerate = fee / vsize if vsize else 0
    if st.get("confirmed"):
        bh = st.get("block_height")
        tip = await get_block_height()
        confs = (tip - bh + 1) if (tip and bh) else "?"
        estado_es = f"🟢 Confirmada ({confs} confirmaciones)\nBloque: {bh:,}"
        estado_en = f"🟢 Confirmed ({confs} confirmations)\nBlock: {bh:,}"
    else:
        estado_es = "🟡 Pendiente (en el mempool)"
        estado_en = "🟡 Pending (in the mempool)"
    if lg == "es":
        return ("🔎 *Transacción*\n\n"
                f"{estado_es}\n\n"
                f"💰 Monto total: *{fmt_sats(total_out)} sats* ({fmt_btc(total_out/SATS_PER_BTC)} BTC)\n"
                f"💸 Comisión: *{fmt_sats(fee)} sats* ({feerate:.1f} sats/vByte)\n"
                f"📏 Tamaño: {vsize:,} vBytes\n\n_Datos de mempool.space._")
    return ("🔎 *Transaction*\n\n"
            f"{estado_en}\n\n"
            f"💰 Total amount: *{fmt_sats(total_out)} sats* ({fmt_btc(total_out/SATS_PER_BTC)} BTC)\n"
            f"💸 Fee: *{fmt_sats(fee)} sats* ({feerate:.1f} sats/vByte)\n"
            f"📏 Size: {vsize:,} vBytes\n\n_Data from mempool.space._")


async def lookup_address(addr, lg):
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"https://mempool.space/api/address/{addr}")
            if r.status_code in (400, 404):
                return "❌ Dirección no válida o sin datos." if lg == "es" else "❌ Invalid address or no data."
            r.raise_for_status()
            d = r.json()
    except Exception:
        return "⚠️ Error consultando la red. Intenta de nuevo." if lg == "es" else "⚠️ Network error. Try again."
    cs = d.get("chain_stats", {})
    ms = d.get("mempool_stats", {})
    funded = cs.get("funded_txo_sum", 0) + ms.get("funded_txo_sum", 0)
    spent = cs.get("spent_txo_sum", 0) + ms.get("spent_txo_sum", 0)
    balance = funded - spent
    txcount = cs.get("tx_count", 0) + ms.get("tx_count", 0)
    tkey = addr_utils.detect_address_type(addr)
    tline = (f"🏷️ Tipo: *{addr_utils.addr_type_short(tkey, lg)}*\n" if tkey else "")
    if lg == "es":
        return ("🔎 *Dirección*\n\n"
                f"{tline}"
                f"💰 Saldo: *{fmt_sats(balance)} sats* ({fmt_btc(balance/SATS_PER_BTC)} BTC)\n"
                f"📥 Recibido total: {fmt_sats(funded)} sats\n"
                f"📤 Enviado total: {fmt_sats(spent)} sats\n"
                f"🔁 Transacciones: {txcount:,}\n\n_Datos de mempool.space._")
    return ("🔎 *Address*\n\n"
            f"{tline}"
            f"💰 Balance: *{fmt_sats(balance)} sats* ({fmt_btc(balance/SATS_PER_BTC)} BTC)\n"
            f"📥 Total received: {fmt_sats(funded)} sats\n"
            f"📤 Total sent: {fmt_sats(spent)} sats\n"
            f"🔁 Transactions: {txcount:,}\n\n_Data from mempool.space._")


async def addrtype_input(update, context):
    lg = lang(context)
    addr = update.message.text.strip()
    key = addr_utils.detect_address_type(addr)
    if not key:
        msg = ("❌ Esa no parece una dirección Bitcoin válida. Revisa que esté bien "
               "copiada (bc1.../1.../3...)." if lg == "es" else
               "❌ That doesn't look like a valid Bitcoin address. Check it's copied "
               "correctly (bc1.../1.../3...).")
        await reply_md(update, msg, tools_back_keyboard(lg))
        return ADDRTYPE_INPUT
    header = "✅ *Dirección válida*\n\n" if lg == "es" else "✅ *Valid address*\n\n"
    await reply_md(update, header + addr_utils.addr_type_card(key, lg), tools_keyboard(lg))
    return TOOLS_MENU


# ─── Donaciones (deriva dirección nueva desde la xpub pública) ───────────────────
def derive_donation_address(index):
    node = Bip32Slip10Secp256k1.FromExtendedKey(DONATION_XPUB)
    pk = node.DerivePath(f"0/{index}").PublicKey().KeyObject()
    return P2WPKHAddr.EncodeKey(pk, hrp="bc", wit_ver=0)


def next_donation_address():
    global _donation_counter
    idx = _donation_counter % DONATION_POOL
    _donation_counter += 1
    return derive_donation_address(idx)


def make_qr_png(data):
    img = qrcode.make(data)
    bio = io.BytesIO()
    bio.name = "donacion.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio


def donation_caption(lg, addr):
    if lg == "es":
        return ("🧡 *Apoya SatoshiIntel*\n\n"
                "Escanea este QR con tu wallet para donar en Bitcoin (on-chain), "
                "o copia la dirección:\n\n"
                f"`{addr}`\n\n"
                "Cada donación usa una dirección distinta para tu privacidad. "
                "¡Gracias por apoyar el proyecto! 🟠\n\n"
                "_No confíes, verifica._")
    return ("🧡 *Support SatoshiIntel*\n\n"
            "Scan this QR with your wallet to donate in Bitcoin (on-chain), "
            "or copy the address:\n\n"
            f"`{addr}`\n\n"
            "Each donation uses a different address for your privacy. "
            "Thanks for supporting the project! 🟠\n\n"
            "_Don't trust, verify._")


async def send_donation(query, lg):
    if not DONATION_XPUB:
        msg = ("🧡 Las donaciones aún no están configuradas. Vuelve pronto."
               if lg == "es" else "🧡 Donations aren't set up yet. Check back soon.")
        await edit_md(query, msg, main_menu_keyboard(lg))
        return MAIN_MENU
    try:
        addr = next_donation_address()
        qr = make_qr_png(f"bitcoin:{addr}")
    except Exception as e:
        logger.warning("donación: %s", e)
        msg = ("⚠️ No pude generar la dirección. Intenta de nuevo."
               if lg == "es" else "⚠️ Couldn't generate the address. Try again.")
        await edit_md(query, msg, main_menu_keyboard(lg))
        return MAIN_MENU
    try:
        await query.message.reply_photo(photo=qr, caption=donation_caption(lg, addr), parse_mode="Markdown")
    except Exception:
        await query.message.reply_text(donation_caption(lg, addr), parse_mode="Markdown")
    await query.message.reply_text(main_title(lg), parse_mode="Markdown", reply_markup=main_menu_keyboard(lg))
    return MAIN_MENU


# ─── Comandos de atajo ──────────────────────────────────────────────────────────
async def diccionario_command(update, context):
    lg = lang(context)
    await reply_md(update, dict_menu_title(lg), dictionary_keyboard(lg))
    return DICT_MENU


async def bip39_command(update, context):
    lg = lang(context)
    await reply_md(update, bip39_menu_text(lg), bip39_keyboard(lg))
    return BIP39_MENU


async def quiz_command(update, context):
    lg = lang(context)
    n = min(QUIZ_LEN, len(content_quiz.QUESTIONS))
    order = random.sample(range(len(content_quiz.QUESTIONS)), n)
    context.user_data["quiz"] = {"order": order, "i": 0, "score": 0}
    q = content_quiz.QUESTIONS[order[0]]
    await reply_md(update, quiz_q_text(order[0], 0, n, lg), quiz_options_keyboard(q, lg))
    return QUIZ


async def herramientas_command(update, context):
    lg = lang(context)
    title = "🧮 *Herramientas* — elige una:" if lg == "es" else "🧮 *Tools* — choose one:"
    await reply_md(update, title, tools_keyboard(lg))
    return TOOLS_MENU


async def educacion_command(update, context):
    lg = lang(context)
    title = "📚 *Educación* — elige una categoría:" if lg == "es" else "📚 *Education* — choose a category:"
    await reply_md(update, title, education_keyboard(lg))
    return EDU_MENU


# ─── Menú de comandos de Telegram (set_my_commands) ─────────────────────────────
async def post_init(app):
    es_cmds = [
        BotCommand("start", "Iniciar / elegir idioma"),
        BotCommand("menu", "Menú principal"),
        BotCommand("herramientas", "Calculadoras y herramientas"),
        BotCommand("educacion", "Aprende sobre Bitcoin"),
        BotCommand("diccionario", "Diccionario Bitcoin"),
        BotCommand("quiz", "Pon a prueba lo que sabes"),
        BotCommand("bip39", "Lista BIP39 (2048 palabras)"),
        BotCommand("precio", "Precio de Bitcoin ahora"),
        BotCommand("idioma", "Cambiar idioma"),
    ]
    en_cmds = [
        BotCommand("start", "Start / choose language"),
        BotCommand("menu", "Main menu"),
        BotCommand("herramientas", "Calculators and tools"),
        BotCommand("educacion", "Learn about Bitcoin"),
        BotCommand("diccionario", "Bitcoin dictionary"),
        BotCommand("quiz", "Test what you know"),
        BotCommand("bip39", "BIP39 wordlist (2048 words)"),
        BotCommand("precio", "Bitcoin price now"),
        BotCommand("idioma", "Change language"),
    ]
    await app.bot.set_my_commands(es_cmds)
    await app.bot.set_my_commands(en_cmds, language_code="en")
    # "About" del perfil (short description, máx 120 caracteres)
    try:
        await app.bot.set_my_short_description(
            "₿ Creado para los que amamos Bitcoin. Educación y herramientas para volverte soberano. No confíes, verifica.")
        await app.bot.set_my_short_description(
            "₿ Built for those who love Bitcoin. Education and tools to become sovereign. Don't trust, verify.",
            language_code="en")
    except Exception as e:
        logger.warning("No pude fijar el About: %s", e)
    logger.info("✅ Menú de comandos y About configurados en Telegram.")


# ─── main ───────────────────────────────────────────────────────────────────────
def main():
    if not TOKEN:
        raise SystemExit(
            "\n⚠️  Falta el token. Pon TELEGRAM_BOT_TOKEN en un archivo .env\n"
            "   (local) o como variable de entorno (Railway).\n"
            "   Ejemplo .env:  TELEGRAM_BOT_TOKEN=123456:ABC...\n"
        )

    app = Application.builder().token(TOKEN).post_init(post_init).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("menu", menu_command),
            CommandHandler("idioma", idioma_command),
            CommandHandler("language", idioma_command),
            CommandHandler("precio", precio_command),
            CommandHandler("price", precio_command),
            CommandHandler("diccionario", diccionario_command),
            CommandHandler("dictionary", diccionario_command),
            CommandHandler("bip39", bip39_command),
            CommandHandler("quiz", quiz_command),
            CommandHandler("herramientas", herramientas_command),
            CommandHandler("tools", herramientas_command),
            CommandHandler("educacion", educacion_command),
            CommandHandler("education", educacion_command),
        ],
        states={
            LANG_SELECT: [CallbackQueryHandler(lang_select, pattern="^lang_")],
            MAIN_MENU: [CallbackQueryHandler(main_menu_callback)],
            TOOLS_MENU: [CallbackQueryHandler(tools_menu_callback)],
            EDU_MENU: [CallbackQueryHandler(education_menu_callback)],
            EDU_CAT: [CallbackQueryHandler(edu_cat_callback)],
            TOOL_INPUT: [
                CallbackQueryHandler(tools_menu_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, tool_input),
            ],
            SCAM_QUIZ: [CallbackQueryHandler(scam_quiz_callback)],
            DICT_MENU: [CallbackQueryHandler(dictionary_menu_callback)],
            DICT_CAT: [CallbackQueryHandler(dict_cat_callback)],
            DICT_SEARCH: [
                CallbackQueryHandler(dict_cat_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, dict_search_input),
            ],
            BIP39_MENU: [CallbackQueryHandler(bip39_menu_callback)],
            BIP39_INPUT: [
                CallbackQueryHandler(bip39_menu_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bip39_input),
            ],
            QUIZ: [CallbackQueryHandler(quiz_callback)],
            EXPLORER_INPUT: [
                CallbackQueryHandler(tools_menu_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, explorer_input),
            ],
            ADDRTYPE_INPUT: [
                CallbackQueryHandler(tools_menu_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, addrtype_input),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("menu", menu_command)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    logger.info("🚀 Bitcoin Bot iniciado. Esperando mensajes...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
