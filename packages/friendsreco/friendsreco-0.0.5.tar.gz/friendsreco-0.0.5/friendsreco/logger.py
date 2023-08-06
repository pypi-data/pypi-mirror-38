import logging
import logging.config
import sys


class ColorFormatter(logging.Formatter):
    BLUE = '\033[1;94m'
    GREEN = '\033[1;92m'
    YELLOW = '\033[1;93m'
    RED = '\033[1;91m'
    END_TAG = '\033[0m'

    def format(self, record):
        message = logging.Formatter.format(self, record)

        if record.levelno == logging.DEBUG:
            return self.BLUE + message + self.END_TAG

        elif record.levelno == logging.INFO:
            return self.GREEN + message + self.END_TAG

        elif record.levelno == logging.WARNING:
            return self.YELLOW + message + self.END_TAG

        elif record.levelno == logging.ERROR:
            return self.RED + message + self.END_TAG


def configure(debug=False):
    formatter_str = '[ %(asctime)s ][ %(levelname)s ][ %(name)s ] %(message)s'

    config = {
        'version': 1,
        'formatters': {
            'color': {
                '()': 'friendsreco.logger.ColorFormatter',
                'fmt': formatter_str
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'color'
            }
        },
        'root': {
            'level': 'DEBUG' if debug else 'INFO',
            'handlers': ['console']
        }
    }

    logging.config.dictConfig(config)
