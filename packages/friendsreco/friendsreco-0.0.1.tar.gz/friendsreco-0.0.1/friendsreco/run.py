import argparse
import logging

import yaml

from friendsreco.app import app

parser = argparse.ArgumentParser(description='Friends Recommendations API')
parser.add_argument('--port', '-p', type=int, default=8080)

def main():
    args = parser.parse_args()
    app.run(port=args.port,
            access_log=logging.getLogger('friendsreco.access'))
