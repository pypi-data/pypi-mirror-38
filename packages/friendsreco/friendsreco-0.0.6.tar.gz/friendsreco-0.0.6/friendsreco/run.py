import argparse
import asyncio
import logging

import uvloop

from .api import Api
from .logger import configure as configure_logging

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parser = argparse.ArgumentParser(description='Friends Recommendations API')
parser.add_argument('--neo4j-url', '-n', type=str, required=True)
parser.add_argument('--port', '-p', type=int, default=8080)
parser.add_argument('--no-initial-friendships', '-i', action='store_false')
parser.add_argument('--debug', '-d', action='store_true')

args = parser.parse_args()

configure_logging(args.debug)

api = Api(args.neo4j_url, args.no_initial_friendships)


def main():
    from .app import app, register_cleanup

    register_cleanup(api.cleanup)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(api.start())

    app.run(port=args.port,
            access_log=logging.getLogger('friendsreco.access'))
