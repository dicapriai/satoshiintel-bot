CATEGORIES = [
    {
        "key": "dic_seguridad",
        "btn_es": "🔐 Seguridad",
        "btn_en": "🔐 Security",
        "order": [
            "t_sec_seed",
            "t_sec_passphrase",
            "t_sec_multisig",
            "t_sec_cold",
            "t_sec_hot",
            "t_sec_hardware",
            "t_sec_selfcustody",
            "t_sec_entropy",
            "t_sec_clavepublica",
            "t_sec_claveprivada",
        ],
        "terms": {
            "t_sec_seed": {
                "btn_es": "🔑 Seed Phrase",
                "btn_en": "🔑 Seed Phrase",
                "es": """🔑 *Seed Phrase (frase semilla)*

12 o 24 palabras que respaldan y recuperan tu wallet. Quien las tenga controla tus bitcoins.

📊 *Datos rápidos:*
• Estándar: BIP39
• Guárdala en papel, nunca en foto ni nube

⚠️ Nunca la compartas con nadie.

🎓 Nivel: Principiante
🔗 Relacionado: BIP39 · Passphrase · Self Custody""",
                "en": """🔑 *Seed Phrase*

12 or 24 words that back up and recover your wallet. Whoever holds them controls your bitcoins.

📊 *Quick facts:*
• Standard: BIP39
• Store on paper, never in photos or the cloud

⚠️ Never share it with anyone.

🎓 Level: Beginner
🔗 Related: BIP39 · Passphrase · Self Custody""",
            },
            "t_sec_passphrase": {
                "btn_es": "➕ Passphrase",
                "btn_en": "➕ Passphrase",
                "es": """➕ *Passphrase*

Una palabra o frase extra que se añade a tu seed para crear una wallet oculta y más segura. A veces se llama palabra 25.

📊 *Datos rápidos:*
• Suma protección a tu seed
• Si la olvidas, pierdes el acceso

⚠️ Guárdala por separado de la seed.

🎓 Nivel: Intermedio
🔗 Relacionado: Seed Phrase · BIP39 · Cold Wallet""",
                "en": """➕ *Passphrase*

An extra word or phrase added to your seed to create a hidden, more secure wallet. Sometimes called the 25th word.

📊 *Quick facts:*
• Adds protection to your seed
• Forget it and you lose access

⚠️ Store it apart from the seed.

🎓 Level: Intermediate
🔗 Related: Seed Phrase · BIP39 · Cold Wallet""",
            },
            "t_sec_multisig": {
                "btn_es": "🧩 Multisig",
                "btn_en": "🧩 Multisig",
                "es": """🧩 *Multisig (multifirma)*

Wallet que necesita varias firmas para gastar, por ejemplo 2 de 3 llaves. Si pierdes una llave, aún puedes acceder.

📊 *Datos rápidos:*
• Ejemplo común: 2 de 3
• Reparte el riesgo en varios lugares

🎓 Nivel: Intermedio
🔗 Relacionado: Self Custody · Cold Wallet · Hardware Wallet""",
                "en": """🧩 *Multisig*

A wallet that needs several signatures to spend, for example 2 of 3 keys. Lose one key and you can still access funds.

📊 *Quick facts:*
• Common setup: 2 of 3
• Spreads risk across places

🎓 Level: Intermediate
🔗 Related: Self Custody · Cold Wallet · Hardware Wallet""",
            },
            "t_sec_cold": {
                "btn_es": "🧊 Cold Wallet",
                "btn_en": "🧊 Cold Wallet",
                "es": """🧊 *Cold Wallet (almacenamiento en frío)*

Wallet cuyas llaves se guardan sin conexión a internet. Es la forma más segura de guardar bitcoin a largo plazo.

📊 *Datos rápidos:*
• Sin conexión, menos riesgo de hackeo
• Ideal para ahorros grandes

🎓 Nivel: Principiante
🔗 Relacionado: Hardware Wallet · Hot Wallet · Self Custody""",
                "en": """🧊 *Cold Wallet (cold storage)*

A wallet whose keys are kept offline. It is the safest way to store bitcoin for the long term.

📊 *Quick facts:*
• Offline means lower hack risk
• Ideal for larger savings

🎓 Level: Beginner
🔗 Related: Hardware Wallet · Hot Wallet · Self Custody""",
            },
            "t_sec_hot": {
                "btn_es": "🔥 Hot Wallet",
                "btn_en": "🔥 Hot Wallet",
                "es": """🔥 *Hot Wallet (wallet caliente)*

Wallet conectada a internet, como una app de móvil. Es cómoda para gastar pero más expuesta a ataques.

📊 *Datos rápidos:*
• Práctica para el día a día
• Guarda solo montos pequeños

⚠️ No la uses para grandes ahorros.

🎓 Nivel: Principiante
🔗 Relacionado: Cold Wallet · Self Custody · Hardware Wallet""",
                "en": """🔥 *Hot Wallet*

A wallet connected to the internet, like a phone app. Handy for spending but more exposed to attacks.

📊 *Quick facts:*
• Practical for daily use
• Keep only small amounts

⚠️ Do not use it for large savings.

🎓 Level: Beginner
🔗 Related: Cold Wallet · Self Custody · Hardware Wallet""",
            },
            "t_sec_hardware": {
                "btn_es": "📟 Hardware Wallet",
                "btn_en": "📟 Hardware Wallet",
                "es": """📟 *Hardware Wallet*

Dispositivo físico que guarda tus llaves sin conexión y firma transacciones de forma segura. Tus bitcoins quedan protegidos aunque tu computadora tenga virus.

📊 *Datos rápidos:*
• Las llaves nunca salen del aparato
• Marcas conocidas: varias disponibles

🎓 Nivel: Principiante
🔗 Relacionado: Cold Wallet · Seed Phrase · Self Custody""",
                "en": """📟 *Hardware Wallet*

A physical device that stores your keys offline and signs transactions securely. Your bitcoins stay safe even if your computer has a virus.

📊 *Quick facts:*
• Keys never leave the device
• Several trusted brands exist

🎓 Level: Beginner
🔗 Related: Cold Wallet · Seed Phrase · Self Custody""",
            },
            "t_sec_selfcustody": {
                "btn_es": "🗝️ Self Custody",
                "btn_en": "🗝️ Self Custody",
                "es": """🗝️ *Self Custody (autocustodia)*

Tú guardas tus propias llaves privadas, sin depender de un banco ni de un exchange. Eres tu propio banco.

📊 *Datos rápidos:*
• Tú controlas, tú eres responsable
• Frase clave: no tus llaves, no tus bitcoins

🎓 Nivel: Principiante
🔗 Relacionado: Seed Phrase · Cold Wallet · Hardware Wallet""",
                "en": """🗝️ *Self Custody*

You hold your own private keys, without relying on a bank or an exchange. You are your own bank.

📊 *Quick facts:*
• You control, you are responsible
• Key phrase: not your keys, not your bitcoins

🎓 Level: Beginner
🔗 Related: Seed Phrase · Cold Wallet · Hardware Wallet""",
            },
            "t_sec_entropy": {
                "btn_es": "🎲 Entropy",
                "btn_en": "🎲 Entropy",
                "es": """🎲 *Entropy (entropía)*

La aleatoriedad usada para crear tu seed. Más entropía significa una clave más difícil de adivinar.

📊 *Datos rápidos:*
• Más aleatoriedad, más seguridad
• La genera tu wallet o dados

🎓 Nivel: Avanzado
🔗 Relacionado: Seed Phrase · BIP39 · Self Custody""",
                "en": """🎲 *Entropy*

The randomness used to create your seed. More entropy means a key that is harder to guess.

📊 *Quick facts:*
• More randomness, more security
• Generated by your wallet or dice

🎓 Level: Advanced
🔗 Related: Seed Phrase · BIP39 · Self Custody""",
            },
            "t_sec_clavepublica": {
                "btn_es": "🔓 Clave Pública",
                "btn_en": "🔓 Public Key",
                "es": """🔓 *Clave Pública*

Es como tu número de cuenta: puedes compartirla sin riesgo. Sirve para que otros te envíen bitcoin, y de ella se generan tus direcciones.

📊 *Datos rápidos:*
• Se puede compartir sin peligro
• Nace de la clave privada (proceso irreversible)
• De ella salen tus direcciones

💡 Analogía: es el _buzón_, todos pueden meter cartas.

🎓 Nivel: Intermedio
🔗 Relacionado: Clave Privada · Dirección · Wallet""",
                "en": """🔓 *Public Key*

Like your account number: you can share it safely. Others use it to send you bitcoin, and your addresses are derived from it.

📊 *Quick facts:*
• Safe to share
• Derived from the private key (one-way)
• Your addresses come from it

💡 Analogy: it's the _mailbox_, anyone can drop letters in.

🎓 Level: Intermediate
🔗 Related: Private Key · Address · Wallet""",
            },
            "t_sec_claveprivada": {
                "btn_es": "🔒 Clave Privada",
                "btn_en": "🔒 Private Key",
                "es": """🔒 *Clave Privada*

El secreto que controla y firma tus bitcoins. Quien la tenga puede gastar tus fondos, así que jamás se comparte.

📊 *Datos rápidos:*
• Nunca la compartas con nadie
• Tu frase semilla la respalda
• Si la pierdes, pierdes el acceso

💡 Analogía: es la _llave del buzón_, solo tú la tienes.

⚠️ Nadie legítimo te la pedirá jamás.

🎓 Nivel: Intermedio
🔗 Relacionado: Clave Pública · Seed Phrase · Self Custody""",
                "en": """🔒 *Private Key*

The secret that controls and signs your bitcoins. Whoever holds it can spend your funds, so it is never shared.

📊 *Quick facts:*
• Never share it with anyone
• Your seed phrase backs it up
• Lose it and you lose access

💡 Analogy: it's the _mailbox key_, only you have it.

⚠️ No legitimate party will ever ask for it.

🎓 Level: Intermediate
🔗 Related: Public Key · Seed Phrase · Self Custody""",
            },
        },
    },
    {
        "key": "dic_privacidad",
        "btn_es": "🕶️ Privacidad",
        "btn_en": "🕶️ Privacy",
        "order": [
            "t_pri_coinjoin",
            "t_pri_kyc",
            "t_pri_nokyc",
            "t_pri_change",
            "t_pri_chainanalysis",
            "t_pri_payjoin",
        ],
        "terms": {
            "t_pri_coinjoin": {
                "btn_es": "🌀 CoinJoin",
                "btn_en": "🌀 CoinJoin",
                "es": """🌀 *CoinJoin*

Método donde varias personas juntan sus bitcoins en una sola transacción para dificultar el rastreo. Mejora tu privacidad.

📊 *Datos rápidos:*
• Mezcla fondos de muchos usuarios
• Rompe el rastro de origen

🎓 Nivel: Intermedio
🔗 Relacionado: PayJoin · Chain Analysis · No-KYC""",
                "en": """🌀 *CoinJoin*

A method where several people combine their bitcoins into a single transaction to make tracing harder. It improves your privacy.

📊 *Quick facts:*
• Mixes funds from many users
• Breaks the trail of origin

🎓 Level: Intermediate
🔗 Related: PayJoin · Chain Analysis · No-KYC""",
            },
            "t_pri_kyc": {
                "btn_es": "🪪 KYC",
                "btn_en": "🪪 KYC",
                "es": """🪪 *KYC (conoce a tu cliente)*

Proceso donde un exchange te pide identidad y documentos antes de operar. Vincula tu nombre a tus bitcoins.

📊 *Datos rápidos:*
• Exige ID, selfie o domicilio
• Reduce tu privacidad

⚠️ Tus datos quedan ligados a tus compras.

🎓 Nivel: Principiante
🔗 Relacionado: No-KYC · Chain Analysis · CoinJoin""",
                "en": """🪪 *KYC (know your customer)*

A process where an exchange asks for your identity and documents before trading. It links your name to your bitcoins.

📊 *Quick facts:*
• Requires ID, selfie or address
• Reduces your privacy

⚠️ Your data gets tied to your purchases.

🎓 Level: Beginner
🔗 Related: No-KYC · Chain Analysis · CoinJoin""",
            },
            "t_pri_nokyc": {
                "btn_es": "🕵️ No-KYC",
                "btn_en": "🕵️ No-KYC",
                "es": """🕵️ *No-KYC (sin identificación)*

Formas de conseguir bitcoin sin entregar tu identidad, como entre personas o cajeros sin registro. Más privacidad.

📊 *Datos rápidos:*
• No vincula tu nombre a tus monedas
• Suele tener límites de monto

🎓 Nivel: Intermedio
🔗 Relacionado: KYC · CoinJoin · Self Custody""",
                "en": """🕵️ *No-KYC*

Ways to get bitcoin without handing over your identity, such as peer to peer or no-signup ATMs. More privacy.

📊 *Quick facts:*
• Does not tie your name to coins
• Often has amount limits

🎓 Level: Intermediate
🔗 Related: KYC · CoinJoin · Self Custody""",
            },
            "t_pri_change": {
                "btn_es": "🔁 Change Address",
                "btn_en": "🔁 Change Address",
                "es": """🔁 *Change Address (dirección de cambio)*

Dirección nueva donde tu wallet devuelve el bitcoin sobrante de un pago, parecido al vuelto. Ayuda a tu privacidad.

📊 *Datos rápidos:*
• La crea tu wallet de forma automática
• Es tuya, no la pierdes

🎓 Nivel: Intermedio
🔗 Relacionado: Chain Analysis · CoinJoin · PayJoin""",
                "en": """🔁 *Change Address*

A new address where your wallet sends the leftover bitcoin from a payment, like getting change. It helps your privacy.

📊 *Quick facts:*
• Created automatically by your wallet
• It is yours, you do not lose it

🎓 Level: Intermediate
🔗 Related: Chain Analysis · CoinJoin · PayJoin""",
            },
            "t_pri_chainanalysis": {
                "btn_es": "🔎 Chain Analysis",
                "btn_en": "🔎 Chain Analysis",
                "es": """🔎 *Chain Analysis (análisis de cadena)*

Técnicas que estudian la blockchain pública para intentar rastrear quién envió o recibió bitcoins.

📊 *Datos rápidos:*
• Usa el registro público de transacciones
• Empresas la venden a bancos y gobiernos

⚠️ Por eso la privacidad importa.

🎓 Nivel: Avanzado
🔗 Relacionado: CoinJoin · PayJoin · KYC""",
                "en": """🔎 *Chain Analysis*

Techniques that study the public blockchain to try to trace who sent or received bitcoins.

📊 *Quick facts:*
• Uses the public transaction record
• Firms sell it to banks and governments

⚠️ This is why privacy matters.

🎓 Level: Advanced
🔗 Related: CoinJoin · PayJoin · KYC""",
            },
            "t_pri_payjoin": {
                "btn_es": "🤝 PayJoin",
                "btn_en": "🤝 PayJoin",
                "es": """🤝 *PayJoin*

Pago donde quien envía y quien recibe aportan fondos a la misma transacción, confundiendo al análisis de cadena.

📊 *Datos rápidos:*
• Mejora privacidad en pagos normales
• También llamado P2EP

🎓 Nivel: Avanzado
🔗 Relacionado: CoinJoin · Chain Analysis · Change Address""",
                "en": """🤝 *PayJoin*

A payment where both sender and receiver add funds to the same transaction, confusing chain analysis.

📊 *Quick facts:*
• Improves privacy in normal payments
• Also called P2EP

🎓 Level: Advanced
🔗 Related: CoinJoin · Chain Analysis · Change Address""",
            },
        },
    },
]
