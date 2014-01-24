def get_domain(url):
	return url.split('.')[-2] # TODO: do this in some proper way...

def get_irc_username(string):
	return string.split('!')[0]

def get_entry(key, servers):
	"""Compensate stupid server name handling
	"""
	for k, v in servers.items():
		if get_domain(k) == get_domain(key):
			return v
	return None