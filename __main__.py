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
    import config
    for i in range(len(paths)):
        sys.path.insert(0, paths[-i-1])
        imp.reload(config)
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
    if hasattr(config, 'header_regex') and \
            hasattr(config, 'header_translate'):
        configs['header_regex'] = getattr(config, 'header_regex')
        configs['header_translate'] = getattr(config, 'header_translate')

##########################
# Command-line Interface #
##########################

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

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
