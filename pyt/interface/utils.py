import threading, datetime


def start_thread(func, callback=None):
	thread = threading.Thread(target=func, kwargs={} if callback == None else {'callback': callback})
	thread.daemon = True
	thread.start()

def get_date(frmt):
	return datetime.datetime.now().strftime(frmt)