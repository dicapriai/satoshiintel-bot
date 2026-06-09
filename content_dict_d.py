CATEGORIES = [
    {
        "key": "dic_bips",
        "btn_es": "🏛️ BIPs",
        "btn_en": "🏛️ BIPs",
        "order": [
            "t_bip_bip32",
            "t_bip_bip39",
            "t_bip_bip44",
            "t_bip_bip84",
            "t_bip_bip141",
            "t_bip_bip340",
            "t_bip_bip341",
            "t_bip_bip85",
        ],
        "terms": {
            "t_bip_bip32": {
                "btn_es": "🌳 BIP32",
                "btn_en": "🌳 BIP32",
                "es": """🌳 *BIP32*

Crea wallets jerárquicas y deterministas, donde una sola semilla genera infinitas claves organizadas como un árbol.

📊 *Datos rápidos:*
• Publicado: 2012
• Uso: Wallets HD
• Base de muchas wallets modernas

🎓 Nivel: Intermedio
🔗 Relacionado: BIP39 · BIP44 · Seed Phrase""",
                "en": """🌳 *BIP32*

Creates hierarchical deterministic wallets, where a single seed generates infinite keys organized like a tree.

📊 *Quick facts:*
• Published: 2012
• Use: HD wallets
• Base of many modern wallets

🎓 Level: Intermediate
🔗 Related: BIP39 · BIP44 · Seed Phrase""",
            },
            "t_bip_bip39": {
                "btn_es": "🔐 BIP39",
                "btn_en": "🔐 BIP39",
                "es": """🔐 *BIP39*

Estándar que convierte un número aleatorio en una frase de 12 o 24 palabras para respaldar tu wallet.

📊 *Datos rápidos:*
• Publicado: 2013
• Uso: Seed Phrase
• Compatible con casi todas las wallets

🎓 Nivel: Intermedio
🔗 Relacionado: BIP32 · BIP44 · Seed Phrase""",
                "en": """🔐 *BIP39*

A standard that turns a random number into a 12 or 24 word phrase to back up your wallet.

📊 *Quick facts:*
• Published: 2013
• Use: Seed Phrase
• Works with most wallets

🎓 Level: Intermediate
🔗 Related: BIP32 · BIP44 · Seed Phrase""",
            },
            "t_bip_bip44": {
                "btn_es": "🗂️ BIP44",
                "btn_en": "🗂️ BIP44",
                "es": """🗂️ *BIP44*

Define una estructura de rutas para que una sola semilla maneje varias monedas y cuentas de forma ordenada.

📊 *Datos rápidos:*
• Publicado: 2014
• Uso: Multi cuenta y multi moneda
• Construido sobre BIP32

🎓 Nivel: Intermedio
🔗 Relacionado: BIP32 · BIP39 · BIP84""",
                "en": """🗂️ *BIP44*

Defines a path structure so a single seed can manage several coins and accounts in an orderly way.

📊 *Quick facts:*
• Published: 2014
• Use: Multi account and multi coin
• Built on top of BIP32

🎓 Level: Intermediate
🔗 Related: BIP32 · BIP39 · BIP84""",
            },
            "t_bip_bip84": {
                "btn_es": "⚡ BIP84",
                "btn_en": "⚡ BIP84",
                "es": """⚡ *BIP84*

Define las rutas para direcciones SegWit nativas, que empiezan con bc1 y abaratan las comisiones.

📊 *Datos rápidos:*
• Publicado: 2017
• Uso: Direcciones bc1
• Comisiones más bajas

🎓 Nivel: Intermedio
🔗 Relacionado: BIP44 · BIP141 · SegWit""",
                "en": """⚡ *BIP84*

Defines the paths for native SegWit addresses, which start with bc1 and make fees cheaper.

📊 *Quick facts:*
• Published: 2017
• Use: bc1 addresses
• Lower fees

🎓 Level: Intermediate
🔗 Related: BIP44 · BIP141 · SegWit""",
            },
            "t_bip_bip141": {
                "btn_es": "🧩 BIP141",
                "btn_en": "🧩 BIP141",
                "es": """🧩 *BIP141 SegWit*

Reorganiza cómo se guardan las firmas en cada transacción, liberando espacio en el bloque y bajando comisiones.

📊 *Datos rápidos:*
• Activado: 2017
• Uso: Más capacidad por bloque
• Habilita Lightning Network

🎓 Nivel: Avanzado
🔗 Relacionado: BIP84 · Lightning · Taproot""",
                "en": """🧩 *BIP141 SegWit*

Reorganizes how signatures are stored in each transaction, freeing up block space and lowering fees.

📊 *Quick facts:*
• Activated: 2017
• Use: More capacity per block
• Enables Lightning Network

🎓 Level: Advanced
🔗 Related: BIP84 · Lightning · Taproot""",
            },
            "t_bip_bip340": {
                "btn_es": "✍️ BIP340",
                "btn_en": "✍️ BIP340",
                "es": """✍️ *BIP340 Schnorr*

Introduce las firmas Schnorr, más pequeñas y eficientes, que permiten combinar varias firmas en una sola.

📊 *Datos rápidos:*
• Activado: 2021
• Uso: Firmas eficientes
• Mejora privacidad

🎓 Nivel: Avanzado
🔗 Relacionado: BIP341 · Taproot · SegWit""",
                "en": """✍️ *BIP340 Schnorr*

Introduces Schnorr signatures, smaller and more efficient, which let several signatures combine into one.

📊 *Quick facts:*
• Activated: 2021
• Use: Efficient signatures
• Improves privacy

🎓 Level: Advanced
🔗 Related: BIP341 · Taproot · SegWit""",
            },
            "t_bip_bip341": {
                "btn_es": "🌿 BIP341",
                "btn_en": "🌿 BIP341",
                "es": """🌿 *BIP341 Taproot*

Mejora privacidad y eficiencia haciendo que transacciones simples y complejas se vean iguales en la cadena.

📊 *Datos rápidos:*
• Activado: 2021
• Uso: Privacidad y contratos
• Usa firmas Schnorr

🎓 Nivel: Avanzado
🔗 Relacionado: BIP340 · SegWit · Lightning""",
                "en": """🌿 *BIP341 Taproot*

Improves privacy and efficiency by making simple and complex transactions look the same on the chain.

📊 *Quick facts:*
• Activated: 2021
• Use: Privacy and contracts
• Uses Schnorr signatures

🎓 Level: Advanced
🔗 Related: BIP340 · SegWit · Lightning""",
            },
            "t_bip_bip85": {
                "btn_es": "🌱 BIP85",
                "btn_en": "🌱 BIP85",
                "es": """🌱 *BIP85*

Permite derivar muchas seed phrases hijas a partir de una sola semilla maestra, como un generador de respaldos.

📊 *Datos rápidos:*
• Publicado: 2020
• Uso: Múltiples wallets de una semilla
• Útil para organizar fondos

🎓 Nivel: Avanzado
🔗 Relacionado: BIP32 · BIP39 · Seed Phrase""",
                "en": """🌱 *BIP85*

Lets you derive many child seed phrases from a single master seed, like a backup generator.

📊 *Quick facts:*
• Published: 2020
• Use: Multiple wallets from one seed
• Handy to organize funds

🎓 Level: Advanced
🔗 Related: BIP32 · BIP39 · Seed Phrase""",
            },
        },
    },
    {
        "key": "dic_mercado",
        "btn_es": "📈 Mercado",
        "btn_en": "📈 Market",
        "order": [
            "t_mkt_bull",
            "t_mkt_bear",
            "t_mkt_ath",
            "t_mkt_atl",
            "t_mkt_etf",
            "t_mkt_spot_etf",
            "t_mkt_funding",
            "t_mkt_liquidation",
        ],
        "terms": {
            "t_mkt_bull": {
                "btn_es": "🐂 Bull Market",
                "btn_en": "🐂 Bull Market",
                "es": """🐂 *Bull Market*

Periodo de mercado alcista en el que los precios suben con fuerza y predomina el optimismo.

📊 *Datos rápidos:*
• Tendencia: Al alza
• Ánimo: Optimista
• Suele atraer nuevos compradores

🎓 Nivel: Principiante
🔗 Relacionado: Bear Market · ATH · HODL""",
                "en": """🐂 *Bull Market*

A rising market period where prices climb strongly and optimism takes over.

📊 *Quick facts:*
• Trend: Upward
• Mood: Optimistic
• Often attracts new buyers

🎓 Level: Beginner
🔗 Related: Bear Market · ATH · HODL""",
            },
            "t_mkt_bear": {
                "btn_es": "🐻 Bear Market",
                "btn_en": "🐻 Bear Market",
                "es": """🐻 *Bear Market*

Periodo de mercado bajista en el que los precios caen y domina el miedo.

📊 *Datos rápidos:*
• Tendencia: A la baja
• Ánimo: Pesimista
• Buen momento para aprender

🎓 Nivel: Principiante
🔗 Relacionado: Bull Market · ATL · HODL""",
                "en": """🐻 *Bear Market*

A falling market period where prices drop and fear dominates.

📊 *Quick facts:*
• Trend: Downward
• Mood: Pessimistic
• A good time to learn

🎓 Level: Beginner
🔗 Related: Bull Market · ATL · HODL""",
            },
            "t_mkt_ath": {
                "btn_es": "🚀 ATH",
                "btn_en": "🚀 ATH",
                "es": """🚀 *ATH*

Significa All Time High, el precio más alto que Bitcoin ha alcanzado en toda su historia.

📊 *Datos rápidos:*
• Sigla: All Time High
• Marca: Máximo histórico
• Suele generar entusiasmo

🎓 Nivel: Principiante
🔗 Relacionado: ATL · Bull Market · Sound Money""",
                "en": """🚀 *ATH*

Stands for All Time High, the highest price Bitcoin has ever reached in its history.

📊 *Quick facts:*
• Acronym: All Time High
• Marks: Record high
• Often sparks excitement

🎓 Level: Beginner
🔗 Related: ATL · Bull Market · Sound Money""",
            },
            "t_mkt_atl": {
                "btn_es": "🪂 ATL",
                "btn_en": "🪂 ATL",
                "es": """🪂 *ATL*

Significa All Time Low, el precio más bajo que un activo ha registrado en toda su historia.

📊 *Datos rápidos:*
• Sigla: All Time Low
• Marca: Mínimo histórico
• Opuesto al ATH

🎓 Nivel: Principiante
🔗 Relacionado: ATH · Bear Market · Stack Sats""",
                "en": """🪂 *ATL*

Stands for All Time Low, the lowest price an asset has ever recorded in its history.

📊 *Quick facts:*
• Acronym: All Time Low
• Marks: Record low
• Opposite of ATH

🎓 Level: Beginner
🔗 Related: ATH · Bear Market · Stack Sats""",
            },
            "t_mkt_etf": {
                "btn_es": "🏦 ETF Bitcoin",
                "btn_en": "🏦 Bitcoin ETF",
                "es": """🏦 *ETF Bitcoin*

Fondo que cotiza en bolsa y permite invertir en Bitcoin desde una cuenta tradicional, sin manejar la wallet.

📊 *Datos rápidos:*
• Tipo: Producto regulado
• Acceso: Bolsa tradicional
• No tienes las llaves

🎓 Nivel: Intermedio
🔗 Relacionado: Spot ETF · Self Custody · Not Your Keys""",
                "en": """🏦 *Bitcoin ETF*

A fund traded on the stock market that lets you invest in Bitcoin from a traditional account, without handling a wallet.

📊 *Quick facts:*
• Type: Regulated product
• Access: Traditional market
• You do not hold the keys

🎓 Level: Intermediate
🔗 Related: Spot ETF · Self Custody · Not Your Keys""",
            },
            "t_mkt_spot_etf": {
                "btn_es": "🎯 Spot ETF",
                "btn_en": "🎯 Spot ETF",
                "es": """🎯 *Spot ETF*

ETF que respalda cada acción con Bitcoin real comprado al precio actual, no con contratos a futuro.

📊 *Datos rápidos:*
• Respaldo: Bitcoin real
• Aprobado en EEUU: 2024
• Sigue el precio de contado

🎓 Nivel: Intermedio
🔗 Relacionado: ETF Bitcoin · Self Custody · Sound Money""",
                "en": """🎯 *Spot ETF*

An ETF that backs each share with real Bitcoin bought at the current price, not with futures contracts.

📊 *Quick facts:*
• Backing: Real Bitcoin
• Approved in US: 2024
• Tracks the spot price

🎓 Level: Intermediate
🔗 Related: Bitcoin ETF · Self Custody · Sound Money""",
            },
            "t_mkt_funding": {
                "btn_es": "💸 Funding Rate",
                "btn_en": "💸 Funding Rate",
                "es": """💸 *Funding Rate*

Pago periódico entre traders de futuros que mantiene el precio del contrato cerca del precio real.

📊 *Datos rápidos:*
• Ámbito: Futuros perpetuos
• Señal: Sentimiento del mercado
• Puede ser positivo o negativo

🎓 Nivel: Avanzado
🔗 Relacionado: Liquidación · Bull Market · Bear Market""",
                "en": """💸 *Funding Rate*

A periodic payment between futures traders that keeps the contract price close to the real price.

📊 *Quick facts:*
• Scope: Perpetual futures
• Signal: Market sentiment
• Can be positive or negative

🎓 Level: Advanced
🔗 Related: Liquidation · Bull Market · Bear Market""",
            },
            "t_mkt_liquidation": {
                "btn_es": "💥 Liquidación",
                "btn_en": "💥 Liquidation",
                "es": """💥 *Liquidación*

Cierre forzado de una posición apalancada cuando el precio se mueve en contra y se agota la garantía.

📊 *Datos rápidos:*
• Causa: Apalancamiento
• Efecto: Pérdida de la garantía
• Común en alta volatilidad

🎓 Nivel: Avanzado
🔗 Relacionado: Funding Rate · Bear Market · Self Custody""",
                "en": """💥 *Liquidation*

The forced closing of a leveraged position when the price moves against you and the collateral runs out.

📊 *Quick facts:*
• Cause: Leverage
• Effect: Loss of collateral
• Common in high volatility

🎓 Level: Advanced
🔗 Related: Funding Rate · Bear Market · Self Custody""",
            },
        },
    },
    {
        "key": "dic_cultura",
        "btn_es": "🟠 Cultura Bitcoiner",
        "btn_en": "🟠 Bitcoiner Culture",
        "order": [
            "t_cul_orange_pill",
            "t_cul_hodl",
            "t_cul_stack_sats",
            "t_cul_self_custody",
            "t_cul_nykync",
            "t_cul_cypherpunk",
            "t_cul_sound_money",
        ],
        "terms": {
            "t_cul_orange_pill": {
                "btn_es": "🟠 Orange Pill",
                "btn_en": "🟠 Orange Pill",
                "es": """🟠 *Orange Pill*

Momento en que una persona entiende Bitcoin a fondo y cambia su forma de ver el dinero.

📊 *Datos rápidos:*
• Origen: Cultura bitcoiner
• Idea: Despertar financiero
• Se usa como verbo: orangepillear

🎓 Nivel: Principiante
🔗 Relacionado: Sound Money · Cypherpunk · HODL""",
                "en": """🟠 *Orange Pill*

The moment a person truly understands Bitcoin and changes how they see money.

📊 *Quick facts:*
• Origin: Bitcoiner culture
• Idea: Financial awakening
• Used as a verb: to orange pill

🎓 Level: Beginner
🔗 Related: Sound Money · Cypherpunk · HODL""",
            },
            "t_cul_hodl": {
                "btn_es": "💎 HODL",
                "btn_en": "💎 HODL",
                "es": """💎 *HODL*

Estrategia de guardar tus bitcoins a largo plazo sin venderlos pase lo que pase con el precio.

📊 *Datos rápidos:*
• Origen: Un error de tipeo en 2013
• Idea: Mantener con convicción
• Ignora el ruido diario

🎓 Nivel: Principiante
🔗 Relacionado: Stack Sats · Bull Market · Bear Market""",
                "en": """💎 *HODL*

The strategy of keeping your bitcoins long term without selling no matter what the price does.

📊 *Quick facts:*
• Origin: A typo back in 2013
• Idea: Hold with conviction
• Ignores daily noise

🎓 Level: Beginner
🔗 Related: Stack Sats · Bull Market · Bear Market""",
            },
            "t_cul_stack_sats": {
                "btn_es": "🧱 Stack Sats",
                "btn_en": "🧱 Stack Sats",
                "es": """🧱 *Stack Sats*

Acumular satoshis poco a poco de forma constante, sin importar el precio del momento.

📊 *Datos rápidos:*
• Unidad: Satoshi
• Hábito: Compras regulares
• Reduce el estrés del timing

🎓 Nivel: Principiante
🔗 Relacionado: HODL · Sound Money · Self Custody""",
                "en": """🧱 *Stack Sats*

Accumulating satoshis little by little in a steady way, no matter the current price.

📊 *Quick facts:*
• Unit: Satoshi
• Habit: Regular buys
• Reduces timing stress

🎓 Level: Beginner
🔗 Related: HODL · Sound Money · Self Custody""",
            },
            "t_cul_self_custody": {
                "btn_es": "🔑 Self Custody",
                "btn_en": "🔑 Self Custody",
                "es": """🔑 *Self Custody*

Guardar tú mismo las llaves de tus bitcoins, sin depender de un banco ni de un exchange.

📊 *Datos rápidos:*
• Control: Tú y solo tú
• Herramienta: Tu propia wallet
• Más responsabilidad y libertad

🎓 Nivel: Intermedio
🔗 Relacionado: Not Your Keys · Seed Phrase · Stack Sats""",
                "en": """🔑 *Self Custody*

Holding the keys to your own bitcoins yourself, without depending on a bank or an exchange.

📊 *Quick facts:*
• Control: You and only you
• Tool: Your own wallet
• More responsibility and freedom

🎓 Level: Intermediate
🔗 Related: Not Your Keys · Seed Phrase · Stack Sats""",
            },
            "t_cul_nykync": {
                "btn_es": "⚠️ Not Your Keys",
                "btn_en": "⚠️ Not Your Keys",
                "es": """⚠️ *Not Your Keys Not Your Coins*

Si no controlas las llaves de tus bitcoins, en realidad no son tuyos sino del exchange.

📊 *Datos rápidos:*
• Lección: Custodia importa
• Riesgo: Confiar en terceros
• Lema clásico bitcoiner

🎓 Nivel: Intermedio
🔗 Relacionado: Self Custody · Seed Phrase · ETF Bitcoin""",
                "en": """⚠️ *Not Your Keys Not Your Coins*

If you do not control the keys to your bitcoins, they are not really yours but the exchange's.

📊 *Quick facts:*
• Lesson: Custody matters
• Risk: Trusting third parties
• Classic bitcoiner motto

🎓 Level: Intermediate
🔗 Related: Self Custody · Seed Phrase · Bitcoin ETF""",
            },
            "t_cul_cypherpunk": {
                "btn_es": "🕶️ Cypherpunk",
                "btn_en": "🕶️ Cypherpunk",
                "es": """🕶️ *Cypherpunk*

Movimiento que usa la criptografía para defender la privacidad y la libertad individual frente al control.

📊 *Datos rápidos:*
• Origen: Años 80 y 90
• Lema: Privacidad para todos
• Inspiró el nacimiento de Bitcoin

🎓 Nivel: Intermedio
🔗 Relacionado: Sound Money · Self Custody · Orange Pill""",
                "en": """🕶️ *Cypherpunk*

A movement that uses cryptography to defend privacy and individual freedom against control.

📊 *Quick facts:*
• Origin: 1980s and 1990s
• Motto: Privacy for everyone
• Inspired the birth of Bitcoin

🎓 Level: Intermediate
🔗 Related: Sound Money · Self Custody · Orange Pill""",
            },
            "t_cul_sound_money": {
                "btn_es": "🪙 Sound Money",
                "btn_en": "🪙 Sound Money",
                "es": """🪙 *Sound Money*

Dinero sólido cuya oferta no puede inflarse a voluntad, por lo que conserva su valor con el tiempo.

📊 *Datos rápidos:*
• Cualidad: Escasez real
• Ejemplo: Bitcoin con 21 millones
• Resiste la inflación

🎓 Nivel: Intermedio
🔗 Relacionado: HODL · Stack Sats · Cypherpunk""",
                "en": """🪙 *Sound Money*

Hard money whose supply cannot be inflated at will, so it keeps its value over time.

📊 *Quick facts:*
• Quality: Real scarcity
• Example: Bitcoin with 21 million
• Resists inflation

🎓 Level: Intermediate
🔗 Related: HODL · Stack Sats · Cypherpunk""",
            },
        },
    },
    {
        "key": "dic_nostr",
        "btn_es": "🦩 Nostr",
        "btn_en": "🦩 Nostr",
        "order": [
            "t_nos_nostr",
            "t_nos_npub",
            "t_nos_nsec",
            "t_nos_zaps",
            "t_nos_relays",
        ],
        "terms": {
            "t_nos_nostr": {
                "btn_es": "🦩 Nostr",
                "btn_en": "🦩 Nostr",
                "es": """🦩 *Nostr*

Protocolo abierto para redes sociales sin censura, donde tu identidad y tus mensajes te pertenecen.

📊 *Datos rápidos:*
• Tipo: Protocolo abierto
• Idea: Redes sin censura
• Se integra con pagos Bitcoin

🎓 Nivel: Principiante
🔗 Relacionado: npub · Relays · Zaps""",
                "en": """🦩 *Nostr*

An open protocol for censorship resistant social networks, where your identity and messages belong to you.

📊 *Quick facts:*
• Type: Open protocol
• Idea: Censorship free networks
• Integrates with Bitcoin payments

🎓 Level: Beginner
🔗 Related: npub · Relays · Zaps""",
            },
            "t_nos_npub": {
                "btn_es": "🟢 npub",
                "btn_en": "🟢 npub",
                "es": """🟢 *npub*

Tu clave pública en Nostr, parecida a un usuario, que puedes compartir para que te encuentren.

📊 *Datos rápidos:*
• Función: Identidad pública
• Empieza por: npub
• Segura de compartir

🎓 Nivel: Principiante
🔗 Relacionado: nsec · Nostr · Relays""",
                "en": """🟢 *npub*

Your public key on Nostr, similar to a username, that you can share so others can find you.

📊 *Quick facts:*
• Role: Public identity
• Starts with: npub
• Safe to share

🎓 Level: Beginner
🔗 Related: nsec · Nostr · Relays""",
            },
            "t_nos_nsec": {
                "btn_es": "🔴 nsec",
                "btn_en": "🔴 nsec",
                "es": """🔴 *nsec*

Tu clave privada en Nostr, como una contraseña secreta que nunca debes compartir con nadie.

📊 *Datos rápidos:*
• Función: Llave secreta
• Empieza por: nsec
• Jamás la compartas

🎓 Nivel: Principiante
🔗 Relacionado: npub · Nostr · Self Custody""",
                "en": """🔴 *nsec*

Your private key on Nostr, like a secret password that you should never share with anyone.

📊 *Quick facts:*
• Role: Secret key
• Starts with: nsec
• Never share it

🎓 Level: Beginner
🔗 Related: npub · Nostr · Self Custody""",
            },
            "t_nos_zaps": {
                "btn_es": "⚡ Zaps",
                "btn_en": "⚡ Zaps",
                "es": """⚡ *Zaps*

Propinas instantáneas en satoshis que envías a otra persona en Nostr usando la red Lightning.

📊 *Datos rápidos:*
• Moneda: Satoshis
• Red: Lightning
• Premian buen contenido

🎓 Nivel: Principiante
🔗 Relacionado: Nostr · npub · Stack Sats""",
                "en": """⚡ *Zaps*

Instant tips in satoshis that you send to someone on Nostr using the Lightning network.

📊 *Quick facts:*
• Currency: Satoshis
• Network: Lightning
• Reward good content

🎓 Level: Beginner
🔗 Related: Nostr · npub · Stack Sats""",
            },
            "t_nos_relays": {
                "btn_es": "📡 Relays",
                "btn_en": "📡 Relays",
                "es": """📡 *Relays*

Servidores que reciben y reparten los mensajes de Nostr, y puedes elegir a cuáles conectarte.

📊 *Datos rápidos:*
• Función: Transmitir mensajes
• Control: Tú eliges cuáles usar
• Pueden ser públicos o privados

🎓 Nivel: Intermedio
🔗 Relacionado: Nostr · npub · Zaps""",
                "en": """📡 *Relays*

Servers that receive and spread Nostr messages, and you can choose which ones to connect to.

📊 *Quick facts:*
• Role: Relay messages
• Control: You pick which to use
• Can be public or private

🎓 Level: Intermediate
🔗 Related: Nostr · npub · Zaps""",
            },
        },
    },
]
