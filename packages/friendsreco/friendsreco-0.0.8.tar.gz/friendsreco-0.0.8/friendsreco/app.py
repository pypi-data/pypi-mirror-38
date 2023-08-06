import logging
import os.path

import connexion
from aiohttp import web

_logger = logging.getLogger('friendsreco.app')


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response

    except Exception as error:
        _logger.exception('{}: {}'.format(type(error), error))
        raise web.HTTPInternalServerError()


options = {'swagger_ui': False}
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
app = connexion.AioHttpApp(__name__, specification_dir=_pkg_dir,
                           only_one_api=True, options=options)
_api = app.add_api('openapi.yaml')
_api.middlewares.append(error_middleware)


def register_cleanup(func):
    _api.on_cleanup.append(lambda x: func())
