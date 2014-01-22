import curses
from curses import panel


class Menu(object):
	def __init__(self, title, items, window):
		self.win = window

		self.panel = panel.new_panel(self.win)
		self.panel.hide()
		panel.update_panels()

		self.pos = 0
		self.items = items
		self.title = title

	def navigate(self, shift):                                                   
		self.pos += shift                                                   
		if self.pos < 0:                                                
			self.pos = 0                                                
		elif self.pos >= len(self.items):                               
			self.pos = len(self.items) - 1

	def get_selection(self):
		return self.items[self.pos]

	def add_item(self, item):
		self.items.append(item)

	def display(self):
		self.panel.top()                                                     
		self.panel.show()                                                    
		self.win.clear()

		self.win.addstr(1, 1, self.title, curses.A_UNDERLINE)
		while True:                                                          
			self.win.refresh()                                            
			curses.doupdate()                                                
			for index, item in enumerate(self.items):                        
				if index == self.pos:                                   
					mode = curses.A_REVERSE                                  
				else:                                                        
					mode = curses.A_NORMAL                                   

				msg = '%s' % str(item[0])
				self.win.addstr(3 + index, 1, msg, mode)