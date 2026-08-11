CATEGORY = {
    "key": "cat_e",
    "btn_es": "🔒 Seguridad avanzada",
    "btn_en": "🔒 Advanced security",
}

ORDER = ["edu_e1", "edu_e2", "edu_e3", "edu_e4", "edu_e5",
         "edu_e6", "edu_e7", "edu_e8", "edu_e9"]

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

*La huella maestra: tu mejor aliado* 🔎
Toda wallet muestra un código de ocho caracteres llamado _master fingerprint_ o XFP, por ejemplo A1B2C3D4. Lo verás en Coldcard, Jade, Sparrow o Electrum.

Lo importante es esto:
• Tu semilla sola da una huella.
• Tu semilla *con* la passphrase da una huella *distinta*.
• Y si escribes la passphrase con un error, da otra huella diferente.

Como no existe el aviso de contraseña incorrecta, la huella es tu única forma rápida de saber si entraste a la wallet correcta. Anótala hoy junto a tu respaldo, y el día que restaures compárala: si coincide, escribiste todo bien. Si no coincide, hay un error y aún estás a tiempo de corregirlo.

Anota las dos: la de la semilla sola y la de la semilla con passphrase.

*Reglas:*
• Hazlo todo sin conexión. Nunca escribas tu semilla en una web, una app, un chat ni una IA.
• La huella no revela tus claves, es seguro anotarla. Pero no la publiques: identifica tu wallet.
• Cuando muevas fondos a una wallet nueva, manda primero una cantidad pequeña de prueba.

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

*The master fingerprint: your best ally* 🔎
Every wallet shows an eight character code called the _master fingerprint_ or XFP, for example A1B2C3D4. You'll see it on Coldcard, Jade, Sparrow or Electrum.

Here's what matters:
• Your seed alone gives one fingerprint.
• Your seed *with* the passphrase gives a *different* one.
• And if you type the passphrase with a mistake, it gives yet another one.

Since there is no wrong-password warning, the fingerprint is your only quick way to know you entered the right wallet. Write it down today next to your backup, and compare it the day you restore: if it matches, you typed everything correctly. If it doesn't, something is wrong and you still have time to fix it.

Write both down: the one for the seed alone and the one for seed plus passphrase.

*Rules:*
• Do it all offline. Never type your seed into a website, an app, a chat or an AI.
• The fingerprint doesn't reveal your keys, it's safe to write down. But don't publish it: it identifies your wallet.
• When moving funds to a new wallet, send a small test amount first.

A backup you never tested isn't a backup: it's a hope.

