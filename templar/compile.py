######################################################################
# compile.py
#
# Author: Albert Wu
#
# Compiler for 61A TA repo. Supports template inheritance and embedded
# Python.
#
######################################################################

import re
import argparse
import os
import templar.link as link
from templar.markdown import Markdown


##############
# Public API #
##############

def compile(template_path, attrs):
    # process template inheritance first
    templates = get_all_templates(template_path, [], attrs['TEMPLATE_DIRS'])
    templates.reverse()
    template = compile_inheritance(templates)

    while expr_re.search(template):
        for tag in expr_re.findall(template):
            if tag in attrs:
                val = attrs[tag]
            else:
                try:
                    val = eval(tag, attrs)
                except:
                    val = ''
            template = re.sub('\{\{\s.+?\s\}\}', str(val), template,
                              count=1)
    return template

##################
# REGEX PATTERNS #
##################

extend_tag_re = re.compile(r'<%\s*extends\s*(.+?)\s*%>\n')

super_open_re= re.compile(r'<%\s*(.+?)\s*%>')
super_close_re = re.compile(r'<%/\s*(.+?)\s*%>')

sub_tag_re = re.compile('\{%\s*(.+?)\s*%\}')

expr_re = re.compile('\{{2}\s*(.+?)\s*\}{2}')

#####################
# TEMPLATE RETRIEVAL #
#####################

def get_template(filename, template_dirs):
    """Return the contents of `filename` as a string.

    PARAMETERS:
    filename -- string: name of template file relative to a 'template'
                directory

    BEHAVIOR:
    `filename` should be of the format:

        [<app>:]<filepath>

    The filepath is expected to be a relative path to a template file
    (usually an html template). If <app> is provided, `get_template`
    will look only in that app's template directory. Otherwise,
    `get_template` will look through the list TEMPLATE_DIRS in order,
    and search in a directory called 'templates' in each of them for
    `filename`.

    By default, the repo home directory is searched first,
    before any app directories.

    If no such `filename` is found, the program exits with status 1.
    """
    if ':' in filename:
        app, filename = filename.split(':')
        dirs = [path for path in template_dirs if app in path]
    else:
        dirs = template_dirs
    for path in dirs:
        template = os.path.join(path, 'templates', filename)
        if os.path.exists(template):
            with open(template, 'r') as f:
                contents = f.read()
            return contents
    print(filename + ' could not be found in:')
    for path in dirs:
        print(os.path.join(path, 'templates'))
    exit(1)


def get_all_templates(filename, templates, template_dirs):
    """Get all templates referenced in an inheritance hierarchy.

    PARAMETERS:
    filename  -- string: the most immediate template.
    templates -- list: a pre-existing (possibly empty) list of
                 templates (contents, not filepaths). `templates` will
                 be mutated to contain all templates in the hierarchy.

    RETURNS:
    list: `templates`, now containing contents of all inherited
    templates. The hierarchy the root (base template) comes first, and
    the children come after it.

    EXCEPTIONS:
    Exits with status 1 if improper inheritance syntax is encountered.
    """
    contents = get_template(filename, template_dirs)
    match = extend_tag_re.match(contents)
    if match:
        contents = contents[len(match.group(0)):]
        parent = match.group(1)
        get_all_templates(parent, templates, template_dirs)
    templates.append(contents)
    return templates

########################
# INHERITANCE COMPILER #
########################


def list_supers(template):
    """Return a dictionary where keys are tags inherited by the
    template, and values are lists of lines that correspond to each
    tag.

    PARAMETERS:
    template -- a single string. Inheritance tags should be on their
                own line. Inheritance tags cannot be nested -- if they
                are, the inner tags will be treated as plain text.

    RETURNS:
    A dictionary, where keys are tags and values are lists of lines
    associated with each tag. The lines do NOT end in newline
    characters.

    >>> t = '<% t1 %>\\nhello\\nthere dog\\n<%/ t1 %>'
    >>> list_supers(t)
    {'t1': ['hello', 'there dog']}
    >>> t = '<% t1 %>\\n<%/ t1 %>\\n<% t2 %>\\nhello\\n<%/ t2 %>'
    >>> list_supers(t)
    {'t2': ['hello'], 't1': []}
    >>> t = '<% t1 %>\\n<% t2 %>\\n<%/ t2 %>\\n<%/ t1 %>'
    >>> list_supers(t)
    {'t1': ['<% t2 %>', '<%/ t2 %>']}
    """
    supers = {}
    tag = None
    for line in template.split('\n'):
        open_match = super_open_re.match(line)
        close_match = super_close_re.match(line)
        if open_match and tag is None:
            tag = open_match.group(1)
            supers[tag] = []
        elif close_match and close_match.group(1) == tag:
            tag = None
        elif tag:
            supers[tag].append(line)
    return supers


