CATEGORIES = [
    {
        "key": "dic_wallets",
        "btn_es": "👛 Wallets",
        "btn_en": "👛 Wallets",
        "order": [
            "t_wal_hot",
            "t_wal_cold",
            "t_wal_hardware",
            "t_wal_mobile",
            "t_wal_desktop",
            "t_wal_lightning",
            "t_wal_multisig",
            "t_wal_watchonly",
            "t_wal_airgapped",
            "t_wal_custodial",
            "t_wal_noncustodial",
        ],
        "terms": {
            "t_wal_hot": {
                "btn_es": "🔥 Hot Wallet",
                "btn_en": "🔥 Hot Wallet",
                "es": """🔥 *Hot Wallet (caliente)*

Wallet conectada a internet. Cómoda para el día a día y montos pequeños.

📊 *Ejemplos:*
• BlueWallet
• Phoenix
• Muun

🎓 Nivel: Principiante
🔗 Relacionado: Cold Wallet · Lightning · Self Custody""",
                "en": """🔥 *Hot Wallet*

A wallet connected to the internet. Convenient for daily use and small amounts.

📊 *Examples:*
• BlueWallet
• Phoenix
• Muun

🎓 Level: Beginner
🔗 Related: Cold Wallet · Lightning · Self Custody""",
            },
            "t_wal_cold": {
                "btn_es": "❄️ Cold Wallet",
                "btn_en": "❄️ Cold Wallet",
                "es": """❄️ *Cold Wallet (fría)*

Wallet desconectada de internet. Ideal para guardar grandes cantidades a largo plazo.

📊 _Nota:_ No es una marca, sino cualquier wallet que mantiene tus llaves offline.

🎓 Nivel: Intermedio
🔗 Relacionado: Hardware · Air Gapped · Self Custody""",
                "en": """❄️ *Cold Wallet*

A wallet kept offline. Ideal for storing large amounts long term.

📊 _Note:_ Not a brand, but any wallet that keeps your keys offline.

🎓 Level: Intermediate
🔗 Related: Hardware · Air Gapped · Self Custody""",
            },
            "t_wal_hardware": {
                "btn_es": "🔐 Hardware Wallet",
                "btn_en": "🔐 Hardware Wallet",
                "es": """🔐 *Hardware Wallet*

Dispositivo físico que guarda tus llaves offline y firma transacciones de forma segura.

📊 *Ejemplos:*
• Coldcard
• Jade
• Trezor
• Ledger

🎓 Nivel: Intermedio
🔗 Relacionado: Cold Wallet · Air Gapped · Non-Custodial""",
                "en": """🔐 *Hardware Wallet*

A physical device that stores your keys offline and signs transactions securely.

📊 *Examples:*
• Coldcard
• Jade
• Trezor
• Ledger

🎓 Level: Intermediate
🔗 Related: Cold Wallet · Air Gapped · Non-Custodial""",
            },
            "t_wal_mobile": {
                "btn_es": "📱 Mobile Wallet",
                "btn_en": "📱 Mobile Wallet",
                "es": """📱 *Mobile Wallet (móvil)*

App de wallet en tu teléfono. Práctica para pagos y uso cotidiano.

📊 *Ejemplos:*
• Phoenix
• Aqua
• Zeus

🎓 Nivel: Principiante
🔗 Relacionado: Hot Wallet · Lightning · Desktop Wallet""",
                "en": """📱 *Mobile Wallet*

A wallet app on your phone. Handy for payments and everyday use.

📊 *Examples:*
• Phoenix
• Aqua
• Zeus

🎓 Level: Beginner
🔗 Related: Hot Wallet · Lightning · Desktop Wallet""",
            },
            "t_wal_desktop": {
                "btn_es": "💻 Desktop Wallet",
                "btn_en": "💻 Desktop Wallet",
                "es": """💻 *Desktop Wallet (escritorio)*

Wallet para tu computadora, con más funciones avanzadas y control.

📊 *Ejemplos:*
• Sparrow
• Electrum

🎓 Nivel: Intermedio
🔗 Relacionado: Mobile Wallet · Multisig · Watch Only""",
                "en": """💻 *Desktop Wallet*

A wallet for your computer, with more advanced features and control.

📊 *Examples:*
• Sparrow
• Electrum

🎓 Level: Intermediate
🔗 Related: Mobile Wallet · Multisig · Watch Only""",
            },
            "t_wal_lightning": {
                "btn_es": "⚡ Lightning Wallet",
                "btn_en": "⚡ Lightning Wallet",
                "es": """⚡ *Lightning Wallet*

Wallet para pagos instantáneos y baratos por la red Lightning.

📊 *Ejemplos:*
• Phoenix
• Wallet of Satoshi
• Zeus

🎓 Nivel: Principiante
🔗 Relacionado: Hot Wallet · Mobile Wallet · Custodial""",
                "en": """⚡ *Lightning Wallet*

A wallet for instant, cheap payments over the Lightning network.

📊 *Examples:*
• Phoenix
• Wallet of Satoshi
• Zeus

🎓 Level: Beginner
🔗 Related: Hot Wallet · Mobile Wallet · Custodial""",
            },
            "t_wal_multisig": {
                "btn_es": "🔏 Multisig Wallet",
                "btn_en": "🔏 Multisig Wallet",
                "es": """🔏 *Multisig Wallet*

Necesita varias llaves para gastar (ejemplo 2 de 3). Más seguridad contra robos y errores.

📊 *Ejemplos:*
• Casa
• Nunchuk
• Sparrow

🎓 Nivel: Avanzado
🔗 Relacionado: Hardware · Self Custody · Cold Wallet""",
                "en": """🔏 *Multisig Wallet*

Requires several keys to spend (for example 2 of 3). More security against theft and mistakes.

📊 *Examples:*
• Casa
• Nunchuk
• Sparrow

🎓 Level: Advanced
🔗 Related: Hardware · Self Custody · Cold Wallet""",
            },
            "t_wal_watchonly": {
                "btn_es": "👀 Watch Only",
                "btn_en": "👀 Watch Only",
                "es": """👀 *Watch Only Wallet*

Monitorea tus fondos sin poder gastarlos, porque no contiene las llaves privadas.

📊 _Nota:_ Útil para vigilar saldos manteniendo las llaves en frío.

🎓 Nivel: Intermedio
🔗 Relacionado: Cold Wallet · Hardware · Air Gapped""",
                "en": """👀 *Watch Only Wallet*

Monitors your funds without being able to spend them, since it holds no private keys.

📊 _Note:_ Useful for tracking balances while keeping keys in cold storage.

🎓 Level: Intermediate
🔗 Related: Cold Wallet · Hardware · Air Gapped""",
            },
            "t_wal_airgapped": {
                "btn_es": "🛡️ Air Gapped",
                "btn_en": "🛡️ Air Gapped",
                "es": """🛡️ *Air Gapped Wallet*

Nunca se conecta a internet; firma vía QR o tarjeta SD. Máxima seguridad.

📊 _Nota:_ Es una forma de usar hardware wallets sin cables ni conexión.

🎓 Nivel: Avanzado
🔗 Relacionado: Hardware · Cold Wallet · Multisig""",
                "en": """🛡️ *Air Gapped Wallet*

Never connects to the internet; signs via QR or SD card. Maximum security.

📊 _Note:_ A way to use hardware wallets with no cables or connection.

🎓 Level: Advanced
🔗 Related: Hardware · Cold Wallet · Multisig""",
            },
            "t_wal_custodial": {
                "btn_es": "🏦 Custodial",
                "btn_en": "🏦 Custodial",
                "es": """🏦 *Custodial Wallet*

Un tercero controla las llaves por ti. Fácil de usar, pero dependes de la empresa.

⚠️ No controlas tus llaves (not your keys, not your coins).

📊 *Ejemplos:*
• Coinbase
• Binance
• Strike

🎓 Nivel: Principiante
🔗 Relacionado: Non-Custodial · Hot Wallet · Lightning""",
                "en": """🏦 *Custodial Wallet*

A third party controls the keys for you. Easy to use, but you depend on the company.

⚠️ You do not control your keys (not your keys, not your coins).

📊 *Examples:*
• Coinbase
• Binance
• Strike

🎓 Level: Beginner
🔗 Related: Non-Custodial · Hot Wallet · Lightning""",
            },
            "t_wal_noncustodial": {
                "btn_es": "🔑 Non-Custodial",
                "btn_en": "🔑 Non-Custodial",
                "es": """🔑 *Non-Custodial Wallet*

Tú controlas las llaves privadas. Plena soberanía sobre tus bitcoins.

📊 *Ejemplos:*
• Sparrow
• Jade
• Phoenix

🎓 Nivel: Intermedio
🔗 Relacionado: Self Custody · Hardware · Custodial""",
                "en": """🔑 *Non-Custodial Wallet*

You control the private keys. Full sovereignty over your bitcoins.

📊 *Examples:*
• Sparrow
• Jade
• Phoenix

🎓 Level: Intermediate
🔗 Related: Self Custody · Hardware · Custodial""",
            },
        },
    },
]
