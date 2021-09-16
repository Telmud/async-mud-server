import asyncio
import random
import logging


class Client(object):
	def __init__(self, server, protocol):
		self.logger = logging.getLogger("__main__." + __name__)
		self.server = server
		self.protocol = protocol
		try:
			self.id = random.choice([i for i in range(0, 10000) if i not in [x.id for x in self.server.clients]])
		except IndexError:
			self.id = None
			self.logger.error("Couldn't assign id to a client (Probably hit the slot limit), assigning None")	
		self.logger.debug("Created object {}".format(self))

	def __eq__(self, other):
		if self.id == other.id:
			return True	

	def __str__(self):
		return "Client<{}>".format(self.id)

	def __repr__(self):
		return self.__str__()