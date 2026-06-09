CATEGORIES = [
    {
        "key": "dic_lightning",
        "btn_es": "⚡ Lightning",
        "btn_en": "⚡ Lightning",
        "order": [
            "t_ln_lightning",
            "t_ln_channel",
            "t_ln_routing",
            "t_ln_liquidity",
            "t_ln_bolt11",
            "t_ln_lnurl",
            "t_ln_address",
        ],
        "terms": {
            "t_ln_lightning": {
                "btn_es": "⚡ Lightning Network",
                "btn_en": "⚡ Lightning Network",
                "es": """⚡ *Lightning Network*

Capa rápida sobre Bitcoin para pagos instantáneos y baratos, ideal para montos pequeños.

📊 *Datos rápidos:*
• Pagos en segundos
• Comisiones mínimas
• Usa canales de pago

🎓 Nivel: Intermedio
🔗 Relacionado: Canal · Routing · Bolt11""",
                "en": """⚡ *Lightning Network*

A fast layer on top of Bitcoin for instant, cheap payments, ideal for small amounts.

📊 *Quick facts:*
• Payments in seconds
• Tiny fees
• Uses payment channels

🎓 Level: Intermediate
🔗 Related: Channel · Routing · Bolt11""",
            },
            "t_ln_channel": {
                "btn_es": "🔗 Canal",
                "btn_en": "🔗 Channel",
                "es": """🔗 *Canal de pago*

Conexión privada entre dos personas que permite enviar muchos pagos sin tocar la cadena principal.

📊 *Datos rápidos:*
• Se abre y se cierra en la cadena
• Pagos ilimitados mientras esté abierto
• Necesita fondos bloqueados

🎓 Nivel: Intermedio
🔗 Relacionado: Lightning · Liquidez · Routing""",
                "en": """🔗 *Payment channel*

A private connection between two people that lets you send many payments without touching the main chain.

📊 *Quick facts:*
• Opens and closes on chain
• Unlimited payments while open
• Needs locked funds

🎓 Level: Intermediate
🔗 Related: Lightning · Liquidity · Routing""",
            },
            "t_ln_routing": {
                "btn_es": "🧭 Routing",
                "btn_en": "🧭 Routing",
                "es": """🧭 *Routing*

Proceso que mueve tu pago de un canal a otro hasta llegar al destino, aunque no estés conectado directo.

📊 *Datos rápidos:*
• Salta de nodo en nodo
• Cobra comisiones pequeñas
• Busca la mejor ruta

🎓 Nivel: Avanzado
🔗 Relacionado: Canal · Liquidez · Lightning""",
                "en": """🧭 *Routing*

The process that moves your payment from one channel to another until it reaches the destination, even if you are not directly connected.

📊 *Quick facts:*
• Hops from node to node
• Charges small fees
• Finds the best path

🎓 Level: Advanced
🔗 Related: Channel · Liquidity · Lightning""",
            },
            "t_ln_liquidity": {
                "btn_es": "💧 Liquidez",
                "btn_en": "💧 Liquidity",
                "es": """💧 *Liquidez*

Cantidad de fondos disponibles en un canal para enviar o recibir pagos.

📊 *Datos rápidos:*
• Liquidez de salida para enviar
• Liquidez de entrada para recibir
• Se equilibra con el uso

🎓 Nivel: Avanzado
🔗 Relacionado: Canal · Routing · Lightning""",
                "en": """💧 *Liquidity*

The amount of funds available in a channel to send or receive payments.

📊 *Quick facts:*
• Outbound liquidity to send
• Inbound liquidity to receive
• Balances with use

🎓 Level: Advanced
🔗 Related: Channel · Routing · Lightning""",
            },
            "t_ln_bolt11": {
                "btn_es": "🧾 Factura Bolt11",
                "btn_en": "🧾 Bolt11 Invoice",
                "es": """🧾 *Bolt11 (Factura)*

Código que pide un pago por Lightning, con el monto y los datos del destino incluidos.

📊 *Datos rápidos:*
• Empieza con lnbc
• Suele tener un solo uso
• Puede caducar

🎓 Nivel: Intermedio
🔗 Relacionado: Lightning · LNURL · Lightning Address""",
                "en": """🧾 *Bolt11 (Invoice)*

A code that requests a Lightning payment, with the amount and destination details included.

📊 *Quick facts:*
• Starts with lnbc
• Usually single use
• Can expire

🎓 Level: Intermediate
🔗 Related: Lightning · LNURL · Lightning Address""",
            },
            "t_ln_lnurl": {
                "btn_es": "🔆 LNURL",
                "btn_en": "🔆 LNURL",
                "es": """🔆 *LNURL*

Estándar que hace Lightning más fácil, permitiendo cobrar, pagar o iniciar sesión con un solo código.

📊 *Datos rápidos:*
• Facturas reutilizables
• Sirve para retiros y login
• Mejora la experiencia

🎓 Nivel: Avanzado
🔗 Relacionado: Bolt11 · Lightning Address · Lightning""",
                "en": """🔆 *LNURL*

A standard that makes Lightning easier, letting you receive, pay or log in with a single code.

📊 *Quick facts:*
• Reusable invoices
• Works for withdrawals and login
• Better user experience

🎓 Level: Advanced
🔗 Related: Bolt11 · Lightning Address · Lightning""",
            },
            "t_ln_address": {
                "btn_es": "📧 Lightning Address",
                "btn_en": "📧 Lightning Address",
                "es": """📧 *Lightning Address*

Dirección con forma de correo, como nombre arroba dominio, para recibir pagos Lightning fácilmente.

📊 *Datos rápidos:*
• Se ve como un email
• Fácil de compartir
• Funciona sobre LNURL

🎓 Nivel: Principiante
🔗 Relacionado: LNURL · Bolt11 · Lightning""",
                "en": """📧 *Lightning Address*

An address shaped like an email, such as name at domain, to receive Lightning payments easily.

📊 *Quick facts:*
• Looks like an email
• Easy to share
• Built on LNURL

🎓 Level: Beginner
🔗 Related: LNURL · Bolt11 · Lightning""",
            },
        },
    },
    {
        "key": "dic_mineria",
        "btn_es": "⛏️ Minería",
        "btn_en": "⛏️ Mining",
        "order": [
            "t_min_mining",
            "t_min_asic",
            "t_min_hashrate",
            "t_min_sha256",
            "t_min_difficulty",
            "t_min_reward",
        ],
        "terms": {
            "t_min_mining": {
                "btn_es": "⛏️ Minería",
                "btn_en": "⛏️ Mining",
                "es": """⛏️ *Minería*

Proceso donde computadoras compiten por resolver un problema y así confirmar bloques de transacciones.

📊 *Datos rápidos:*
• Asegura la red
• Crea nuevos bitcoins
• Usa mucha electricidad

🎓 Nivel: Principiante
🔗 Relacionado: ASIC · Hashrate · Recompensa""",
                "en": """⛏️ *Mining*

The process where computers compete to solve a puzzle and confirm blocks of transactions.

📊 *Quick facts:*
• Secures the network
• Creates new bitcoins
• Uses a lot of electricity

🎓 Level: Beginner
🔗 Related: ASIC · Hashrate · Block reward""",
            },
            "t_min_asic": {
                "btn_es": "🖥️ ASIC",
                "btn_en": "🖥️ ASIC",
                "es": """🖥️ *ASIC*

Máquina especializada hecha solo para minar Bitcoin, mucho más potente que una computadora normal.

📊 *Datos rápidos:*
• Muy eficiente para minar
• No sirve para otras tareas
• Consume bastante energía

🎓 Nivel: Intermedio
🔗 Relacionado: Minería · Hashrate · SHA256""",
                "en": """🖥️ *ASIC*

A specialized machine built only to mine Bitcoin, far more powerful than a normal computer.

📊 *Quick facts:*
• Very efficient at mining
• Useless for other tasks
• Consumes plenty of power

🎓 Level: Intermediate
🔗 Related: Mining · Hashrate · SHA256""",
            },
            "t_min_hashrate": {
                "btn_es": "📈 Hashrate",
                "btn_en": "📈 Hashrate",
                "es": """📈 *Hashrate*

Mide la potencia total de cálculo que protege la red; cuanto más alto, más segura es.

📊 *Datos rápidos:*
• Cuenta intentos por segundo
• Más hashrate, más seguridad
• Suma de todos los mineros

🎓 Nivel: Intermedio
🔗 Relacionado: Minería · ASIC · Dificultad""",
                "en": """📈 *Hashrate*

Measures the total computing power protecting the network; the higher it is, the more secure it is.

📊 *Quick facts:*
• Counts attempts per second
• More hashrate, more security
• Sum of all miners

🎓 Level: Intermediate
🔗 Related: Mining · ASIC · Difficulty""",
            },
            "t_min_sha256": {
                "btn_es": "🔐 SHA256",
                "btn_en": "🔐 SHA256",
                "es": """🔐 *SHA256*

Función matemática que convierte cualquier dato en una huella única de longitud fija.

📊 *Datos rápidos:*
• Siempre da el mismo largo
• Imposible de revertir
• Base de la minería

🎓 Nivel: Avanzado
🔗 Relacionado: Minería · Prueba de Trabajo · Merkle Tree""",
                "en": """🔐 *SHA256*

A math function that turns any data into a unique fixed length fingerprint.

📊 *Quick facts:*
• Always same length
• Impossible to reverse
• Core of mining

🎓 Level: Advanced
🔗 Related: Mining · Proof of Work · Merkle Tree""",
            },
            "t_min_difficulty": {
                "btn_es": "🎚️ Ajuste de Dificultad",
                "btn_en": "🎚️ Difficulty Adjustment",
                "es": """🎚️ *Ajuste de Dificultad*

Mecanismo que sube o baja lo difícil que es minar para mantener un bloque cada diez minutos.

📊 *Datos rápidos:*
• Cambia cada 2016 bloques
• Aproximadamente cada dos semanas
• Mantiene el ritmo estable

🎓 Nivel: Avanzado
🔗 Relacionado: Hashrate · Minería · Bloque""",
                "en": """🎚️ *Difficulty Adjustment*

A mechanism that raises or lowers how hard mining is to keep one block every ten minutes.

📊 *Quick facts:*
• Changes every 2016 blocks
• Roughly every two weeks
• Keeps the pace steady

🎓 Level: Advanced
🔗 Related: Hashrate · Mining · Block""",
            },
            "t_min_reward": {
                "btn_es": "🎁 Recompensa de Bloque",
                "btn_en": "🎁 Block Reward",
                "es": """🎁 *Recompensa de Bloque*

Bitcoins nuevos que gana el minero por confirmar un bloque, más las comisiones de ese bloque.

📊 *Datos rápidos:*
• Se reduce a la mitad cada halving
• Paga a quien resuelve el bloque
• Incluye las comisiones

🎓 Nivel: Principiante
🔗 Relacionado: Minería · Bloque · Hashrate""",
                "en": """🎁 *Block Reward*

New bitcoins the miner earns for confirming a block, plus the fees in that block.

📊 *Quick facts:*
• Cut in half each halving
• Pays whoever solves the block
• Includes the fees

🎓 Level: Beginner
🔗 Related: Mining · Block · Hashrate""",
            },
        },
    },
    {
        "key": "dic_tecnico",
        "btn_es": "🛠️ Técnico",
        "btn_en": "🛠️ Technical",
        "order": [
            "t_tec_utxo",
            "t_tec_mempool",
            "t_tec_block",
            "t_tec_pow",
            "t_tec_fullnode",
            "t_tec_merkle",
            "t_tec_taproot",
            "t_tec_confirmation",
        ],
        "terms": {
            "t_tec_utxo": {
                "btn_es": "🧩 UTXO",
                "btn_en": "🧩 UTXO",
                "es": """🧩 *UTXO*

Un trozo de bitcoin que recibiste y aún no has gastado; tu saldo es la suma de todos ellos.

📊 *Datos rápidos:*
• Como billetes en tu cartera
• Se gasta completo
• El cambio crea uno nuevo

🎓 Nivel: Intermedio
🔗 Relacionado: Mempool · Bloque · Confirmación""",
                "en": """🧩 *UTXO*

A piece of bitcoin you received and have not spent yet; your balance is the sum of all of them.

📊 *Quick facts:*
• Like bills in your wallet
• Spent whole
• Change creates a new one

🎓 Level: Intermediate
🔗 Related: Mempool · Block · Confirmation""",
            },
            "t_tec_mempool": {
                "btn_es": "⏳ Mempool",
                "btn_en": "⏳ Mempool",
                "es": """⏳ *Mempool*

Sala de espera donde quedan las transacciones antes de entrar en un bloque.

📊 *Datos rápidos:*
• Las que pagan más entran antes
• Cambia de tamaño todo el tiempo
• Refleja la congestión

🎓 Nivel: Intermedio
🔗 Relacionado: Bloque · Confirmación · UTXO""",
                "en": """⏳ *Mempool*

A waiting room where transactions sit before entering a block.

📊 *Quick facts:*
• Higher fees go in first
• Size changes constantly
• Reflects congestion

🎓 Level: Intermediate
🔗 Related: Block · Confirmation · UTXO""",
            },
            "t_tec_block": {
                "btn_es": "🧱 Bloque",
                "btn_en": "🧱 Block",
                "es": """🧱 *Bloque*

Paquete de transacciones confirmadas que se agrega a la cadena, en promedio cada diez minutos.

📊 *Datos rápidos:*
• Enlazado al bloque anterior
• Tiene tamaño limitado
• Lo crea un minero

🎓 Nivel: Principiante
🔗 Relacionado: Mempool · Confirmación · Merkle Tree""",
                "en": """🧱 *Block*

A bundle of confirmed transactions added to the chain, on average every ten minutes.

📊 *Quick facts:*
• Linked to the previous block
• Has a limited size
• Created by a miner

🎓 Level: Beginner
🔗 Related: Mempool · Confirmation · Merkle Tree""",
            },
            "t_tec_pow": {
                "btn_es": "🔨 Prueba de Trabajo",
                "btn_en": "🔨 Proof of Work",
                "es": """🔨 *Prueba de Trabajo*

Sistema que exige gastar energía y cálculo para crear bloques, lo que hace la red difícil de atacar.

📊 *Datos rápidos:*
• Cuesta esfuerzo real
• Fácil de verificar
• Protege la cadena

🎓 Nivel: Avanzado
🔗 Relacionado: Minería · SHA256 · Bloque""",
                "en": """🔨 *Proof of Work*

A system that requires spending energy and computation to create blocks, making the network hard to attack.

📊 *Quick facts:*
• Costs real effort
• Easy to verify
• Protects the chain

🎓 Level: Advanced
🔗 Related: Mining · SHA256 · Block""",
            },
            "t_tec_fullnode": {
                "btn_es": "🖧 Nodo Completo",
                "btn_en": "🖧 Full Node",
                "es": """🖧 *Nodo Completo*

Computadora que guarda y verifica toda la cadena, comprobando las reglas por sí misma.

📊 *Datos rápidos:*
• No confía, verifica
• Guarda todo el historial
• Te da independencia

🎓 Nivel: Intermedio
🔗 Relacionado: Bloque · Confirmación · Prueba de Trabajo""",
                "en": """🖧 *Full Node*

A computer that stores and verifies the whole chain, checking the rules for itself.

📊 *Quick facts:*
• Does not trust, verifies
• Keeps the full history
• Gives you independence

🎓 Level: Intermediate
🔗 Related: Block · Confirmation · Proof of Work""",
            },
            "t_tec_merkle": {
                "btn_es": "🌳 Merkle Tree",
                "btn_en": "🌳 Merkle Tree",
                "es": """🌳 *Merkle Tree*

Estructura que resume todas las transacciones de un bloque en una sola huella.

📊 *Datos rápidos:*
• Permite pruebas compactas
• Detecta cualquier cambio
• Usa SHA256

🎓 Nivel: Avanzado
🔗 Relacionado: Bloque · SHA256 · Nodo Completo""",
                "en": """🌳 *Merkle Tree*

A structure that summarizes all transactions in a block into a single fingerprint.

📊 *Quick facts:*
• Enables compact proofs
• Detects any change
• Uses SHA256

🎓 Level: Advanced
🔗 Related: Block · SHA256 · Full Node""",
            },
            "t_tec_taproot": {
                "btn_es": "🌱 Taproot",
                "btn_en": "🌱 Taproot",
                "es": """🌱 *Taproot*

Mejora de Bitcoin que hace las transacciones más privadas, eficientes y baratas.

📊 *Datos rápidos:*
• Activado en 2021
• Mejora la privacidad
• Apoya contratos avanzados

🎓 Nivel: Avanzado
🔗 Relacionado: Bloque · Nodo Completo · UTXO""",
                "en": """🌱 *Taproot*

A Bitcoin upgrade that makes transactions more private, efficient and cheap.

📊 *Quick facts:*
• Activated in 2021
• Improves privacy
• Supports advanced contracts

🎓 Level: Advanced
🔗 Related: Block · Full Node · UTXO""",
            },
            "t_tec_confirmation": {
                "btn_es": "✅ Confirmación",
                "btn_en": "✅ Confirmation",
                "es": """✅ *Confirmación*

Cada bloque añadido sobre tu transacción la hace más segura y difícil de revertir.

📊 *Datos rápidos:*
• Una confirmación por bloque
• Seis suelen bastar
• Más confirmaciones, más seguridad

🎓 Nivel: Principiante
🔗 Relacionado: Bloque · Mempool · UTXO""",
                "en": """✅ *Confirmation*

Each block added on top of your transaction makes it more secure and harder to reverse.

📊 *Quick facts:*
• One confirmation per block
• Six is usually enough
• More confirmations, more security

🎓 Level: Beginner
🔗 Related: Block · Mempool · UTXO""",
            },
        },
    },
]