def compile_inheritance(templates):
    """Compiles the inheritance chain of templates into a single
    template.

    PARAMETERS:
    templates -- a list of templates. The sub-template
                 should be first, and the super-templates (parents)
                 should be ordered after. In addition, each template
                 should be a single string.

    RETURNS:
    A single template (as a string). The template will be devoid of
    inheritance tags.

    DESCRIPTION:
    Compilation begins at the top of the template chain and works
    its way down to child templates. This allows child templates to
    inherit not just from parents, but from higher ancestors as well.

    If a sub-template decides not to inherit a tag in its
    super-template, that tag will be removed in the final result.

    >>> t = ['<% t1 %>\\nhello\\n<%/ t1 %>', '{% t1 %}']
    >>> compile_inheritance(t)
    'hello'
    >>> t = ['<% t2 %>\\nhello\\n<%/ t2 %>', '<% t1 %>\\n{% t2 %}\\n<%/ t1 %>', '{% t1 %}']
    >>> compile_inheritance(t)
    'hello'
    >>> t = ['<% t2 %>\\nhello\\n<%/ t2 %>', '<% t1 %>\\nbye\\n<%/ t1 %>', '{% t1 %}{% t2 %}']
    >>> compile_inheritance(t)
    'byehello'
    >>> t = ['<% t1 %>\\nbye\\n<%/ t1 %>', '{% t1 %}{{ hi }}{% t2 %}']
    >>> compile_inheritance(t)
    'bye{{ hi }}'
    """
    if len(templates) == 1:
        return re.sub('\{%\s.+?\s%\}', '', templates[0])
    super_temp, sub_temp = templates.pop(), templates.pop()
    supers = list_supers(sub_temp)
    seen = set()
    for match in sub_tag_re.finditer(super_temp):
        tag = match.group(1)
        if tag not in supers or tag in seen:
            continue
        replace = '\n'.join(supers[tag])
        super_temp = re.sub('\{%\s*' + tag + '\s*%\}', replace,
                            super_temp)
        seen.add(tag)
    templates.append(super_temp)
    return compile_inheritance(templates)


##########################
# COMMAND LINE UTILITIES #
##########################

def cmd_options(parser):
    parser.add_argument('template', help="The template's filename")
    parser.add_argument('-s', '--source', type=str, default=None,
                        help="A Markdown file with content.")
    parser.add_argument('-d', '--destination', type=str, default=None,
                        help='The destination filepath')
    parser.add_argument('-m', '--markdown', action='store_true',
                        help='Use Markdown conversion on source')
    parser.add_argument('-c', '--conditions', action='append',
                        help='Specify conditions for substitutions')

def main(args, configs):
    if args.source:
        if not os.path.exists(args.source):
            print('File ' + args.source + ' does not exist.')
            exit(1)
        elif not os.path.isfile(args.source):
            print(args.source + ' is not a valid file')
            exit(1)
        with open(args.source, 'r') as f:
            result = link.link(f.read())
        if args.markdown:
            markdown_obj = Markdown(result)
            for k, v in markdown_obj.variables.items():
                configs[k] = v
            result = markdown_obj.text
        result = link.substitutions(result,
                                    configs.get('SUBSTITUTIONS', []),
                                    args)
        result, cache = link.retrieve_blocks(result)
        if 'TOC_BUILDER' in configs:
            configs['table-of-contents'] = link.scrape_headers(result, configs['TOC_BUILDER'])
            for import_stmt in (
                    'from datetime import datetime',
                    ):
                exec(import_stmt, configs)
        for k, v in cache.items():
            configs[k] = v

    result = compile(args.template, configs)
    if not args.destination:
        print(result)
        return
    with open(args.destination, 'w') as f:
        f.write(result)
        print('Finished compiling')
        print('Result can be found at ' + args.destination)

if __name__ == '__main__':
    print('Usage: python3 __main__ compile ...')
