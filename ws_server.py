import logging
import asyncio

from websockets import WebSocketServerProtocol
import websockets

logging.basicConfig(level=logging.INFO)

class Server:
	async def unregister(self, ws: WebSocketServerProtocol) -> None:
		logging.info(f"disconnected {ws.remote_address}")

	async def send_to_client(self, ws: WebSocketServerProtocol, msg: str) -> None:
		await ws.send(msg)

	async def distribute(self, ws: WebSocketServerProtocol) -> None:
		async for msg in ws:
			logging.info(f"got msg: {msg}")
			await self.send_to_client(ws, "OK: " + msg)

	async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
		try:
			await self.distribute(ws)
		finally:
			await self.unregister(ws)


if __name__ == '__main__':
	server = Server()
	start_server = websockets.serve(server.ws_handler, 'localhost', 1234)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(start_server)
	loop.run_forever()
