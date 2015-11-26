"""Command-line interface for templar."""

from templar.api import config
from templar.api import publish

import argparse
import logging

LOGGING_FORMAT = '%(levelname)s %(filename)s:%(lineno)d> %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
log = logging.getLogger('templar')

def flags():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source',
                        help='Path to a source file with Markdown content.')
    parser.add_argument('-t', '--template',
                        help='Path to a Jinja template file')
    parser.add_argument('-d', '--destination',
                        help='Path to the destination file.')
    parser.add_argument('-c', '--config', default='config.py',
                        help='Path to a Templar configuration file.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debugging messages.')
    return parser.parse_args()

def run(args):
    log.setLevel(logging.DEBUG if args.debug else logging.ERROR)

    configuration = config.import_config(args.config)
    result = publish.publish_file(configuration, args.source, args.template)

    if args.destination:
        with open(args.destination, 'w') as f:
            f.write(result)
    else:
        print(result)

def main():
    run(flags())

