import threading

class Writer(threading.Thread):

	def __init__(self, buf, path):
		threading.Thread.__init__(self)
		self.daemon = True
		self.path = path
		self.buf = buf

	def run(self):
		f = open(self.path, "w")
		f.write(self.buf)
		f.close()