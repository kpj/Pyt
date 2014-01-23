import shlex


class IRCCmdHandler(object):
	def __init__(self, servers):
		self.servers = servers
		self.communicator = None

	def set_communicator(self, comm):
		self.communicator = comm

	def handle(self, cmd, info):
		channel = info['channel']
		server = info['server']
		typ = info['type']

		if cmd == 'part':
			self.servers[server]["conn"].part(channel, message='Pyt')
			self.communicator("rm_item", channel)