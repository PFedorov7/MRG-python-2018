from aiohttp import web
from aiohttp import ClientSession
import requests
import threading
import urllib.request
from settings import get_config
import asyncio
import argparse
import pprint
import sys

async def handle(request):
	filename = request.match_info.get('file')
	if(filename.endswith('.')):

		new_filename  =  filename[0:-1]
		path_to_file = directory + new_filename

		t2 = Reader(path_to_file)
		t2.start()
		t2.join()

		return web.Response(text=t2.get_file())
	else:
		path_to_file = directory + filename

		t = Reader(path_to_file)
		t.start()
		t.join()

		if(t.get_file() == '404'):
			filename = filename + '.'
			counter = 0
			while(True):
				for item in nodes.values():
					t1 = loop.create_task(ask_nodes(filename, item))
					buff = await t1
					if(buff != '404'):
						t4 = Writer(buff, path_to_file)
						t4.start()
						t4.join()
						return buff
					else:
						counter += 1
						if (counter == len(nodes.values())):
							return web.Response(text='404')
		return web.Response(text=t.get_file())


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



async def ask_nodes(filename, item):
	async with ClientSession() as session:
		response =  await fetch(session, 'http://{}:{}/{}'.format(item['host'], item['port'], filename))
		if(response == '404'):
			return '404'
		return web.Response(text=response)

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

parser = argparse.ArgumentParser()
parser.add_argument ('--config', help=' put configuration to YAML path file')
res = parser.parse_args()
yaml = res.config

my_conf = get_config(yaml)
host = my_conf['storage']['self']['host']
port = my_conf['storage']['self']['port']
directory = my_conf['storage']['directory']
nodes = my_conf['storage']['nodes']

app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.get('/{file}', handle),
])

loop = asyncio.get_event_loop()
f = loop.create_server(app.make_handler(), host, port)
srv = loop.run_until_complete(f)

loop.run_forever()