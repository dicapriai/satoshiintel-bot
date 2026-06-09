# 📚 Contenido extraído de los 12 libros — para Educación y Herramientas

Fuente: biblioteca en `Desktop/BITCOIN BOT LIBROS`. Material minado por 4 agentes.
Este archivo es la "materia prima" para ir implementando módulos en el bot.

---

## 🎓 MÓDULOS DE EDUCACIÓN PROPUESTOS (agrupados)

### A) Fundamentos del dinero
1. **¿Qué es el dinero?** — trueque, coincidencia de deseos, el bien más "vendible". (Ammous, Antonopoulos)
2. **Dinero duro vs dinero fácil** — ratio existencias/flujo (stock-to-flow). (Ammous)
3. **Los 21 millones** — escasez absoluta, 100M de sats por BTC, ajuste de dificultad. (Ammous, Gigi)
4. **El halving** — 50→25→12.5→6.25 BTC cada 210.000 bloques (~4 años) hasta ~2140. (Ammous)
5. **La inflación: el impuesto invisible** — efecto Cantillon, hiperinflación, "ladrón silencioso". (Ammous, Gigi)
6. **Preferencia temporal** — cigarra vs hormiga; buen dinero = pensar a largo plazo. (Pueblo Bitcoin, Gigi)
7. **Oro vs Bitcoin** — misma escasez, mejor tecnología (viaja por internet, divisible, sin custodio). (Del oro al bitcoin)

### B) Cómo funciona (simple)
8. **El problema del doble gasto** — por qué hacía falta un banco… o no. (Inventemos Bitcoin)
9. **Descentralización y nodos** — "todos los nodos son iguales"; imposible de apagar. (Antonopoulos)
10. **Las llaves = un llavero** — la wallet NO guarda monedas, guarda llaves. (Antonopoulos)
11. **Minería y Prueba de Trabajo** — la lotería que cuesta energía; SHA-256. (Inventemos, con Rigor)
12. **Cómo fluye una transacción** — firmar → anunciar → verificar → bloque → confirmaciones. (Antonopoulos)
13. **Blockchain y UTXO** — 10 amigos con libretas; piezas de dinero, no saldos. (con Rigor)

### C) Historia y cultura
14. **Satoshi y el bloque génesis** — el titular de The Times grabado en la 1ª página. (Libro de Satoshi)
15. **Historia de la criptografía** — de la escítala espartana a Turing y los cypherpunks. (Criptoria)
16. **No confíes, verifica** — el mantra; vacuna contra estafas. (Gigi)
17. **Por qué Satoshi desapareció** — sin fundador = descentralización real. (Gigi)

### D) Práctica y mentalidad
18. **Autocustodia: "not your keys, not your coins"** — tu banco suizo en la cabeza. (Pueblo Bitcoin)
19. **Empezar con poco: tus primeros sats** — desde $10; DCA; no trading. (Bitcoin para Pobres)
20. **Lightning Network** — pagos instantáneos y casi gratis (off-chain). (con Rigor, Para Pobres)
21. **Estafas y FUD: cómo protegerte** — altcoins basura, promesas de rendimiento, cold wallet. (Para Pobres)
22. **El internet del dinero / adopción** — para los otros 6.500 millones; estamos como Internet en los 90. (Antonopoulos, Gigi)

---

## 🧮 HERRAMIENTAS PROPUESTAS (con su fórmula)

| # | Herramienta | Fórmula / datos | Necesita API |
|---|-------------|-----------------|--------------|
| 1 | **Conversor SAT/USD/BTC** (ya hecho) | `sats = USD/precio × 100M` | Precio (✔ ya) |
| 2 | **Calculadora de inflación** (pérdida poder adquisitivo) | `valor_real = monto/(1+i)^n` | No |
| 3 | **Planificador DCA "Apila Sats"** | `sats = (aporte/precio)×100M` por periodo, sumado | Precio |
| 4 | **Cuenta regresiva al halving** | `bloques_rest = 210.000 − (altura mod 210.000)`; ×10 min | Altura de bloque |
| 5 | **% de los 21M ya minados** | suma de recompensas por época | Altura de bloque |
| 6 | **Ahorrar en sats vs fiat** | fiat `M/(1+i)^n` vs BTC `M×(1+g)^n` | Precio |
| 7 | **Calculadora de remesas** (vs Western Union) | `ahorro = monto × (com_trad% − com_LN%)` | No |
| 8 | **Stock-to-flow / dureza** | `S2F = existencias/flujo`; inflación = `1/S2F` | Altura (opcional) |
| 9 | **Scam-checker / banderas rojas** | cuestionario con puntaje de riesgo | No |
| 10 | **Quiz educativo** (21 preguntas) | banco de preguntas con explicación | No |
| 11 | **Cita del día / "En palabras de Satoshi"** | banco de frases rotativas | No |

**APIs gratis sin key:** precio → CoinGecko (ya usado). Altura de bloque/halving → mempool.space o blockchain.info.

---

## 💬 MEJORES FRASES (para usar en el bot)

- "Solo dos cosas son realmente escasas: el tiempo y Bitcoin." — Ammous (vía Gigi)
- "Bitcoin son matemáticas, el dinero Fiat es humo." — Bitcoin para Pobres
- "Bitcoin siempre es cara cuando la comparas con el pasado, pero barata cuando la comparas con el futuro." — Bitcoin para Pobres
- "Una 'cartera' no es una cartera; es un llavero. No contiene monedas: contiene llaves." — Antonopoulos
- "No confíes, verifica." — cultura Bitcoin (Gigi)
- "Bitcoin no es una moneda. Bitcoin es Internet del Dinero." — Antonopoulos
- "Nunca le preguntes a un taxista qué piensa de Uber, ni a un banquero qué piensa de Bitcoin." — Bitcoin para Pobres
- "Pones tu patrimonio en Bitcoin, memorizas las claves… ¡Ponle impuestos a ESO!" — Saylor (vía La Filosofía de Bitcoin)
- "Bitcoin está construido sobre un 100% de verificación y un 0% de confianza." — Ammous
- "Bitcoin no va a cambiar. Yo cambiaré." — Gigi
- Bloque génesis: "The Times 03/Enero/2009 — El ministro de hacienda al borde del segundo rescate bancario."
- "El futuro ya está aquí, solo que no está igualmente distribuido." — William Gibson (vía Gigi)
