import irc.client, irc.events
import socket

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
	try:
		del servers[event.target]
	except KeyError:
		print("[DEBUG] - Tried to delete nonexistent target")

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

def _on_part(conn, event):
	channel = event.target
	remote_addr = socket.gethostbyaddr(conn.socket.getpeername()[0])[0]

	my_data = utils.get_entry(remote_addr, settings)
	target_nick = utils.get_irc_username(event.source)

	if my_data["nick"] != target_nick:
		# someone else left channel
		communicator(
			"recv_msg",
			{
				"target": channel, 
				"sender": channel, 
				"msg": '%s left' % target_nick
			}
		)
	else:
		# I left channel - TODO: improve command handler
		pass

def _on_join(conn, event):
	channel = event.target
	remote_addr = socket.gethostbyaddr(conn.socket.getpeername()[0])[0]

	my_data = utils.get_entry(remote_addr, settings)
	target_nick = utils.get_irc_username(event.source)

	if my_data["nick"] == target_nick:
		# I joined channel
		for server, data in settings.items():
			if utils.get_domain(remote_addr) == utils.get_domain(server):
				communicator(
					"add_item", 
					{
						'channel': channel, 
						'server': server,
						'type': 'irc'
					}
				)
				break
	else:
		# someone else joined channel
		communicator(
			"recv_msg",
			{
				"target": channel, 
				"sender": channel, 
				"msg": '%s joined' % target_nick
			}
		)

def generic_print(conn, event):
	source = event.source
	arg = ' '.join(event.arguments)

	communicator(
		"recv_msg",
		{
			"target": "master", 
			"sender": source, 
			"msg": arg
		}
	)

# other stuff
def join_channel(chan, server):
	if irc.client.is_channel(chan):
		servers[server]["conn"].join(chan)
		servers[server].get("chans", []).append(chan)

# publicly accessible functions
def login(username, passwd, server):
	servers[server] = {}

	servers[server]["conn"] = client.server().connect(server, 6667, username)

	# add generic printing for everything
	for val in irc.events.numeric.values():
		servers[server]["conn"].add_global_handler(val, generic_print)

	# add some specific behaviours
	servers[server]["conn"].add_global_handler("welcome", _on_connect)
	servers[server]["conn"].add_global_handler("disconnect", _on_disconnect)
	servers[server]["conn"].add_global_handler("privmsg", _on_privmsg)
	servers[server]["conn"].add_global_handler("pubmsg", _on_pubmsg)
	servers[server]["conn"].add_global_handler("join", _on_join)
	servers[server]["conn"].add_global_handler("part", _on_part)


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
	channel = info['channel']
	server = info['server']

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