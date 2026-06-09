CATEGORIES = [
    {
        "key": "dic_general",
        "btn_es": "📚 General",
        "btn_en": "📚 General",
        "order": [
            "t_gen_bitcoin",
            "t_gen_satoshi",
            "t_gen_blockchain",
            "t_gen_wallet",
            "t_gen_nodo",
            "t_gen_halving",
            "t_gen_mineria",
            "t_gen_address",
        ],
        "terms": {
            "t_gen_bitcoin": {
                "btn_es": "🔸 Bitcoin",
                "btn_en": "🔸 Bitcoin",
                "es": """🔸 *Bitcoin (BTC)*

Dinero digital descentralizado, sin bancos ni intermediarios. Su oferta máxima es de 21 millones.

📊 *Datos rápidos:*
• Símbolo: BTC
• Suministro máximo: 21,000,000
• Lanzamiento: 03/01/2009

🎓 Nivel: Principiante
🔗 Relacionado: Blockchain · Satoshi · Halving""",
                "en": """🔸 *Bitcoin (BTC)*

Decentralized digital money, no banks or middlemen. Max supply is 21 million.

📊 *Quick facts:*
• Ticker: BTC
• Max supply: 21,000,000
• Launch: 2009-01-03

🎓 Level: Beginner
🔗 Related: Blockchain · Satoshi · Halving""",
            },
            "t_gen_satoshi": {
                "btn_es": "🔸 Satoshi",
                "btn_en": "🔸 Satoshi",
                "es": """🔸 *Satoshi (SAT)*

La unidad más pequeña de Bitcoin. Un bitcoin se divide en 100 millones de satoshis.

📊 *Datos rápidos:*
• 1 BTC = 100,000,000 sats
• Símbolo: SAT
• Sirve para pagos pequeños

🎓 Nivel: Principiante
🔗 Relacionado: Bitcoin · Wallet · Address""",
                "en": """🔸 *Satoshi (SAT)*

The smallest unit of Bitcoin. One bitcoin divides into 100 million satoshis.

📊 *Quick facts:*
• 1 BTC = 100,000,000 sats
• Symbol: SAT
• Used for small payments

🎓 Level: Beginner
🔗 Related: Bitcoin · Wallet · Address""",
            },
            "t_gen_blockchain": {
                "btn_es": "🔸 Blockchain",
                "btn_en": "🔸 Blockchain",
                "es": """🔸 *Blockchain*

Un libro de cuentas público y compartido que guarda todas las transacciones en bloques enlazados. Nadie lo puede alterar.

📊 *Datos rápidos:*
• Bloque nuevo cada 10 minutos
• Es pública y verificable

🎓 Nivel: Principiante
🔗 Relacionado: Bitcoin · Nodo · Minería""",
                "en": """🔸 *Blockchain*

A public, shared ledger that stores every transaction in linked blocks. No one can alter it.

📊 *Quick facts:*
• New block every 10 minutes
• Public and verifiable

🎓 Level: Beginner
🔗 Related: Bitcoin · Node · Mining""",
            },
            "t_gen_wallet": {
                "btn_es": "🔸 Wallet",
                "btn_en": "🔸 Wallet",
                "es": """🔸 *Wallet (Billetera)*

App o dispositivo que guarda tus llaves para enviar y recibir bitcoin. Tus llaves, tus bitcoins.

📊 *Datos rápidos:*
• Tipos: caliente y fría
• Guarda llaves, no monedas

🎓 Nivel: Principiante
🔗 Relacionado: Address · Satoshi · Bitcoin""",
                "en": """🔸 *Wallet*

App or device that holds your keys to send and receive bitcoin. Your keys, your bitcoin.

📊 *Quick facts:*
• Types: hot and cold
• Stores keys, not coins

🎓 Level: Beginner
🔗 Related: Address · Satoshi · Bitcoin""",
            },
            "t_gen_nodo": {
                "btn_es": "🔸 Nodo",
                "btn_en": "🔸 Node",
                "es": """🔸 *Nodo (Node)*

Una computadora que guarda una copia de la blockchain y verifica las reglas de la red.

📊 *Datos rápidos:*
• Miles repartidos por el mundo
• Cualquiera puede correr uno

🎓 Nivel: Intermedio
🔗 Relacionado: Blockchain · Minería · Bitcoin""",
                "en": """🔸 *Node*

A computer that keeps a copy of the blockchain and verifies the network rules.

📊 *Quick facts:*
• Thousands around the world
• Anyone can run one

🎓 Level: Intermediate
🔗 Related: Blockchain · Mining · Bitcoin""",
            },
            "t_gen_halving": {
                "btn_es": "🔸 Halving",
                "btn_en": "🔸 Halving",
                "es": """🔸 *Halving*

Evento que reduce a la mitad la recompensa de los mineros. Ocurre cada 4 años aproximadamente.

📊 *Datos rápidos:*
• Cada 210,000 bloques
• Hace al BTC más escaso

🎓 Nivel: Intermedio
🔗 Relacionado: Minería · Bitcoin · Blockchain""",
                "en": """🔸 *Halving*

Event that cuts the miner reward in half. It happens roughly every 4 years.

📊 *Quick facts:*
• Every 210,000 blocks
• Makes BTC more scarce

🎓 Level: Intermediate
🔗 Related: Mining · Bitcoin · Blockchain""",
            },
            "t_gen_mineria": {
                "btn_es": "🔸 Minería",
                "btn_en": "🔸 Mining",
                "es": """🔸 *Minería (Mining)*

Proceso donde computadoras compiten por resolver un problema y así crear bloques nuevos y ganar bitcoin.

📊 *Datos rápidos:*
• Usa prueba de trabajo
• Asegura la red

🎓 Nivel: Intermedio
🔗 Relacionado: Halving · Nodo · Blockchain""",
                "en": """🔸 *Mining*

Process where computers compete to solve a puzzle, creating new blocks and earning bitcoin.

📊 *Quick facts:*
• Uses proof of work
• Secures the network

🎓 Level: Intermediate
🔗 Related: Halving · Node · Blockchain""",
            },
            "t_gen_address": {
                "btn_es": "🔸 Address",
                "btn_en": "🔸 Address",
                "es": """🔸 *Address (Dirección)*

Un código tipo dirección de correo donde recibes bitcoin. Puedes compartirla sin riesgo.

📊 *Datos rápidos:*
• Pública y segura de compartir
• Crea una nueva por pago

🎓 Nivel: Principiante
🔗 Relacionado: Wallet · Satoshi · Bitcoin""",
                "en": """🔸 *Address*

A code like an email address where you receive bitcoin. You can share it safely.

📊 *Quick facts:*
• Public and safe to share
• Use a new one per payment

🎓 Level: Beginner
🔗 Related: Wallet · Satoshi · Bitcoin""",
            },
        },
    },
    {
        "key": "dic_historico",
        "btn_es": "📖 Histórico",
        "btn_en": "📖 History",
        "order": [
            "t_his_satoshi_nakamoto",
            "t_his_whitepaper",
            "t_his_genesis_block",
            "t_his_pizza_day",
            "t_his_mtgox",
            "t_his_halvings",
        ],
        "terms": {
            "t_his_satoshi_nakamoto": {
                "btn_es": "📜 Satoshi Nakamoto",
                "btn_en": "📜 Satoshi Nakamoto",
                "es": """📜 *Satoshi Nakamoto*

El seudónimo del creador anónimo de Bitcoin. Nadie sabe quién es realmente.

📊 *Datos rápidos:*
• Activo entre 2008 y 2011
• Identidad aún desconocida

🎓 Nivel: Principiante
🔗 Relacionado: Whitepaper · Genesis Block · Bitcoin""",
                "en": """📜 *Satoshi Nakamoto*

The pseudonym of Bitcoin's anonymous creator. Nobody knows who they really are.

📊 *Quick facts:*
• Active between 2008 and 2011
• Identity still unknown

🎓 Level: Beginner
🔗 Related: Whitepaper · Genesis Block · Bitcoin""",
            },
            "t_his_whitepaper": {
                "btn_es": "📜 Whitepaper",
                "btn_en": "📜 Whitepaper",
                "es": """📜 *Whitepaper*

El documento de 9 páginas que explicó Bitcoin por primera vez, publicado por Satoshi en 2008.

📊 *Datos rápidos:*
• Publicado: 31/10/2008
• Título sobre dinero entre pares

🎓 Nivel: Principiante
🔗 Relacionado: Satoshi Nakamoto · Genesis Block · Bitcoin""",
                "en": """📜 *Whitepaper*

The 9 page document that first explained Bitcoin, published by Satoshi in 2008.

📊 *Quick facts:*
• Published: 2008-10-31
• Titled on peer to peer cash

🎓 Level: Beginner
🔗 Related: Satoshi Nakamoto · Genesis Block · Bitcoin""",
            },
            "t_his_genesis_block": {
                "btn_es": "📜 Genesis Block",
                "btn_en": "📜 Genesis Block",
                "es": """📜 *Genesis Block*

El primer bloque de la blockchain de Bitcoin, minado por Satoshi. Marca el inicio de la red.

📊 *Datos rápidos:*
• Fecha: 03/01/2009
• Es el bloque número 0

🎓 Nivel: Intermedio
🔗 Relacionado: Whitepaper · Blockchain · Satoshi Nakamoto""",
                "en": """📜 *Genesis Block*

The first block of Bitcoin's blockchain, mined by Satoshi. It marks the start of the network.

📊 *Quick facts:*
• Date: 2009-01-03
• It is block number 0

🎓 Level: Intermediate
🔗 Related: Whitepaper · Blockchain · Satoshi Nakamoto""",
            },
            "t_his_pizza_day": {
                "btn_es": "📜 Pizza Day",
                "btn_en": "📜 Pizza Day",
                "es": """📜 *Bitcoin Pizza Day*

La primera compra real con bitcoin: 2 pizzas por 10,000 BTC en 2010. Hoy se celebra cada año.

📊 *Datos rápidos:*
• Fecha: 22/05/2010
• Pagó 10,000 BTC

🎓 Nivel: Principiante
🔗 Relacionado: Bitcoin · Satoshi · Wallet""",
                "en": """📜 *Bitcoin Pizza Day*

The first real purchase with bitcoin: 2 pizzas for 10,000 BTC in 2010. Now celebrated yearly.

📊 *Quick facts:*
• Date: 2010-05-22
• Paid 10,000 BTC

🎓 Level: Beginner
🔗 Related: Bitcoin · Satoshi · Wallet""",
            },
            "t_his_mtgox": {
                "btn_es": "📜 MtGox",
                "btn_en": "📜 MtGox",
                "es": """📜 *MtGox*

Un exchange muy popular que quebró en 2014 tras perder cientos de miles de bitcoins. Una gran lección de seguridad.

📊 *Datos rápidos:*
• Quiebra: 2014
• Enseñó: no tus llaves, no tus BTC

🎓 Nivel: Intermedio
🔗 Relacionado: Wallet · Address · Bitcoin""",
                "en": """📜 *MtGox*

A very popular exchange that collapsed in 2014 after losing hundreds of thousands of bitcoins. A major security lesson.

📊 *Quick facts:*
• Collapse: 2014
• Lesson: not your keys, not your BTC

🎓 Level: Intermediate
🔗 Related: Wallet · Address · Bitcoin""",
            },
            "t_his_halvings": {
                "btn_es": "📜 Halvings",
                "btn_en": "📜 Halvings",
                "es": """📜 *Halvings*

Las fechas históricas en que la recompensa minera se redujo a la mitad, haciendo al BTC más escaso.

📊 *Datos rápidos:*
• 2012 y 2016
• 2020 y 2024

🎓 Nivel: Intermedio
🔗 Relacionado: Halving · Minería · Bitcoin""",
                "en": """📜 *Halvings*

The historic dates when the mining reward was cut in half, making BTC more scarce.

📊 *Quick facts:*
• 2012 and 2016
• 2020 and 2024

🎓 Level: Intermediate
🔗 Related: Halving · Mining · Bitcoin""",
            },
        },
    },
]
