# ₿ Bitcoin Bot — Telegram

Bot educativo de Bitcoin con calculadora de precios en vivo (SAT ⇄ USD ⇄ BTC),
inspirado en la calculadora de Bitcoin Magazine. Bilingüe (Español / English).

## Secciones
- 🧮 **Herramientas**:
  - 💰 Precio de Bitcoin en vivo (CoinGecko)
  - 💵 Conversor USD / ⚡ SATS / ₿ BTC (en ambos sentidos)
  - 📉 Calculadora de inflación (pérdida de poder adquisitivo del fiat)
  - 🟧 Apila Sats (DCA): cuántos sats acumulas invirtiendo $X cada semana
  - ⏳ Cuenta regresiva al halving + % de los 21M ya minados (datos reales de mempool.space)
  - 🌍 Remesas vs Western Union (ahorro con Bitcoin/Lightning)
  - 🚩 Detector de estafas (cuestionario de banderas rojas)
- 📚 **Educación** — 22 módulos en 4 categorías, extraídos de 12 libros:
  - 🏛️ Fundamentos del dinero (7): qué es el dinero, escasez, los 21M, halving, inflación, preferencia temporal, oro vs BTC
  - ⚙️ Cómo funciona (6): doble gasto, nodos, llaves/llavero, minería/PoW, transacciones, blockchain/UTXO
  - 📜 Historia y cultura (4): Satoshi y el bloque génesis, historia de la criptografía, no confíes verifica, por qué Satoshi desapareció
  - 🛠️ Práctica y mentalidad (5): autocustodia, empezar con poco, Lightning, estafas/FUD, internet del dinero
- 💬 **Cita del día**: frases de los libros (Ammous, Antonopoulos, Gigi, etc.)

Precio en vivo de **CoinGecko** y altura de bloque de **mempool.space** (ambos gratis, sin API key, caché 60s).

### Archivos del proyecto
- `bot.py` — lógica, menús y herramientas
- `content_edu_a/b/c/d.py` — contenido educativo (4 categorías). Para añadir un tema, edita el dict `MODULES` y añade su clave a `ORDER`.
- `content_quotes.py` — banco de citas
- `CONTENIDO_LIBROS.md` — material crudo extraído de los libros (ideas pendientes)

---

## 1. Crear el bot en Telegram
1. Abre Telegram y busca **@BotFather**.
2. Envía `/newbot`, ponle nombre y usuario (debe terminar en `bot`).
3. Copia el **token** que te da.

## 2. Instalar y correr (local, por terminal)
```bash
cd "/Users/turyaacademy/Desktop/BITCOINBOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN='PEGA_AQUI_TU_TOKEN'
python bot.py
```
Cuando veas `🚀 Bitcoin Bot iniciado`, abre tu bot en Telegram y envía `/start`.

## Comandos
- `/start` — elegir idioma y abrir el menú
- `/menu` — menú principal
- `/precio` o `/price` — precio rápido de Bitcoin
- `/idioma` o `/language` — cambiar idioma
- `/cancel` — cancelar

---

## 3. Subir a GitHub + desplegar (cuando esté listo)
Recomendado: **Railway** (igual que TuryaCredit) o **Render**.
- En el servicio, define la variable `TELEGRAM_BOT_TOKEN`.
- Start command: `python bot.py`
- El `.gitignore` ya evita subir `.env` y secretos.
