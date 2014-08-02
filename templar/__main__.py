import argparse
import importlib.machinery
import os
import sys
from templar import compile, link, markdown, log

VARIABLES = 'VARIABLES'
CONFIG_NAME = 'config.py'

##############
# Public API #
##############

def get_paths(templar_path, source_path):
    """Retrieves a list of paths to search depending on templar_path
    (the filepath of this file) and source_path (the filepath of the
    source directory/file).

    PARAMETERS:
    templar_path -- str; filepath of Templar
    source_path  -- str; filepath of the source directory/file

    Templar first determines the least common ancestor of templar_path
    and source_path. The resulting list of paths will be all paths
    from the ancestor to source_path, starting from the ancestor to
    source_path.

    RETURNS:
    list of str; a list of filepaths, starting with the ancestor and
    ending at source_path.
    """
    paths = []
    while not templar_path.startswith(source_path):
        paths.append(source_path)
        source_path = os.path.dirname(source_path)
    paths.append(source_path)
    paths.reverse()
    return paths

def configure(paths):
    """For each filepath in paths, search for a file called config.py
    and add its configuration variables if the file exists.

    PARAMETERS:
    paths -- list of str; a list of filepaths to search. Search goes
             through the list starting from the first index.

    If two filepaths have the same variable in their respective
    config.py, the filepath that is processed later will overwrite the
    filepath that is processed earlier.

    RETURNS:
    dict; configuration dictionary with the following key-value pairs:

    TEMPLATE_DIRS
    SUBSTITUTIONS
    VARIABLES
    TOC_BUILDER
    """
    configs = {VARIABLES: {}}
    root = paths[0]
    for path in paths:
        sys.path.insert(0, path)
        if not file_exists(os.path.join(path, CONFIG_NAME)):
            continue
        extract_configs(import_config(path, root), configs)
    return configs

###########################
# Configuration utilities #
###########################

def import_config(path, root):
    """Imports a file called config.py that is located in the directory
    denoted by the parameter PATH.

    PARAMETERS:
    path -- str; directory in which config.py is located. The directory
            is assumed to contain a config.py file; any validation
            should be made before calling this function.

    RETURNS:
    module; the imported config.py module.
    """
    path = os.path.join(path, 'config.py')
    loader = importlib.machinery.SourceFileLoader(path, path)
    return loader.load_module().configurations

def extract_configs(source, dest):
    """Extract conifguration variables from config and place them in
    configs.

    PARAMETERS:
    source -- dict; a source of configuration variables
    dest   -- dict; destination for configuration variables

    DESCRIPTION:
    source is not assumed to have any contents. However, the only
    contents in source that are copied over to dest are the
    following:

    VARIABLES     -- dict; contains variables as key-value pairs. The
                     key-value pairs in source will be copied over
                     to the VARIABLES key in dest.
    SUBSTITUTIONS -- list of tuples; a sequence of
                     (regex, substitution) groups. The substitutions
                     in source are appended to the list of
                     substitutions in dest
    TEMPLATE_DIRS -- list of str; a sequence of filepaths in which
                     to look for templates
    TOC_BUILDER   -- utils.core.TableOfContents; an object that parses
                     table of contents.

    If any of these keys already exist in dest, their values will be
    overwritten by the value in source.
    """
    for k, v in source.get('VARIABLES', {}).items():
        dest[VARIABLES][k] = v
    for lst in ('SUBSTITUTIONS', 'TEMPLATE_DIRS'):
        new = source.get(lst, [])
        dest.setdefault(lst, []).extend(new)
    for obj in ('TOC_BUILDER',):
        if obj in source:
            dest[obj] = source[obj]

def file_exists(path):
    return os.path.exists(path)

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
    dest = os.path.join(path, CONFIG_NAME)
    config = os.path.join(os.path.dirname(__file__), CONFIG_NAME)
    with open(config, 'r') as f:
        template = f.read()
    if os.path.exists(path) and (not os.path.exists(dest) \
            or 'y' in input('Remove existing {}? [y/n] '.format(CONFIG_NAME)).lower()):
        with open(dest, 'w') as f:
            f.write(template)
        log.info('Copied ' + CONFIG_NAME + ' to ' + dest)
        exit(0)
    else:
        log.warn(CONFIG_NAME + ' not copied')
        exit(1)

def main():
    paths = get_paths(os.path.abspath(__file__), os.getcwd())

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    markdown_parser = subparsers.add_parser('markdown')
    markdown.cmd_options(markdown_parser)
    markdown_parser.set_defaults(func=markdown.main)

    link_parser = subparsers.add_parser('link')
    link.cmd_options(link_parser)
    link_parser.set_defaults(
            func=lambda args: link.main(args, configure(paths)))

    compile_parser = subparsers.add_parser('compile')
    compile.cmd_options(compile_parser)
    compile_parser.set_defaults(
            func=lambda args: compile.main(args, configure(paths)))

    config_parser = subparsers.add_parser('config')
    config_cmd_options(config_parser)
    config_parser.set_defaults(func=config_main)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
