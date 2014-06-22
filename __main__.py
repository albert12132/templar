import compile
import link
import markdown

import argparse
import imp
import os
import sys


def configure_path():
    configs = {}
    cwd = os.getcwd()
    templar = os.path.abspath(__file__)
    paths = []
    while not templar.startswith(cwd):
        paths.append(cwd)
        cwd = os.path.dirname(cwd)
    root = cwd
    paths.append(root)
    sys.path.insert(0, root)
    for path in paths:
        path = path.replace(root, '').replace('/', '.') + '.config'
        path = path.strip('.')
        config = importlib.import_module(path)
        extract_configs(config, configs)
    return configs

def extract_configs(config, configs):
    for dct in ('VARIABLES',):
        if hasattr(config, dct):
            new = getattr(config, dct)
            for k, v in new.items():
                configs[k] = v
    for lst in ('SUBSTITUTIONS', 'TEMPLATE_DIRS'):
        if hasattr(config, lst):
            new = getattr(config, lst)
            configs.setdefault(lst, []).extend(new)
    if hasattr(config, 'table_of_contents') and \
            hasattr(config, 'header_regex') and \
            hasattr(config, 'header_translate'):
        configs['table_of_contents'] = getattr(config, 'table_of_contents')
        configs['header_regex'] = getattr(config, 'header_regex')
        configs['header_translate'] = getattr(config, 'header_translate')


##########################
# Command-line Interface #
##########################

def config_cmd_options(parser):
    parser.add_argument('-p', '--path', type=str,
                        help="Add config.py to specified path")

def config_main(args, configs=None):
    if args.path:
        path = args.path
    else:
        path = os.getcwd()
    path = os.path.join(path, 'config.py')
    config = os.path.join(os.path.dirname(__file__), 'config.py')
    with open(config, 'r') as f:
        template = f.read()
    if not os.path.exists(path) or \
            'y' in input('Remove existing config.py? [y/n] ').lower():
        with open(path, 'w') as f:
            f.write(template)
        print('Copied config.py to', path)
        exit(0)
    else:
        print('config.py not copied')
        exit(1)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    markdown_parser = subparsers.add_parser('markdown')
    markdown.cmd_options(markdown_parser)
    markdown_parser.set_defaults(func=markdown.main)

    link_parser = subparsers.add_parser('link')
    link.cmd_options(link_parser)
    link_parser.set_defaults(func=link.main)

    compile_parser = subparsers.add_parser('compile')
    compile.cmd_options(compile_parser)
    compile_parser.set_defaults(func=compile.main)

    config_parser = subparsers.add_parser('config')
    config_cmd_options(config_parser)
    config_parser.set_defaults(func=config_main)

    args = parser.parse_args()

    configs = configure_path()
    args.func(args, configs)

if __name__ == '__main__':
    main()
