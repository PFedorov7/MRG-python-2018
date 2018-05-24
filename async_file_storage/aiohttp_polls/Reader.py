import threading

class Reader(threading.Thread):
	
	def __init__(self, filename):
		threading.Thread.__init__(self)
		self.daemon = True
		self.filename = filename
		self.buf = ''

	def run(self):
		try:
			f = open(self.filename)
			self.buf = f.read()
			f.close()
		except FileNotFoundError:
			self.buf = '404'

	def get_file(self):
		return self.buf