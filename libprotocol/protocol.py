import asyncio
import logging
from utils.buffer import TelnetBuffer
from libprotocol.client import Client


class MUDProtocol(asyncio.Protocol):
	def __init__(self, server, loop):
		super().__init__()
		self.logger = logging.getLogger("__main__." + __name__)
		self.server = server
		self.loop = loop
		self.transport = None
		self.belongsTo = None
		self.buffer = TelnetBuffer()
		self.logger.debug("Created object {}".format(self))

	def connection_made(self, transport):
		self.transport = transport
		self.logger.info("Connection recieved from {}".format(self.transport.get_extra_info("peername")))
		self.belongsTo = Client(self.server, self)
		if self.belongsTo.id is None:
			self.logger.warning("Disconnecting client with no ID")
			self.transport.close()
			return
		self.server.clients.append(self.belongsTo)
		self.logger.debug("Clients Connected: {}".format(self.server.clients))
		self.transport.write("\u001B[2J".encode("latin1"))

	def data_received(self, data):
		self.buffer.process_data(data.decode("latin1"))
		if self.buffer.isDone():
			self.write(self.buffer.flush() + "\n")
			self.server.broadcast(self.buffer.getLastMessage() + "\n", exclude=[self.belongsTo])
			self.logger.debug("{} flushed: {}".format(self.belongsTo, self.buffer.getLastMessage()))

	def connection_lost(self, exception):
		self.logger.info("Connection lost from {}, err: {}".format(self.transport.get_extra_info("peername"), exception))
		if self.belongsTo.id is None:
			self.logger.warning("Tried looping a client without ID")
		else:
			self.server.clients.remove(self.belongsTo)
		self.logger.debug("{} has no purpose".format(self))
		self.logger.debug("Clients Connected: {}".format(self.server.clients))

	def write(self, message):
		self.transport.write(message.encode("latin1"))

	def __str__(self):
		if self.transport is None:
			toFormat1 = "None"
		else:
			toFormat1 = self.transport.get_extra_info("peername")[0]

		return "MUDProtocol<{}>".format(toFormat1)

	def __repr__(self):
		return self.__str__()
