import irc.client, shlex

from pyt.config_handler import loader
from pyt.chat_handler import utils
from pyt.command_handler import handler


client = irc.client.IRC()
servers = {} # holds all connected servers and additional information
# servers = {
#	{
#		"conn": <connection object>,
#		"chans": [<chan name>, <chan name>]	
#	}
#}
cmd_handler = handler.IRCCmdHandler(servers)
settings = loader.load_config()

# connection handling
def _on_connect(conn, event):
	for server, data in settings.items():
		if utils.get_domain(event.source) == utils.get_domain(server):
			for chan in data['channels']:
				join_channel(chan, server)

def _on_disconnect(conn, event):
	del servers[event.target]

def _on_privmsg(conn, event):
	pass

def _on_pubmsg(conn, event):
	communicator(
		"recv_msg",
		{
			"target": event.target, 
			"sender": event.source, 
			"msg": event.arguments[0]
		}
	)

# other stuff
def join_channel(chan, server):
	if irc.client.is_channel(chan):
		servers[server]["conn"].join(chan)
		servers[server].get("chans", []).append(chan)
		
		communicator("add_item", (chan, server, 'irc'))

# publicly accessible functions
def login(username, passwd, server):
	servers[server] = {}

	servers[server]["conn"] = client.server().connect(server, 6667, username)

	servers[server]["conn"].add_global_handler("welcome", _on_connect)
	servers[server]["conn"].add_global_handler("disconnect", _on_disconnect)
	servers[server]["conn"].add_global_handler("privmsg", _on_privmsg)
	servers[server]["conn"].add_global_handler("pubmsg", _on_pubmsg)


def get_channel_list(server):
	try:
		return servers[server]["chans"]
	except KeyError:
		return []

def parse_input(msg, info):
	if len(msg) == 0:
		pass
	elif msg[0] == '/':
		parse_command(msg, info)
	else:
		send_privmsg(msg, info)

def parse_command(msg, info):
	cmd = msg[1:]
	cmd_handler.handle(cmd, info)

def send_privmsg(msg, info):
	channel = info[0]
	server = info[1]

	for serv, data in servers.items():
		if utils.get_domain(server) == utils.get_domain(serv):
			servers[server]["conn"].privmsg(channel, msg)
			break


def init_connection(callback):
	global communicator
	communicator = callback

	cmd_handler.set_communicator(communicator)

	for server, data in settings.items():
		if data['type'] == 'irc':
			login(data['nick'], None, server)
	client.process_forever()


if __name__ == "__main__":
	init_connection(lambda x, y: 42)