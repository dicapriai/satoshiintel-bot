# SatoshiIntel — bot de Bitcoin para Telegram

**[@SatoshiIntelbot](https://t.me/SatoshiIntelbot)** · Canal: [@SatoshiIntel](https://t.me/SatoshiIntel)

Bot educativo y de herramientas de Bitcoin, bilingüe (español / inglés). Precio en vivo,
alertas, calculadoras, explorador de direcciones y transacciones, 30 lecciones,
diccionario de 90 términos y quiz.

---

## Por qué este código es público

No está aquí para que te lo instales. **Está aquí para que compruebes que no te miento.**

Un bot que te dice "tus consultas son privadas" te está pidiendo que confíes. Y en Bitcoin
la regla es la contraria: *don't trust, verify*. Así que aquí tienes el código entero, y
debajo te digo **exactamente dónde mirar** para verificar cada cosa que promete el bot.

No hace falta que seas programador. Basta con buscar el archivo y leer unas líneas.

---

## Compruébalo tú mismo

### 1. «No guardo lo que consultas»

Abre `bot.py` y busca `CREATE TABLE`. Vas a encontrar **dos tablas, y solo dos**:

```sql
users   -> chat_id, username, first_name, language, joined_at
alerts  -> chat_id, direction, target, lang, created_at
```

**No existe ninguna tabla de consultas.** Ni de direcciones, ni de transacciones, ni de
mensajes. No es que el bot decida no enseñarlas: es que **no hay dónde guardarlas**.

Y para que no quede duda, busca `INSERT INTO` en todo el archivo. Hay **exactamente dos**
en las 2.400 líneas del bot: uno registra al usuario, otro guarda una alerta de precio
que tú creaste a propósito. Nada más se escribe nunca.

### 2. «Tus consultas no salen a empresas de terceros»

Abre `sources.py`. Ahí está la regla, escrita en el propio código:

- **Comisiones, altura de bloque, mempool** → datos públicos y anónimos. Si el nodo no
  responde, se pueden pedir a una API pública sin comprometer a nadie.
- **Direcciones y transacciones** → **sin respaldo, nunca.** Si el nodo no responde, el
  bot dice "no disponible" en vez de preguntar fuera.

Esa asimetría es deliberada. Un respaldo silencioso ahí convertiría una caída del nodo en
una fuga de privacidad que nadie vería. Preferimos el error visible.

En `electrs.py` está cómo se habla directamente con el índice del nodo, sin intermediarios.

### 3. «El bot nunca te pide tu frase semilla»

Busca `semilla` o `seed` en `bot.py`. Aparece **solo dentro del contenido educativo**, y
siempre para decirte que **no la compartas con nadie**. No hay ni un punto del código que
la pida, la reciba o la guarde.

Ningún bot de Telegram debería pedírtela jamás — los mensajes viajan por servidores
ajenos. Si alguno lo hace, es un ladrón.

### 4. «Tus direcciones no acaban en los registros del servidor»

En `bot.py`, líneas 45-46:

```python
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
```

Sin eso, la librería HTTP escribiría cada URL consultada en los registros del servidor —
con la dirección dentro. Silenciarla es lo que evita que queden ahí.

---

## Lo que sí se guarda (y por qué)

Con la misma honestidad:

| Dato | Para qué |
|---|---|
| Tu ID de Telegram | Saber a quién responder y poder enviarte avisos |
| Tu @usuario y nombre | Aparecen en el panel de administración |
| Tu idioma | Responderte en español o inglés |
| Fecha de alta | Estadísticas de uso |
| Tus alertas de precio | Avisarte cuando se cumplan; las creas y las borras tú |

Eso es todo. Lo mismo que ve cualquier persona a la que escribes por Telegram.

---

## Arquitectura

Python 3.12 · `python-telegram-bot` en modo polling · PostgreSQL · sin frameworks web.

| Archivo | Qué hace |
|---|---|
| `bot.py` | Toda la lógica, menús y herramientas |
| `sources.py` | De dónde salen los datos on-chain y la regla de respaldo |
| `electrs.py` | Cliente del protocolo Electrum para hablar con un nodo propio |
| `addr_utils.py` | Validación y tipo de direcciones Bitcoin |
| `content_edu_*.py` | Las 30 lecciones |
| `content_dict_*.py` | El diccionario de 90 términos |

La configuración va por variables de entorno (ver `.env.example`). **Sin un nodo propio
configurado, el bot funciona igual usando la API pública de mempool.space** — que es lo
que hará quien clone este repositorio.

---

## Licencia

MIT — ver [LICENSE](LICENSE). Puedes usar, modificar y distribuir este código.

Si montas algo con él, te agradezco la mención, pero no estás obligado.

---

## Contacto

Errores y sugerencias: [abre un issue](../../issues) · SatoshiIntelbot@proton.me
