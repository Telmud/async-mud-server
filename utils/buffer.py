import logging


class TelnetBuffer(object):
	def __init__(self):
		self.logger = logging.getLogger("__main__." + __name__)
		self.buffer = ""
		self.message = None
		self.lastMessage = None
		self.states = {
			# Different states we can be in while reading data from client
			# See _process_sent_data function
			"READ_STATE_NORMAL": 1,
			"READ_STATE_COMMAND": 2,
			"READ_STATE_SUBNEG": 3,

			# Command codes used by Telnet protocol
			# See _process_sent_data function
			"TN_INTERPRET_AS_COMMAND": 255,
			"TN_ARE_YOU_THERE": 246,
			"TN_WILL": 251,
			"TN_WONT": 252,
			"TN_DO": 253,
			"TN_DONT": 254,
			"TN_SUBNEGOTIATION_START": 250,
			"TN_SUBNEGOTIATION_END": 240

		}
		self.currentState = self.states["READ_STATE_NORMAL"]
		self.logger.debug("Created object {}".format(self))

	def process_data(self, data):
		for c in data:
			# handle the character differently depending on the state we're in:
			# normal state
			if self.currentState == self.states["READ_STATE_NORMAL"]:

				# if we received the special 'interpret as command' code,
				# switch to 'command' state so that we handle the next
				# character as a command code and not as regular text data
				if ord(c) == self.states["TN_INTERPRET_AS_COMMAND"]:
					self.currentState = self.states["READ_STATE_COMMAND"]

				# if we get a newline character, this is the end of the
				# message. Set 'message' to the contents of the buffer and
				# clear the buffer
				elif c == "\n":
					self.message = self.buffer
					self.buffer = ""

				# some telnet clients send the characters as soon as the user
				# types them. So if we get a backspace character, this is where
				# the user has deleted a character and we should delete the
				# last character from the buffer.
				elif c == "\x08":
					self.buffer = self.buffer[:-1]

				# otherwise it's just a regular character - add it to the
				# buffer where we're building up the received message
				else:
					self.buffer += c

			# command state
			elif self.currentState == self.states["READ_STATE_COMMAND"]:

				# the special 'start of subnegotiation' command code indicates
				# that the following characters are a list of options until
				# we're told otherwise. We switch into 'subnegotiation' state
				# to handle this
				if ord(c) == self.states["TN_SUBNEGOTIATION_START"]:
					self.currentState = self.states["READ_STATE_SUBNEG"]

				# if the command code is one of the 'will', 'wont', 'do' or
				# 'dont' commands, the following character will be an option
				# code so we must remain in the 'command' state
				elif ord(c) in (self.states["TN_WILL"], self.states["TN_WONT"], self.states["TN_DO"], self.states["TN_DONT"]):
					self.currentState = self.states["READ_STATE_COMMAND"]

				# for all other command codes, there is no accompanying data so
				# we can return to 'normal' state.
				else:
					self.currentState = self.states["READ_STATE_NORMAL"]

			# subnegotiation state
			elif self.currentState == self.states["READ_STATE_SUBNEG"]:

				# if we reach an 'end of subnegotiation' command, this ends the
				# list of options and we can return to 'normal' state.
				# Otherwise we must remain in this state
				if ord(c) == self.states["TN_SUBNEGOTIATION_END"]:
					self.currentState = self.states["READ_STATE_NORMAL"]

	def flush(self):
		ret = self.message
		self.lastMessage = self.message
		self.message = None
		return ret

	def getLastMessage(self):
		return self.lastMessage

	def isDone(self):
		if type(self.message) == str:
			return True
		else:
			return False

	def __str__(self):
		return "TelnetBuffer<>"

	def __repr__(self):
		return self.__str__()