import curses, locale

from pyt.interface import utils
from pyt.interface.structures import menu
from pyt.config_handler import loader


class ChannelListWindow(object):
	def __init__(self, stdscr):
		(height, width) = stdscr.getmaxyx()
		self.win = curses.newwin(height, 20, 0, 0)
		self.win.immedok(True)

		self.menu = menu.Menu('Channel list', [], self.win)
		utils.start_thread(self.menu.display) # channel list thread

def get_channel_list_window(stdscr):
	return ChannelListWindow(stdscr)


class ChatWindow(object):
	def __init__(self, stdscr):
		(height, width) = stdscr.getmaxyx()
		self.win = curses.newwin(height, width - 20, 0, 25)
		self.win.immedok(True)

		self.chat_history = {}

		self.input = ''

		self.theme = loader.load_theme()

		self.max_input_length = width - 20;
		self.input_field_x = 2
		self.input_field_y = height - 2
		self.win.addstr(self.input_field_y, self.input_field_x - 1, self.theme["prompt"])

		locale.setlocale(locale.LC_ALL, '')
		self.code = locale.getpreferredencoding()

		self.selected_channel = None

	def new_message(self, data=None):
		if not data["target"] in self.chat_history.keys():
			self.chat_history[data["target"]] = []
		self.chat_history[data["target"]].insert(0, self.theme["chat-line"] % (data["sender"], data["msg"]))
		
		self.show_all_messages()

	def show_all_messages(self):
		self.win.clear()
		self.win.addstr(self.input_field_y, self.input_field_x - 1, self.theme["prompt"])

		if self.selected_channel in self.chat_history.keys():
			cur_course = self.chat_history[self.selected_channel]
			for i in range(len(cur_course)):
				self.win.addnstr(
					self.input_field_y - 2 - i, self.input_field_x,
					cur_course[i],
					self.max_input_length
				)

	def update_selection(self, info):
		self.selected_channel = info[0] # 0 -> channel, 1 -> server
		self.show_all_messages()

	def get_input(self):
		tmp = self.input
		self.input = ''
		self.refresh_screen()

		self.new_message({
			"target": self.selected_channel, 
			"sender": "Me", 
			"msg": tmp
		})
		return tmp

	def add_char(self, char):
		self.input += char#.encode(self.code)
		self.refresh_screen()

	def refresh_screen(self):
		self.win.addnstr(
			self.input_field_y, self.input_field_x,
			' ' * self.max_input_length if len(self.input) == 0 else self.input,
			self.max_input_length
		)

def get_chat_window(stdscr):
	return ChatWindow(stdscr)