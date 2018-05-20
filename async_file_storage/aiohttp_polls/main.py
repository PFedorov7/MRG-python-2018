from aiohttp import web
from aiohttp import ClientSession
import requests
import threading
from settings import get_config
import asyncio
import argparse
import pprint


async def handle(request):
	filename = request.match_info.get('file')
	if(filename.endswith('.')):
		try:
			new_filename  =  filename[0:-1]
			path_to_file = directory + new_filename
			file = open(path_to_file)
			my_buffer = file.read()
			return web.Response(text=my_buffer)
		except FileNotFoundError:
			return web.Response(text='404')
	else:
		try:
			path_to_file = directory + filename
			file = open(path_to_file)
			return web.Response(text=file.read())
		except FileNotFoundError:
			filename = filename + '.'
			threads = []
			t = threading.Thread(target=worker(filename))
			threads.append(t)
			t.start()


def worker(filename):
	second_loop = asyncio.new_event_loop()	
	tasks = asyncio.gather(
	 			* [ ask_nodes(filename, item) for item in nodes.values() ]
	 		)
	second_loop.run_until_complete(tasks)

async def ask_nodes(filename, item):
	async with ClientSession() as session:
		response =  await fetch(session, 'http://{}:{}/{}'.format(item['host'], item['port'], filename))
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