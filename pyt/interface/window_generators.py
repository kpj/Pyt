import curses, locale
from curses import panel

from pyt.interface import utils, constants
from pyt.config_handler import loader


class ChannelListWindow(object):
	def __init__(self, stdscr):
		(height, width) = stdscr.getmaxyx()
		self.win = curses.newwin(height, 40, 0, 0)
		self.win.immedok(True)

		self.panel = panel.new_panel(self.win)
		self.panel.hide()
		panel.update_panels()

		self.pos = 0
		self.items = []
		self.title = 'Channel list'

		self.theme = loader.load_theme()

		self.display()

	def navigate(self, shift):
		self.pos += shift
		if self.pos < 0:
			self.pos = 0
		elif self.pos >= len(self.items):
			self.pos = len(self.items) - 1

		self.display()

	def get_selection(self):
		return self.items[self.pos]

	def add_item(self, item):
		self.items.append(item)
		self.display()

	def display(self):
		self.panel.top()
		self.panel.show()
		self.win.clear()

		self.win.addstr(1, 1, self.title, curses.A_UNDERLINE)
		
		self.win.refresh()
		self.win.border(*self.theme['channel-border'])

		for index, item in enumerate(self.items):
			name = item[0]
			server = item[1]
			typ = item[2]

			if index == self.pos:
				mode = curses.A_REVERSE
			else:
				mode = curses.A_NORMAL

			msg = '%s' % str(name)
			self.win.addstr(3 + index, 1, msg, mode)


class ChatWindow(object):
	def __init__(self, stdscr):
		(height, width) = stdscr.getmaxyx()
		self.win = curses.newwin(height, width - 40, 0, 40)
		self.win.immedok(True)

		self.chat_history = {}

		self.input = ''

		self.theme = loader.load_theme()

		self.max_input_length = width - 20;
		self.input_field_x = len(self.theme["prompt"]) + 1
		self.input_field_y = height - 2
		self.win.addstr(
			self.input_field_y,
			self.input_field_x - 1 - len(self.theme["prompt"]), 
			self.theme["prompt"]
		)

		self.win.border(*self.theme['chat-border'])

		locale.setlocale(locale.LC_ALL, '')
		self.code = locale.getpreferredencoding()

		self.selected_channel = None

	def new_message(self, data):
		if not data["target"] in self.chat_history.keys():
			self.chat_history[data["target"]] = []
			
		self.chat_history[data["target"]].insert(
			0, 
			self.theme["chat-line"] % (
				utils.get_date(self.theme["date-format"]), 
				data["sender"], 
				data["msg"]
			)
		)
		
		self.show_all_messages()

	def show_all_messages(self):
		self.refresh_screen()

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
		self.refresh_input()

		if len(tmp) > 0:
			self.new_message({
				"target": self.selected_channel, 
				"sender": "Me", 
				"msg": tmp
			})

		return tmp

	def add_char(self, char):
		self.input += char#.encode(self.code)
		self.refresh_input()

	def rm_last_char(self):
		self.input = self.input[:-1]
		self.refresh_input()

	def refresh_screen(self):
		self.win.clear()

		self.win.border(*self.theme['chat-border'])
		self.win.addstr(
			self.input_field_y,
			self.input_field_x - len(self.theme["prompt"]), 
			self.theme["prompt"]
		)

	def refresh_input(self):
		self.win.addnstr(
			self.input_field_y, self.input_field_x,
			self.input + ' ' * (self.max_input_length - len(self.input)),
			self.max_input_length
		)


def get_chat_window(stdscr):
	return ChatWindow(stdscr)

def get_channel_list_window(stdscr):
	return ChannelListWindow(stdscr)