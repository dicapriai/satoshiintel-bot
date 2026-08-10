"""Que una petición cancelada no le deje su respuesta al siguiente.

EL FALLO QUE SE ARREGLÓ AQUÍ
`Pool.call` devuelve la conexión al pool en su `finally`, incluso si la
cancelaron a media lectura. La respuesta seguía viajando por el cable y se la
comía el usuario siguiente: pedías una dirección y recibías los datos de otra.
En producción se veía como errores de tipo cambiantes ('str' object has no
attribute 'get', 'height', 'list' object...) y el usuario leía
"No pude escanear ahora".
"""
import asyncio
import json
import electrs


class ServidorLento:
    """Electrs de mentira: responde despacio para poder cancelar a mitad."""

    def __init__(self, retraso=0.5):
        self.retraso = retraso
        self.servidas = 0

    async def _cliente(self, r, w):
        while True:
            linea = await r.readline()
            if not linea:
                break
            pet = json.loads(linea)
            await asyncio.sleep(self.retraso)
            self.servidas += 1
            # La respuesta lleva DENTRO qué se preguntó: así el test puede
            # detectar si a alguien le llega la respuesta de otro.
            w.write((json.dumps({"jsonrpc": "2.0", "id": pet["id"],
                                 "result": {"para": pet["params"][0]}}) + "\n").encode())
            await w.drain()

    async def arrancar(self):
        self.srv = await asyncio.start_server(self._cliente, "127.0.0.1", 0)
        return self.srv.sockets[0].getsockname()[1]


async def demo():
    srv = ServidorLento()
    puerto = await srv.arrancar()
    import os
    os.environ["ELECTRS_HOST"], os.environ["ELECTRS_PORT"] = "127.0.0.1", str(puerto)

    # UNA sola conexión: así el segundo usuario hereda por fuerza la del primero.
    pool = electrs.Pool(timeout=5, size=1)

    # Usuario A pregunta por "A" y se cancela antes de recibir
    tarea = asyncio.create_task(pool.call("m", ["DIRECCION_DE_A"]))
    await asyncio.sleep(0.15)          # ya envió, aún no ha leído
    tarea.cancel()
    try:
        await tarea
    except asyncio.CancelledError:
        pass

    # Usuario B pregunta por "B". Si hereda la conexión sucia, recibe la de A.
    res = await pool.call("m", ["DIRECCION_DE_B"])
    assert res["para"] == "DIRECCION_DE_B", \
        f"¡CRUCE! B pidió DIRECCION_DE_B y recibió {res['para']}"
    print("OK  una petición cancelada no contamina a la siguiente")

    # Y la conexión sigue siendo utilizable después del susto
    res = await pool.call("m", ["DIRECCION_DE_C"])
    assert res["para"] == "DIRECCION_DE_C"
    print("OK  la conexión se rehace sola y sigue sirviendo")

    await pool.close()
    srv.srv.close()
    print("\nOK ✅ pool: sin respuestas cruzadas entre usuarios")


if __name__ == "__main__":
    asyncio.run(demo())
