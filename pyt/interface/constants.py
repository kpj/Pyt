import curses


def init_colors():
	global IRC_CHAN, XMPP_CHAN

	IRC_CHAN = 1
	curses.init_pair(IRC_CHAN, curses.COLOR_RED, curses.COLOR_BLACK)

	XMPP_CHAN = 2
	curses.init_pair(XMPP_CHAN, curses.COLOR_GREEN, curses.COLOR_BLACK)