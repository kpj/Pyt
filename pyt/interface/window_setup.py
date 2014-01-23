import curses

from pyt.interface import window_generators, utils, constants

from pyt.chat_handler import irc_wrapper, xmpp_wrapper


def setup(stdscr, stdout):
	def communicator(type, data):
		if type == "add_item":
			chan_win.add_item(data)
			if len(chan_win.items) == 1:
				# TODO: do this the proper way
				chat_win.update_selection(chan_win.get_selection())
		elif type == "recv_msg":
			chat_win.new_message(data)


	curses.curs_set(0) # disable cursor
	stdscr.immedok(True)
	stdscr.clear()
	constants.init_colors()

	chan_win = window_generators.get_channel_list_window(stdscr)
	chat_win = window_generators.get_chat_window(stdscr)

	# add stdout/err channel
	stdout.set_callback(communicator)
	communicator("add_item", ('stdout', None, 'internal'))

	utils.start_thread(irc_wrapper.init_connection, communicator) # irc thread
	utils.start_thread(xmpp_wrapper.init_connection, communicator) # xmpp thread


	# I/O thread
	while 1:
		key = stdscr.getch()

		# navigate menu
		if key == curses.KEY_UP:
			chan_win.navigate(-1)
			chat_win.update_selection(chan_win.get_selection())
		elif key == curses.KEY_DOWN:
			chan_win.navigate(1)
			chat_win.update_selection(chan_win.get_selection())
		# send message
		elif key == curses.KEY_ENTER or key == ord('\n'):
			sel = chan_win.get_selection()
			typ = sel[2]
			if typ == 'irc':
				irc_wrapper.send_privmsg(chat_win.get_input(), sel)
			elif typ == 'xmpp':
				xmpp_wrapper.send_privmsg(chat_win.get_input(), sel)
		# delet last char
		elif key == curses.KEY_BACKSPACE:
			chat_win.rm_last_char()
		#write message
		else:
			chat_win.add_char(chr(key))