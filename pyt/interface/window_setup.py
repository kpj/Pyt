import curses

from pyt.interface import window_generators, utils

from pyt.chat_handler import irc_wrapper


def setup(stdscr):
	def communicator(type, data):
		if type == "add_item":
			chan_win.menu.add_item(data)
			if len(chan_win.menu.items) == 1:
				# TODO: do this the proper way
				chat_win.update_selection(chan_win.menu.get_selection())
		elif type == "recv_msg":
			chat_win.new_message(data)


	curses.curs_set(0)

	stdscr.immedok(True)
	stdscr.clear()

	chan_win = window_generators.get_channel_list_window(stdscr)

	utils.start_thread(irc_wrapper.init_connection, communicator) # irc thread

	chat_win = window_generators.get_chat_window(stdscr)

	# I/O thread
	while 1:
		key = stdscr.getch()

		# navigate menu
		if key == curses.KEY_UP:
			chan_win.menu.navigate(-1)
			chat_win.update_selection(chan_win.menu.get_selection())
		elif key == curses.KEY_DOWN:
			chan_win.menu.navigate(1)
			chat_win.update_selection(chan_win.menu.get_selection())
		# send message
		elif key == curses.KEY_ENTER or key == ord('\n'):
			irc_wrapper.send_privmsg(chat_win.get_input(), chan_win.menu.get_selection())
		#write message
		else:
			chat_win.add_char(chr(key))