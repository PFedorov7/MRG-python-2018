from views import handle
from aiohttp import web

def setup_routes(app):
	app.add_routes([
	    web.get('/', handle),
	    web.get('/{file}', handle),
	])