_Don't trust, verify._""",
    },
    "edu_e6": {
        "btn_es": "🎲 Crea tu semilla con dados",
        "btn_en": "🎲 Create your seed with dice",
        "es": """*Crea tu semilla con dados*

Sí se puede crear tu semilla con dados. Lo que no se puede es armarla con la lista EFF: esa es de otro estándar y sirve para la passphrase. Los dados llegan a la semilla por otro camino.

*Camino 1: dados, el que usan Coldcard y Jade*
Tiras 50 o más dados y escribes los números en el dispositivo. El aparato aplica SHA-256 a esa cadena y obtiene 128 o 256 bits de entropía, que se convierten en tus 12 o 24 palabras.
Tú pones el azar, el dispositivo solo traduce.

Lo mejor: el proceso es *determinista*. Las mismas tiradas dan siempre la misma semilla, así que puedes comprobar el resultado por tu cuenta con otra herramienta sin conexión. Ya no dependes de confiar en el fabricante.

*Camino 2: eliges tus propias palabras*
Puedes escribir palabras elegidas por ti, pero no las 12 completas: la última lleva un _checksum_ y la calcula el dispositivo. Tú aportas las primeras 11 o 23.
Con monedas queda limpio: 2,048 es 2 elevado a 11, así que 11 tiros dan una palabra (cara 1, cruz 0).

*Referencia:* 50 tiradas de dado son 129 bits, más que suficiente.

_No confíes, verifica._""",
        "en": """*Create your seed with dice*

You can create your seed with dice. What you cannot do is build it from the EFF list: that one belongs to another standard and is for the passphrase. Dice reach the seed by a different route.

*Route 1: dice, the one Coldcard and Jade use*
You roll 50 or more dice and type the numbers into the device. It applies SHA-256 to that string and gets 128 or 256 bits of entropy, which become your 12 or 24 words.
You supply the randomness, the device only translates.

The best part: the process is *deterministic*. The same rolls always give the same seed, so you can verify the result yourself with another offline tool. You no longer depend on trusting the manufacturer.

*Route 2: you pick your own words*
You can type words you chose, but not all 12: the last one carries a _checksum_ and the device computes it. You supply the first 11 or 23.
Coins map cleanly: 2,048 is 2 to the 11th, so 11 flips give one word (heads 1, tails 0).

*Reference:* 50 dice rolls are 129 bits, more than enough.

_Don't trust, verify._""",
    },
    "edu_e7": {
        "btn_es": "🔑 Passphrase: dados vs inventarla",
        "btn_en": "🔑 Passphrase: dice vs inventing it",
        "es": """*Passphrase: con dados o inventada*

La idea que casi nadie entiende: *la fuerza está en el proceso, no en la apariencia.*

Un atacante no prueba al azar. Usa diccionarios de contraseñas filtradas y un motor de reglas que ya prueba automáticamente todos los trucos humanos: cambiar a por 4, e por 3, o por 0, poner mayúscula al inicio, añadir un año, terminar en símbolo, nombres de mascotas y equipos en cada idioma.

Por eso:
• Perr0Firulais2015 aparenta mucho y son unos *35 bits*. Cae en minutos.
• Seis palabras EFF sacadas con dados parecen simplonas y son *77.6 bits*. Imposible.

*¿Y una inventada larga y rara?*
Si de verdad no contiene palabras de diccionario, puede ser fuerte. El problema es otro:
• No puedes *medir* su fuerza. Crees que es sólida, pero no lo sabes.
• No puedes *reproducirla*. ¿Eran dos símbolos o tres? ¿Un espacio o dos? ¿Mayúscula dónde?

Y recuerda: no existe el aviso de contraseña incorrecta. Un carácter distinto abre una wallet vacía, igual que si te hubieran robado.

Se ha perdido más Bitcoin por respaldos mal hechos que por hackeos. Los dados te dan fuerza comprobable *y* algo que podrás copiar exacto dentro de veinte años.

_No confíes, verifica._""",
        "en": """*Passphrase: with dice or invented*

The idea almost nobody gets: *strength lives in the process, not in the appearance.*

An attacker doesn't guess randomly. He uses leaked password dictionaries and a rules engine that already tries every human trick automatically: swap a for 4, e for 3, o for 0, capitalize the first letter, append a year, end with a symbol, pet and team names in every language.

So:
• Perr0Firulais2015 looks impressive and is about *35 bits*. It falls in minutes.
• Six EFF words rolled with dice look plain and are *77.6 bits*. Impossible.

*What about a long weird invented one?*
If it truly contains no dictionary words, it can be strong. The problem is a different one:
• You cannot *measure* its strength. You think it's solid, but you don't know.
• You cannot *reproduce* it. Two symbols or three? One space or two? Capital where?

And remember: there is no wrong-password warning. One different character opens an empty wallet, exactly as if you had been robbed.

More Bitcoin has been lost to bad backups than to hacks. Dice give you provable strength *and* something you can copy exactly twenty years from now.

_Don't trust, verify._""",
    },
    "edu_e8": {
        "btn_es": "🕵️ Cómo funciona un ataque real",
        "btn_en": "🕵️ How a real attack works",
        "es": """*Cómo funciona un ataque real*

Mucha gente cree que el atacante la investiga: su nombre, sus hijos, su mascota. Falso. El ataque es *masivo, ciego y automático*.

*El proceso real:*
Genera todas las semillas posibles con la entropía débil, deriva sus direcciones, las busca en la blockchain (que es pública y gratis de consultar) y barre las que tienen saldo. Sin ningún dato personal. Por eso se vacían cientos de wallets en minutos: es un script, no alguien espiándote.

*¿Sabe si tienes passphrase?* No, y eso es lo mejor.
No existe ninguna marca en la blockchain que lo indique. Con passphrase salen direcciones completamente distintas. Cuando él mira tus direcciones sin passphrase, ve vacío, exactamente igual que una semilla nunca usada. Pasa de largo.

Ojo con una cosa: si tu wallet señuelo tiene *historial* de movimientos, le estás avisando que esa semilla es real y que alguien la usa. Eso sí lo motiva a atacar la passphrase.

*Si ataca la passphrase:* prueba millones de candidatas por segundo en su computadora y compara contra *todas las direcciones con saldo* de Bitcoin a la vez. No necesita conocer la tuya.

*La economía te protege:* tiene millones de semillas. Va por el 99% fácil, los que no tenían passphrase.

_No confíes, verifica._""",
        "en": """*How a real attack works*

Many people think the attacker researches them: their name, their kids, their pet. False. The attack is *massive, blind and automated*.

*The real process:*
It generates every possible seed from the weak entropy, derives their addresses, looks them up on the blockchain (public and free to query) and sweeps the ones holding funds. No personal data at all. That's why hundreds of wallets are emptied in minutes: it's a script, not someone spying on you.

*Does he know if you have a passphrase?* No, and that's the beauty.
There is no marker on the blockchain showing it. With a passphrase you get completely different addresses. When he checks your passphrase-less addresses he sees empty, exactly like a seed that was never used. He moves on.

One caveat: if your decoy wallet has transaction *history*, you are telling him that seed is real and someone uses it. That does motivate him to attack the passphrase.

*If he attacks the passphrase:* he tries millions of candidates per second on his own machine and compares against *every funded Bitcoin address* at once. He doesn't need to know yours.

*Economics protect you:* he holds millions of seeds. He goes for the easy 99%, the ones with no passphrase.

_Don't trust, verify._""",
    },
    "edu_e9": {
        "btn_es": "🍴 Forks y splits: qué hacer",
        "btn_en": "🍴 Forks and splits: what to do",
        "es": """*Forks y divisiones de cadena: qué hacer*

Cada cierto tiempo alguien propone cambiar las reglas de Bitcoin. Como nadie manda, hay que ponerse de acuerdo, y ahí empieza el ruido.

*Los dos tipos:*
• _Soft fork_ — reglas más estrictas. Los nodos viejos siguen aceptando la cadena. Es compatible hacia atrás.
• _Hard fork_ — reglas incompatibles. Si no todos actualizan, la cadena se parte en dos.

Cuando un grupo activa reglas que el resto no acepta, aparece una *división de cadena*: dos redes con la misma historia hasta cierto bloque, y distintas a partir de ahí. Suele pasar que la cadena con poco poder de minado avanza lentísimo y queda atrás.

*Qué haces tú, que solo quieres tus sats a salvo:*
• *No hagas nada apurado.* Si tienes tus llaves, tus monedas existen en ambas cadenas. No se pierden.
• No muevas fondos durante los primeros días de un split. Espera a que se aclare.
• No cambies el software de tu wallet ni de tu nodo por presión de redes sociales.
• Si tienes monedas en un exchange, quien decide es el exchange, no tú. Otra razón para la autocustodia.

🚨 *La estafa de siempre:*
En cada fork aparecen webs y mensajes que dicen "reclama tus monedas del fork, pon aquí tu frase semilla". *Es robo, siempre, sin excepción.* Ninguna cadena legítima te pide tu semilla para nada.

En 2017 se robaron fortunas exactamente así. La regla no cambia: tu semilla no se escribe en ningún lado.

_No confíes, verifica._""",
        "en": """*Forks and chain splits: what to do*

Every now and then someone proposes changing Bitcoin's rules. Since nobody is in charge, people have to agree, and that's where the noise starts.

*The two types:*
• _Soft fork_ — stricter rules. Old nodes still accept the chain. It is backwards compatible.
• _Hard fork_ — incompatible rules. If not everyone upgrades, the chain splits in two.

When a group activates rules the rest don't accept, a *chain split* appears: two networks sharing the same history up to a block, and different after it. Usually the chain with little hash power moves very slowly and falls behind.

*What you do, when you just want your sats safe:*
• *Don't rush anything.* If you hold your keys, your coins exist on both chains. Nothing is lost.
• Don't move funds during the first days of a split. Wait for things to settle.
• Don't switch your wallet or node software because of social media pressure.
• If your coins sit on an exchange, the exchange decides, not you. One more reason for self-custody.

🚨 *The usual scam:*
In every fork, websites and messages appear saying "claim your fork coins, enter your seed phrase here". *That is theft, always, no exceptions.* No legitimate chain ever asks for your seed.

In 2017 fortunes were stolen exactly that way. The rule doesn't change: your seed is never typed anywhere.

_Don't trust, verify._""",
    },
}
