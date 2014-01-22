import threading


def start_thread(func, callback=None):
	thread = threading.Thread(target=func, kwargs={} if callback == None else {'callback': callback})
	thread.daemon = True
	thread.start()