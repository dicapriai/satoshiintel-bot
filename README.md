# ₿ SatoshiIntel — Bot de Bitcoin para Telegram

Academia Bitcoin + Centro de Herramientas en Telegram. Bilingüe (Español / English).

## Funciones
- 🧮 **Herramientas**: precio en vivo, conversor SAT/USD/BTC, Apila Sats (DCA), Profit, Retiro, Cuenta regresiva al halving, Mempool en vivo, detector de estafas.
- 📚 **Educación**: 22 módulos en 4 categorías (fundamentos del dinero, cómo funciona, historia y cultura, práctica y mentalidad).
- 📖 **Diccionario Bitcoin**: 90 términos en 12 categorías, con buscador.
- 🔤 **Lista BIP39**: explorador de las 2048 palabras (buscar por palabra/número, ver por páginas).
- 🧠 **Quiz**: preguntas bilingües para aprender jugando.
- 💬 **Cita del día**.

Datos en vivo gratis (sin API key): precio de **CoinGecko**, red/halving de **mempool.space**.

## Variables de entorno
| Variable | Descripción |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token del bot (de @BotFather). **Obligatoria.** |
| `ADMIN_IDS` | (Opcional) IDs de admin separados por coma. |

## Correr en local
```bash
pip install -r requirements.txt
# crea un archivo .env con: TELEGRAM_BOT_TOKEN=tu_token
python bot.py
```

## Desplegar en Railway
1. Conecta este repo de GitHub a un nuevo proyecto en Railway.
2. En **Variables**, agrega `TELEGRAM_BOT_TOKEN`.
3. Railway usa el `Procfile` (`worker: python bot.py`) para arrancarlo.

## Estructura
- `bot.py` — lógica, menús, herramientas
- `content_edu_*.py` — módulos de educación
- `content_dict_*.py` — términos del diccionario
- `content_quiz.py` — banco de preguntas del quiz
- `content_quotes.py` — citas
- `bip39_english.txt` — lista oficial BIP39 (2048 palabras)
