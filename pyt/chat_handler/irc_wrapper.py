import irc.client

from pyt.config_handler import loader
from pyt.chat_handler import utils


client = irc.client.IRC()
servers = {} # holds all connected servers and additional information
# servers = {
#	{
#		"conn": <connection object>,
#		"chans": [<chan name>, <chan name>]	
#	}
#}
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
	print(event.source)
	print(event.arguments)

# other stuff
def join_channel(chan, server):
	if irc.client.is_channel(chan):
		servers[server]["conn"].join(chan)
		servers[server].get("chans", []).append(chan)
		add_channel_to_menu(chan)

# publicly accessible functions
def login(username, passwd, server):
	servers[server] = {}

	servers[server]["conn"] = client.server().connect(server, 6667, username)

	servers[server]["conn"].add_global_handler("welcome", _on_connect)
	servers[server]["conn"].add_global_handler("disconnect", _on_disconnect)
	servers[server]["conn"].add_global_handler("privmsg", _on_privmsg)

def get_channel_list(server):
	try:
		return servers[server]["chans"]
	except KeyError:
		return []

def send_privmsg(msg, chan, server):
	servers[server]["conn"].privmsg(chan, msg)


def init_connection(callback):
	global add_channel_to_menu
	add_channel_to_menu = callback

	for server, data in settings.items():
		if data['type'] == 'irc':
			login(data['nick'], None, server)
	client.process_forever()