import xml.etree.ElementTree as ET

import sleekxmpp.clientxmpp

from pyt.config_handler import loader
from pyt.chat_handler import utils


settings = loader.load_config()

# connection handling
def _on_message(msg):
	if msg['type'] in ('chat', 'normal'):
		communicator(
			"recv_msg",
			{
				"target": msg.get_from(), 
				"sender": msg.get_from(), 
				"msg": msg.body
			}
		)

# publicly accessible functions
def login(jid, passwd):
	global client
	client = sleekxmpp.clientxmpp.ClientXMPP(jid, passwd)
	if client.connect():
		client.send_presence()

def get_channel_list():
	chans = []

	roster = str(client.get_roster())
	root = ET.fromstring(roster)
	for query in root:
		for item in query:
			jid = item.attrib["jid"]
			chans.append(jid)

	return chans
	
def parse_input(msg, info):
	if msg[0] == '/':
		parse_command(msg, info)
	else:
		send_privmsg(msg, info)

def parse_command(msg, info):
	pass

def send_privmsg(msg, info):
	# info['channel'] -> jid
	client.sendMessage(info['channel'], msg)


def init_connection(callback):
	global communicator
	communicator = callback

	for jid, data in settings.items():
		if data['type'] == 'xmpp':
			login(jid, data['password'])

	client.add_event_handler('message', _on_message)
	client.process()

	for jid in get_channel_list():
		communicator(
			"add_item", 
			{
				'channel': jid, 
				'server': None,
				'type': 'xmpp'
			}
		)


if __name__ == "__main__":
	init_connection(lambda x, y: 42)