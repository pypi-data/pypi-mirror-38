import connexion
import os.path
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
app = connexion.AioHttpApp(__name__, specification_dir=_pkg_dir,
                           only_one_api=True, options={'swagger_ui': False})
api = app.add_api('openapi.yaml')
