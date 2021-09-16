import asyncio
import logging


class Game(object):
	def __init__(self, server, tickRate=5):
		self.logger = logging.getLogger("__main__." + __name__)
		self.server = server
		self.tickRate = tickRate

	def get_location(self):
		pass

	# This is my game loop "sort of", it runs alongside the server in parallel
	async def onTick(self):
		while True:
			self.server.broadcast("Hello traveler!")
			# self.logger.debug("Tick")
			await asyncio.sleep(self.tickRate)

	def __str__(self):
		return "Game<Tick Rate: {}>".format(self.tickRate)

	def __repr__(self):
		return self.__str__()
