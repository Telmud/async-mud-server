import asyncio
import logging
from libprotocol.protocol import MUDProtocol

class MUDServer(object):
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.DEBUG)
		self.clients = []
		self.logger.debug("Created object {}".format(self))
		
	async def start_server(self):
		self.logger.info("Starting Server...")
		loop = asyncio.get_running_loop()
		server = await loop.create_server(lambda: MUDProtocol(self, loop), "0.0.0.0", "7777")
		async with server:
			await server.serve_forever()

	def broadcast(self, message, exclude=[]):
		for client in self.clients:
			if client in exclude:
				continue
			client.protocol.write(message)

	def __str__(self):
		return "MUDServer<Connected: {}>".format(len(self.clients))

	def __repr__(self):
		return self.__str__()

async def main():
	server = MUDServer()
	await server.start_server()

if __name__ == '__main__':
	try:
		logging.basicConfig(format="[%(asctime)s %(levelname)s] (%(module)s.py:%(lineno)d) %(message)s")
		asyncio.run(main())
	except Exception as e:
		print(e)
		exit()