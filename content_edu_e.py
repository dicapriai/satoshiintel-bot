CATEGORY = {
    "key": "cat_e",
    "btn_es": "🔒 Seguridad avanzada",
    "btn_en": "🔒 Advanced security",
}

ORDER = ["edu_e1", "edu_e2", "edu_e3", "edu_e4", "edu_e5"]

MODULES = {
    "edu_e1": {
        "btn_es": "🎲 Entropía y dados",
        "btn_en": "🎲 Entropy & dice",
        "es": """*Entropía: el azar que protege tus bitcoin*

Tu frase semilla nace de un número aleatorio. A ese azar se le llama _entropía_, y se mide en bits. Con 128 bits hay tantas combinaciones posibles que adivinarla es imposible. Con 40 bits, una computadora la revienta en minutos.

En 2026 pasó justo eso: un fallo en las Coldcard hacía que las semillas salieran con ~40-72 bits en vez de 128. Cuando se hizo público, se robaron unos *594 BTC (38 millones de dólares)* de ~500 billeteras en minutos.

¿Quiénes se salvaron? Los que habían creado su semilla con *sus propios dados*.

*Cómo generar tu propia entropía:*
• Un dado normal aporta 2.58 bits. *50 tiradas = 129 bits*, más que suficiente.
• Con la lista EFF, cada 5 dados te dan una palabra (7,776 = 6 elevado a 5). Seis palabras ya son 77 bits.
• Anota todo en papel, sin conexión. Nunca en fotos, nube ni chats.

*La regla de oro:* nunca dejes que un tercero genere tu azar. Ni una web, ni un bot, ni una IA. El único azar en el que puedes confiar es el que tiras tú con tus manos.

_No confíes, verifica._""",
        "en": """*Entropy: the randomness that protects your bitcoin*

Your seed phrase is born from a random number. That randomness is called _entropy_, and it's measured in bits. With 128 bits there are so many combinations that guessing is impossible. With 40 bits, a computer cracks it in minutes.

In 2026 exactly that happened: a Coldcard flaw generated seeds with ~40-72 bits instead of 128. When it went public, about *594 BTC (38 million dollars)* were swept from ~500 wallets in minutes.

Who was safe? The people who created their seed with *their own dice*.

*How to generate your own entropy:*
• One regular die gives 2.58 bits. *50 rolls = 129 bits*, more than enough.
• With the EFF list, every 5 dice give you one word (7,776 = 6 to the 5th). Six words is already 77 bits.
• Write everything on paper, offline. Never in photos, cloud or chats.

*The golden rule:* never let a third party generate your randomness. Not a website, not a bot, not an AI. The only randomness you can trust is the one you roll yourself.

_Don't trust, verify._""",
    },
    "edu_e2": {
        "btn_es": "🎲 Dados: EFF vs BIP39",
        "btn_en": "🎲 Dice: EFF vs BIP39",
        "es": """*Dados: lista EFF vs lista BIP39*

Mucha gente las confunde. Son *dos listas distintas, para cosas distintas.*

*📋 Lista EFF* — 7,776 palabras, 12.9 bits cada una. Sirve para tu *passphrase* (la palabra extra encima de la semilla). La hizo la Electronic Frontier Foundation.

*📋 Lista BIP39* — 2,048 palabras, 11 bits cada una. Son las *12 o 24 palabras de tu semilla*. Es el estándar de Bitcoin.

*Caso 1: passphrase con EFF, los dados dan la palabra directo* ✅
La lista tiene 7,776 palabras porque 6 elevado a 5 es exactamente 7,776. Cinco tiradas apuntan a una palabra:
tiras 4-2-6-1-3, buscas 42613 en la lista, sale _outcome_.
Repites 6 u 8 veces y ya tienes tu passphrase. Sin computadora, sin confiar en nadie.

*Caso 2: semilla BIP39 con dados, NO es directo* ⚠️
No puedes buscar palabra por palabra, por dos razones:
• 2,048 no es potencia de 6, los dados no caen limpio en esa lista.
• La última palabra lleva un _checksum_: no es libre, se calcula. Por eso Jade y Coldcard dicen "yo calculo la última palabra".

Lo que hacen los dispositivos: tiras 50 o más dados y el aparato convierte ese azar en tus 12 o 24 palabras. Tú pones la aleatoriedad, él solo traduce. Eso fue lo que salvó a la gente en el fallo de Coldcard: aunque el chip fallara, *el azar era suyo*.

*Resumen:*
• Dados + EFF = palabras directo, para tu passphrase.
• Dados + dispositivo = tu semilla BIP39 (el azar lo pones tú).

_No confíes, verifica._""",
        "en": """*Dice: EFF list vs BIP39 list*

People mix them up. They are *two different lists, for two different jobs.*

*📋 EFF list* — 7,776 words, 12.9 bits each. It's for your *passphrase* (the extra word on top of the seed). Made by the Electronic Frontier Foundation.

*📋 BIP39 list* — 2,048 words, 11 bits each. These are the *12 or 24 words of your seed*. It's the Bitcoin standard.

*Case 1: passphrase with EFF, dice give the word directly* ✅
The list has 7,776 words because 6 to the 5th is exactly 7,776. Five rolls point to one word:
roll 4-2-6-1-3, look up 42613, you get _outcome_.
Repeat 6 or 8 times and your passphrase is done. No computer, no trusting anyone.

*Case 2: BIP39 seed with dice, NOT direct* ⚠️
You can't look up word by word, for two reasons:
• 2,048 is not a power of 6, dice don't map cleanly onto that list.
• The last word carries a _checksum_: it isn't free, it's computed. That's why Jade and Coldcard say "I'll calculate the last word".

What devices do: you roll 50 or more dice and the device turns that randomness into your 12 or 24 words. You supply the randomness, it only translates. That's what saved people in the Coldcard flaw: even with a faulty chip, *the randomness was theirs*.

*Summary:*
• Dice + EFF = words directly, for your passphrase.
• Dice + device = your BIP39 seed (you supply the randomness).

_Don't trust, verify._""",
    },
    "edu_e3": {
        "btn_es": "🔏 Verifica el firmware",
        "btn_en": "🔏 Verify the firmware",
        "es": """*Verifica el firmware antes de instalarlo*

Descargas una actualización para tu hardware wallet. ¿Cómo sabes que es la verdadera y no una versión manipulada que te va a robar? Con la *firma digital*.

El fabricante firma cada archivo con su llave privada y publica su llave pública. Tú compruebas que la firma cuadra: si alguien alteró un solo byte, la verificación falla.

*Cómo se hace, en simple:*
• Descarga el firmware *solo* desde el sitio oficial del fabricante.
• Descarga también el archivo de firma que lo acompaña.
• Comprueba la firma con una herramienta como GPG usando la llave pública oficial.
• Muchos dispositivos, como Coldcard, también verifican la firma en el propio aparato antes de instalar.

*Reglas de oro:*
• Nunca descargues firmware de un link que te mandaron por chat, correo o redes.
• Guarda la llave pública del fabricante una vez y reúsala. Buscarla de nuevo cada vez es donde te engañan.
• Antes de actualizar, revisa si hay avisos de seguridad publicados.

Verificar toma cinco minutos. No verificar puede costarte todo.

_No confíes, verifica._""",
        "en": """*Verify the firmware before installing it*

You download an update for your hardware wallet. How do you know it's the real one and not a tampered version that will steal from you? With the *digital signature*.

The manufacturer signs every file with their private key and publishes their public key. You check the signature matches: if anyone altered a single byte, verification fails.

*How it works, in simple terms:*
• Download firmware *only* from the manufacturer's official site.
• Also download the signature file that comes with it.
• Check the signature with a tool like GPG using the official public key.
• Many devices, like Coldcard, also verify the signature on the device itself before installing.

*Golden rules:*
• Never download firmware from a link sent to you by chat, email or social media.
• Save the manufacturer's public key once and reuse it. Looking it up fresh every time is where they trick you.
• Before updating, check whether any security advisories have been published.

Verifying takes five minutes. Not verifying can cost you everything.

_Don't trust, verify._""",
    },
    "edu_e4": {
        "btn_es": "🗝️ La passphrase (palabra 13)",
        "btn_en": "🗝️ The passphrase (13th word)",
        "es": """*La passphrase: tu palabra 13*

La passphrase es un secreto extra que se suma a tus 12 o 24 palabras. No se guarda en el dispositivo: vive solo en tu cabeza o en tu papel.

Lo importante es entender esto:
• Semilla sola, sin passphrase → *wallet A*
• Misma semilla + tu passphrase → *wallet B*, completamente distinta
• Misma semilla + un error de tipeo → *wallet C*, vacía

No existe el mensaje de "contraseña incorrecta". Cualquier passphrase que escribas abre alguna wallet válida, solo que vacía. Por eso es tan poderosa y tan peligrosa a la vez.

*Para qué sirve:*
• Si alguien encuentra tu papel con las 12 palabras, no llega a tus fondos reales.
• Puedes dejar una cantidad pequeña en la wallet sin passphrase, como señuelo.

*Cuidados:*
• Distingue mayúsculas, espacios y símbolos. Un espacio de más es otra wallet.
• Si la pierdes, pierdes los fondos. No hay recuperación posible.
• Respáldala en un lugar *distinto* al de tu semilla, nunca en el mismo papel.
• Genérala con dados y la lista EFF, y pruébala primero con una cantidad pequeña.

_No confíes, verifica._""",
        "en": """*The passphrase: your 13th word*

The passphrase is an extra secret added to your 12 or 24 words. It isn't stored on the device: it lives only in your head or on your paper.

The key thing to understand:
• Seed alone, no passphrase → *wallet A*
• Same seed + your passphrase → *wallet B*, completely different
• Same seed + a typo → *wallet C*, empty

There is no "wrong password" message. Any passphrase you type opens some valid wallet, just an empty one. That's what makes it both powerful and dangerous.

*What it's for:*
• If someone finds your paper with the 12 words, they don't reach your real funds.
• You can leave a small amount in the passphrase-less wallet as a decoy.

*Warnings:*
• Capital letters, spaces and symbols matter. One extra space is a different wallet.
• If you lose it, you lose the funds. There is no recovery.
• Back it up somewhere *different* from your seed, never on the same paper.
• Generate it with dice and the EFF list, and test it first with a small amount.

_Don't trust, verify._""",
    },
    "edu_e5": {
        "btn_es": "✅ Verifica tu semilla offline",
        "btn_en": "✅ Verify your seed offline",
        "es": """*Verifica tu semilla antes de confiarle tu dinero*

El error más común no es perder la semilla: es descubrir demasiado tarde que *el respaldo estaba mal*. Una letra torcida, una palabra en el orden equivocado, una foto borrosa. Y te enteras el día que más lo necesitas.

La solución es probar el respaldo *antes* de meter fondos serios.

*Cómo hacerlo:*
• Anota tu semilla en papel y guarda el dispositivo.
• Borra el dispositivo por completo, con un reset de fábrica.
• Recupéralo usando *solo tu papel*, sin mirar nada más.
• Compara: la primera dirección de recibir debe ser exactamente la misma.

Si coincide, tu respaldo sirve. Si no, acabas de salvarte de perderlo todo, y aún estás a tiempo.

*Reglas:*
• Hazlo todo sin conexión. Nunca escribas tu semilla en una web, una app, un chat ni una IA.
• Cuando muevas fondos a una wallet nueva, manda primero una cantidad pequeña de prueba.
• Repite esta verificación de vez en cuando, sobre todo si cambias de papel o de lugar.

Un respaldo que nunca probaste no es un respaldo: es una esperanza.

_No confíes, verifica._""",
        "en": """*Verify your seed before trusting it with your money*

The most common mistake isn't losing the seed: it's finding out too late that *the backup was wrong*. A crooked letter, a word in the wrong order, a blurry photo. And you find out on the day you need it most.

The fix is testing the backup *before* putting serious funds in.

*How to do it:*
• Write your seed on paper and put the device aside.
• Wipe the device completely with a factory reset.
• Restore it using *only your paper*, without looking at anything else.
• Compare: the first receive address must be exactly the same.

If it matches, your backup works. If it doesn't, you just saved yourself from losing everything, and you still have time.

*Rules:*
• Do it all offline. Never type your seed into a website, an app, a chat or an AI.
• When moving funds to a new wallet, send a small test amount first.
• Repeat this check now and then, especially if you change paper or location.

A backup you never tested isn't a backup: it's a hope.

_Don't trust, verify._""",
    },
}
