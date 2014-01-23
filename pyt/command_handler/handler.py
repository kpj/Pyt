import shlex


class IRCCmdHandler(object):
	def __init__(self, servers):
		self.servers = servers
		self.communicator = None

	def set_communicator(self, comm):
		self.communicator = comm

	def handle(self, cmd, info):
		channel = info[0]
		server = info[1]
		typ = info[2]

		if cmd == 'part':
			self.servers[server]["conn"].part(channel, message='Pyt')
			self.communicator("rm_item", channel)