CATEGORY = {
    "key": "cat_b",
    "btn_es": "⚙️ Cómo funciona",
    "btn_en": "⚙️ How it works",
}

ORDER = ["edu_b1", "edu_b2", "edu_b3", "edu_b4", "edu_b5", "edu_b6"]

MODULES = {
    "edu_b1": {
        "btn_es": "♻️ El doble gasto",
        "btn_en": "♻️ Double spending",
        "es": """*♻️ El problema del doble gasto*

El dinero físico tiene una virtud silenciosa: cuando un billete sale de tu mano, ya no lo tienes. Pero lo digital se copia con la misma facilidad que una canción o una película. Entonces, ¿qué impide enviar el mismo dinero dos veces?

Durante décadas la respuesta fue un banco. Cuando pagas, el banco revisa su libro de registro y, si ya gastaste ese saldo, lo rechaza: _"lo siento, no tienes más dinero"_. Ese árbitro central evita el doble gasto, pero te obliga a confiar en él.

La gran idea de Bitcoin fue resolver esto _sin_ banco. En lugar de un árbitro único, miles de participantes guardan una copia del mismo libro y se ponen de acuerdo sobre una sola versión de la verdad. A esto se le llama consenso.

• Sin control central, cada moneda solo puede gastarse una vez.
• Copiar un bitcoin es, en la práctica, lo mismo que falsificar dinero, y la red lo impide.""",
        "en": """*♻️ The double spending problem*

Physical money has a quiet virtue: when a bill leaves your hand, you no longer have it. But digital files copy as easily as a song or a movie. So what stops anyone from sending the same money twice?

For decades the answer was a bank. When you pay, the bank checks its ledger and, if you already spent that balance, it refuses: _"sorry, you have no more money"_. That central referee prevents double spending, but it forces you to trust it.

Bitcoin's great idea was to solve this _without_ a bank. Instead of a single referee, thousands of participants keep a copy of the same ledger and agree on one single version of the truth. This is called consensus.

• With no central control, each coin can only be spent once.
• Copying a bitcoin is, in practice, the same as counterfeiting money, and the network blocks it.""",
    },
    "edu_b2": {
        "btn_es": "🌐 Nodos descentralizados",
        "btn_en": "🌐 Decentralized nodes",
        "es": """*🌐 Descentralización y nodos*

Bitcoin no lo gestiona ninguna empresa. Lo hace funcionar una red de individuos y compañías repartidos por todo el mundo, cada uno corriendo un programa llamado _nodo_.

Un nodo guarda una copia completa del libro de registro y verifica por sí mismo cada regla: que las firmas sean válidas, que no haya doble gasto y que nadie cree bitcoins de la nada. No pide permiso a ningún jefe. Por eso se dice que todos los nodos son iguales: ninguno manda sobre los demás.

¿Y si alguien quisiera apagar Bitcoin? Tendría que apagar de decenas a cientos de miles de computadoras a la vez, muchas en lugares desconocidos. Como dice Antonopoulos, sería un esfuerzo inútil: lo único que lograría es animar a la gente a levantar nodos nuevos.

• Más nodos significan una red más difícil de censurar o detener.
• La verdad no la dicta una autoridad, la sostiene la mayoría que verifica.""",
        "en": """*🌐 Decentralization and nodes*

Bitcoin is run by no single company. It is kept alive by a network of individuals and companies spread across the world, each running a program called a _node_.

A node keeps a full copy of the ledger and checks every rule for itself: that signatures are valid, that there is no double spending and that nobody creates bitcoins out of thin air. It asks no boss for permission. That is why every node is equal: none rules over the others.

And if someone wanted to shut Bitcoin down? They would have to turn off tens to hundreds of thousands of computers at once, many in unknown places. As Antonopoulos puts it, it would be a futile effort: it would only encourage people to spin up new nodes.

• More nodes mean a network that is harder to censor or stop.
• Truth is not dictated by an authority, it is upheld by the verifying majority.""",
    },
    "edu_b3": {
        "btn_es": "🔑 La wallet es un llavero",
        "btn_en": "🔑 The wallet is a keyring",
        "es": """*🔑 Las llaves son un llavero*

Una "cartera" parece que almacena dinero. En Bitcoin no es así. Como dice Antonopoulos: _una cartera no es una cartera, es un llavero_.

Tu wallet no guarda monedas. Las monedas viven en el libro de registro, repartidas por toda la red. Lo que tu wallet guarda son llaves: una clave privada que firma y autoriza los pagos, y una clave pública de la que nace tu dirección para recibir.

La metáfora del llavero ayuda. Imagina un manojo de llaves grande. Puedes copiarlo y darle una copia a tu pareja: ambos llaveros abren exactamente las mismas cerraduras. En Bitcoin, quien tiene la llave controla las monedas asociadas. Por eso se repite tanto: _not your keys, not your coins_.

• Perder las llaves es perder el acceso al dinero, aunque siga en la red.
• Proteger tu llavero, no esconder monedas, es la verdadera seguridad.""",
        "en": """*🔑 The keys are a keyring*

A "wallet" sounds like it stores money. In Bitcoin it does not. As Antonopoulos says: _a wallet is not a wallet, it is a keyring_.

Your wallet holds no coins. The coins live in the ledger, spread across the whole network. What your wallet holds are keys: a private key that signs and authorizes payments, and a public key from which your receiving address is born.

The keyring metaphor helps. Picture a big bunch of keys. You can copy it and hand a copy to your partner: both keyrings open exactly the same locks. In Bitcoin, whoever holds the key controls the associated coins. That is why the saying repeats: _not your keys, not your coins_.

• Losing the keys means losing access to the money, even though it stays on the network.
• Protecting your keyring, not hiding coins, is the real security.""",
    },
    "edu_b4": {
        "btn_es": "⛏️ Minería y PoW",
        "btn_en": "⛏️ Mining and PoW",
        "es": """*⛏️ Minería y Prueba de Trabajo*

¿Quién decide qué transacciones se escriben en el libro si no hay jefe? Bitcoin lo resuelve con una lotería. Cualquiera puede participar, y el ganador anota el siguiente bloque y cobra una recompensa.

Para que nadie monopolice la lotería comprando billetes infinitos gratis, hay que hacer que jugar cueste. Ese coste es energía. Los mineros prueban una y otra vez la función _SHA-256_, añadiendo un número aleatorio llamado nonce, hasta hallar un hash por debajo de un objetivo. Es como lanzar un dado con tantas caras como átomos hay en el universo. A esto se le llama Prueba de Trabajo, _Proof of Work_.

Encontrar el billete ganador es carísimo, pero verificarlo es instantáneo: esa asimetría sostiene la honestidad.

• Cada 2016 bloques, unas dos semanas, la red ajusta la dificultad.
• Así el ritmo se mantiene cerca de un bloque cada 10 minutos.""",
        "en": """*⛏️ Mining and Proof of Work*

Who decides which transactions get written into the ledger if there is no boss? Bitcoin solves it with a lottery. Anyone can join, and the winner records the next block and earns a reward.

So that nobody monopolizes the lottery by printing infinite free tickets, playing must cost something. That cost is energy. Miners try the _SHA-256_ function over and over, adding a random number called a nonce, until they find a hash below a target. It is like rolling a die with as many faces as there are atoms in the universe. This is called Proof of Work.

Finding the winning ticket is hugely expensive, but verifying it is instant: that asymmetry keeps everyone honest.

• Every 2016 blocks, about two weeks, the network adjusts the difficulty.
• That keeps the pace near one block every 10 minutes.""",
    },
    "edu_b5": {
        "btn_es": "📡 Flujo de una transacción",
        "btn_en": "📡 Transaction flow",
        "es": """*📡 Cómo fluye una transacción*

Pagar con Bitcoin es un viaje de pocos pasos, pero elegante. Veámoslo de principio a fin.

• Firmar: tu wallet usa tu clave privada para firmar la transacción. La firma prueba que tienes derecho a gastar, sin revelar la llave.
• Anunciar: la transacción se transmite a la red. Tu nodo se la cuenta a otros nodos, y estos a más, propagándose en segundos.
• Verificar: cada nodo comprueba que la firma es válida y que no es un doble gasto. Si algo falla, la rechaza al instante.
• Bloque: un minero la incluye en el siguiente bloque al ganar la lotería de Prueba de Trabajo.

A partir de ahí llegan las _confirmaciones_: cada bloque nuevo minado encima añade trabajo y seguridad. Una confirmación es un bloque encima; seis confirmaciones, unos sesenta minutos, se consideran pago totalmente seguro. Para una venta pequeña basta con menos.""",
        "en": """*📡 How a transaction flows*

Paying with Bitcoin is a journey of just a few steps, yet an elegant one. Let us follow it from start to finish.

• Sign: your wallet uses your private key to sign the transaction. The signature proves you have the right to spend, without revealing the key.
• Announce: the transaction is broadcast to the network. Your node tells other nodes, and those tell more, propagating in seconds.
• Verify: each node checks that the signature is valid and that it is not a double spend. If anything is wrong, it rejects it instantly.
• Block: a miner includes it in the next block upon winning the Proof of Work lottery.

From there come the _confirmations_: each new block mined on top adds work and security. One confirmation is one block on top; six confirmations, about sixty minutes, are considered a fully safe payment. For a small sale, fewer will do.""",
    },
    "edu_b6": {
        "btn_es": "🧱 Blockchain y UTXO",
        "btn_en": "🧱 Blockchain and UTXO",
        "es": """*🧱 Blockchain y UTXO*

Imagina diez amigos, cada uno con una libreta idéntica. Cuando alguien paga, todos lo anotan en la misma página y, al llenarse, la encadenan a la anterior. Esa cadena de páginas es la _blockchain_: un libro compartido que nadie puede reescribir sin rehacer todo el trabajo posterior.

Ahora la sorpresa: Bitcoin no lleva _saldos_, lleva piezas de dinero. El modelo se llama UTXO, _salidas de transacciones no gastadas_. Tus monedas son, literalmente, salidas que recibiste y aún no has gastado.

Cada pieza se gasta entera, como un billete físico. Si recibiste una de 10 y pagas 7, consumes la pieza completa y la red te devuelve 3 de _cambio_ en una pieza nueva. Por eso casi toda transacción tiene al menos dos salidas.

• La suma de lo que sale nunca supera lo que entra: así se evita crear dinero de la nada.
• No hay cuentas con saldo, solo derechos de valor que pasan de mano en mano.""",
        "en": """*🧱 Blockchain and UTXO*

Picture ten friends, each with an identical notebook. When someone pays, they all write it on the same page and, once full, chain it to the previous one. That chain of pages is the _blockchain_: a shared ledger nobody can rewrite without redoing all the work that follows.

Now the twist: Bitcoin does not track _balances_, it tracks pieces of money. The model is called UTXO, _unspent transaction outputs_. Your coins are, literally, outputs you received and have not yet spent.

Each piece is spent whole, like a physical bill. If you received one worth 10 and pay 7, you consume the entire piece and the network sends you 3 back as _change_ in a brand new piece. That is why almost every transaction has at least two outputs.

• The total going out never exceeds what comes in: that prevents money from being created out of nothing.
• There are no accounts with balances, only rights to value passing from hand to hand.""",
    },
}
