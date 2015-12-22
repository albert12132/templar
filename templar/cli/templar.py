"""Command-line interface for templar."""

from templar.api import config
from templar.api import publish
from templar.exceptions import TemplarError
import templar

import argparse
import logging
import sys

LOGGING_FORMAT = '%(levelname)s %(filename)s:%(lineno)d> %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
log = logging.getLogger('templar')

def flags(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source',
                        help='Path to a source file with Markdown content.')
    parser.add_argument('-t', '--template',
                        help='Path to a Jinja template file')
    parser.add_argument('-d', '--destination',
                        help='Path to the destination file.')
    parser.add_argument('-c', '--config', default='config.py',
                        help='Path to a Templar configuration file.')
    parser.add_argument('--print', action='store_true',
                        help='Forces printing of result to stdout, '
                        'even if --destination is specified')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debugging messages.')
    parser.add_argument('--version', action='store_true',
                        help='Print the version number and exit')
    if args is not None:
        return parser.parse_args(args)
    return parser.parse_args()

def run(args):
    if args.version:
        print('Templar version {}'.format(templar.__version__))
        exit(0)

    log.setLevel(logging.DEBUG if args.debug else logging.ERROR)

    try:
        configuration = config.import_config(args.config)
        result = publish.publish(
                configuration,
                source=args.source,
                template=args.template,
                destination=args.destination,
                no_write=args.print)
    except TemplarError as e:
        if args.debug:
            raise
        else:
            print('{}: {}'.format(type(e).__name__, str(e)), file=sys.stderr)
            exit(1)
    else:
        if not args.destination or args.print:
            print(result)

def main():
    run(flags())

