import os.path

import connexion

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
app = connexion.AioHttpApp(__name__, specification_dir=_pkg_dir,
                           only_one_api=True, options={'swagger_ui': False})
_api = app.add_api('openapi.yaml')


def register_cleanup(func):
    _api.on_cleanup.append(lambda x: func())
