import asyncio
import logging
from gamelib.entities.entity import Entity


class Game(object):
	def __init__(self, server, tickRate=1):
		self.logger = logging.getLogger("__main__." + __name__)
		self.server = server
		self.tickRate = tickRate
		self.entities = []

	def get_location(self):
		pass

	def get_entities(self):
		return self.entities

	# This should work righttt...?
	def find_entities(self, name=None, entityType=type(Entity), uuid=None):
		ret = []
		for entity in self.entities:
			if isinstance(entity, entityType):
				if entity.get_name() == name or entity.get_uuid() == uuid:
					ret.append(entity)
		return ret

	# This is my game loop "sort of", it runs alongside the server in parallel
	async def on_tick(self):
		while True:
			self.server.broadcast("Hello traveler!")
			# self.logger.debug("Tick")
			await asyncio.sleep(self.tickRate)

	def __str__(self):
		return "Game<Tick Rate: {}>".format(self.tickRate)

	def __repr__(self):
		return self.__str__()
