import yaml, os.path


def get_user_dir():
	return os.path.expanduser('~')

def get_application_dir():
	return os.path.join(get_user_dir(), '.pyt')

def load_config(config_path=os.path.join(get_application_dir(), 'pyt.conf')):
	if os.path.isfile(config_path):
		return yaml.load(open(config_path, "r"))
	raise Exception('No config file found at "%s"' % config_path)

def load_theme(config_path=os.path.join(get_application_dir(), 'pyt.theme')):
	if os.path.isfile(config_path):
		return yaml.load(open(config_path, "r"))
	raise Exception('No theme file found at "%s"' % config_path)