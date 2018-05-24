from aiohttp import web
from aiohttp import ClientSession
import requests
import threading
import urllib.request
from Settings import get_config
import asyncio
import argparse
import pprint
import sys

import Reader
import Writer

async def handle(request):
	filename = request.match_info.get('file')

	# This sign '..' indicates that this request came from a neighboring server
	if(filename.endswith('..')):

		new_filename  =  filename[0:-2]
		path_to_file = directory + new_filename

		t2 = Reader.Reader(path_to_file)
		t2.start()
		t2.join()

		return web.Response(text=t2.get_file())
	else:
		path_to_file = directory + filename

		t = Reader.Reader(path_to_file)
		t.start()
		t.join()

		if(t.get_file() == '404'):
			filename = filename + '..'
			counter = 0
			while(True):
				for item in nodes.values():
					t1 = loop.create_task(ask_nodes(filename, item, path_to_file))
					buff = await t1
					if(buff != '404'):
						return buff
					else:
						#if all servers answer 404
						counter += 1
						if (counter == len(nodes.values())):
							return web.Response(text='404')
		else:
			return web.Response(text=t.get_file())


async def ask_nodes(filename, item, path_to_file):
	async with ClientSession() as session:
		response =  await fetch(session, 'http://{}:{}/{}'.format(item['host'], item['port'], filename))
		if(response == '404'):
			return '404'

		t4 = Writer.Writer(response, path_to_file)
		t4.start()
		t4.join()

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