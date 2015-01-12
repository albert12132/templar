######################################################################
# compile.py
#
# Author: Albert Wu
#
# Supports template inheritance and embedded Python.
######################################################################

import argparse
import os
import re
import traceback
import templar.link as link
from templar import log
from templar.markdown import Markdown


##############
# Public API #
##############

def compile(template_path, config):
    template = process_inheritance(template_path,
                                   config['TEMPLATE_DIRS'])
    return process(template, config['VARIABLES'])

def process_inheritance(template_path, template_dirs):
    templates = get_all_templates(template_path, [], template_dirs)
    templates.reverse()
    return compile_inheritance(templates)

def process(template, attrs):
    if not isinstance(attrs, Frame):
        attrs = Frame(bindings=attrs)
    template, macros = process_def(template)
    template = process_call(template, attrs, macros)
    template = process_control(template, attrs)
    while expr_re.search(template):
        template = expr_re.sub(lambda m: str(evaluate(m.group(1),
                                                      attrs)),
                               template)
    return template

##################
# REGEX PATTERNS #
##################

extend_re = re.compile(r"""
    \A<%                # extend must be first line in file
        \s*extends\s+
        (.+?)           # \1 is superclass template
    \s*%>\n
""", re.S | re.X)

super_re= re.compile(r"""
    (<%                 # \1 is block tag
        \s*block\s+
        (.+?)           # \2 is block name
    \s*%>)
    (.*?)               # \3 is block contents
    \1                  # closing block tag
""", re.S | re.X)

sub_re = re.compile(r"""
    \{%
        \s*block\s+
        (.+?)           # \1 is block name
    \s*%\}
""", re.S | re.X)

expr_re = re.compile(r"""
    \{{2}\s*
        (.+?)           # \1 is expression
    \s*\}{2}
""", re.S | re.X)

for_re = r"""
    \{%                     # opening brace
        \s*(for)\s*         # \1 is for keyword
        (                   # \2 is variable list
            (?:
                \{{2}\s*    # variable is of the form {{ var }}
                .*?         # variable name
                \s*\}{2}
                \s*,?\s*    # comma
            )+              # one or more variables
        )
        \s*in\s*
        \{{2}\s*
            (.*?)           # \3 is the iterable
        \s*\}{2}
    \s*%\}
    (.*?)                   # \4 is loop body
    \{%                     # closing brace
        \s*endfor\s*
    %\}
"""

def_re = re.compile(r"""
    \{%                     # opening brace
        \s*def\s+
        (\w+)               # \1 is the macro name
        \s*
        (                   # \2 is variable list
            (?:
                \{{2}\s*    # variable is of the form {{ var }}
                .*?         # variable name
                \s*\}{2}
                \s*,?\s*    # comma
            )+              # one or more variables
        )
    \s*%\}
    (.*?)                   # \3 is macro body
    \{%                     # closing brace
        \s*enddef\s*
    %\}
""", re.S | re.X)

call_re = re.compile(r"""
    \{%
        \s*call\s+
        (\w+)               # \1 is macro name
        \s*
        (                   # \2 is variable list
            (?:
                \{{2}\s*    # argument is of the form {{ var }}
                .*?         # argument
                \s*\}{2}
                \s*,?\s*    # comma
            )+              # one or more arguments
        )
    \s*%\}
""", re.S | re.X)

def conditional_re(keyword):
    return r"""
    \{%                 # brace
        \s*(""" + keyword + r""")\s*      # \1 is brace type
        (?:
            \{{2}\s*    # conditional is of the form {{ cond }}
                (.*?)   # \2 is conditional
            \s*\}{2}
        )?
    \s*%\}
    (.*?)               # \3 is body
    """
if_re = conditional_re('if') + \
    '(?:' + conditional_re('elif') + ')*' + \
    '(?:' + conditional_re('else') + ')?' + \
    r'\{%\s*endif\s*%\}'

########################
# TEMPLATE COMPILATION #
########################

def process_control(template, attrs):
    control_re = re.compile(for_re + '\n|\n' + if_re, re.S | re.X)
    def control_sub(match):
        if match.group(1) == 'for':
            return process_for(match, attrs)
        elif match.group(5) == 'if':
            return process_if(match, attrs)
    return control_re.sub(control_sub, template)

def process_for(match, attrs):
    match = re.match(for_re, match.group(0), flags=re.S | re.X)
    variables = expr_re.findall(match.group(2).replace('\n', ' '))
    iterable = evaluate(match.group(3), attrs)
    text = ''
    for elem in iterable:
        new_frame = Frame(parent=attrs)
        if type(elem) == str or not hasattr(elem, '__iter__'):
            elem = (elem,)
        for var, val in zip(variables, elem):
            new_frame[var] = val
        text += process(match.group(4), new_frame).strip() + '\n'
    return text

def process_if(match, attrs):
    cond_re = re.compile(conditional_re('if|elif|else') + \
            '\n\\n(?=\{%\s*(?:elif|else|endif))', re.S | re.X)
    for keyword, cond, body in cond_re.findall(match.group(0)):
        if keyword == 'else':
            return process(body, attrs).strip()
        elif is_true(cond, attrs):
            return process(body, attrs).strip()
    return ''

def process_call(template, attrs, macros):
    def call_sub(match):
        macro, arguments = match.groups()
        arguments = expr_re.findall(arguments)
        if macro not in macros:
            log.warn('The macro "' + macro + '" is not defined.')
            return ''
        variables, body = macros[macro]
        new_frame = Frame(parent=attrs)
        for var, arg in zip(variables, arguments):
            new_frame[var] = evaluate(arg, attrs)
        return expr_re.sub(lambda m: eval_macro_body(m, new_frame), body.strip('\n'))
    def eval_macro_body(match, attrs):
        result = evaluate(match.group(1), attrs)
        if not result:
            return match.group(0)
        return str(result)
    return call_re.sub(call_sub, template)

def process_def(template):
    macros = {}
    for macro, variables, body in def_re.findall(template):
        variables = expr_re.findall(variables.replace('\n', ' '))
        macros[macro] = (variables, body)
    template = def_re.sub('', template)
    return template, macros


def is_true(expression, attrs):
    if evaluate(expression, attrs):
        return True
    else:
        return False

class Frame:
    def __init__(self, bindings=None, parent=None):
        self.parent = parent
        if bindings:
            self.bindings = bindings
        else:
            self.bindings = {}

    def __getitem__(self, variable):
        if variable in self.bindings:
            return self.bindings[variable]
        elif self.parent:
            return self.parent[variable]
        try:
            return eval(variable)
        except:
            raise KeyError(variable)

    def __contains__(self, variable):
        variable = variable.replace('\n', ' ').strip()
        return variable in self.bindings or \
                self.parent and variable in self.parent

    def __setitem__(self, variable, value):
        self.bindings[variable] = value

def evaluate(expression, attrs):
    expression = expression.replace('\n', ' ').strip()
    if expression in attrs:
        return attrs[expression]
    else:
        try:
            return eval(expression, {}, attrs)
        except Exception as e:
            log.warn('"{}" caused {}: {}'.format(expression,
                e.__class__.__name__, e))
            traceback.print_exc()
            return ''



######################
# TEMPLATE RETRIEVAL #
######################

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
        if file_exists(template):
            return file_read(template)
    log.warn('The template "' + filename \
            + '" could not be found in these directories:')
    for path in dirs:
        log.log(os.path.join(path, 'templates'))
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
    match = extend_re.match(contents)
    if match:
        contents = contents[len(match.group(0)):]
        parent = match.group(1)
        get_all_templates(parent, templates, template_dirs)
    templates.append(contents)
    return templates

########################
# TEMPLATE INHERITANCE #
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

    >>> t = '<% block t1 %>\\nhello\\nthere dog\\n<% block t1 %>'
    >>> list_supers(t)
    {'t1': 'hello\\nthere dog'}
    >>> t = '<% block t1 %>\\n<% block t1 %>\\n<% block t2 %>\\nhello\\n<% block t2 %>'
    >>> list_supers(t)
    {'t2': 'hello', 't1': ''}
    >>> t = '<% block t1 %>\\n<% block t2 %>\\n<% block t2 %>\\n<% block t1 %>'
    >>> list_supers(t)
    {'t1': '<% block t2 %>\\n<% block t2 %>'}
    """
    supers = {}
    tag = None
    for _, name, contents in super_re.findall(template):
        supers[name] = contents.strip()
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
        return sub_re.sub('', templates[0])
    super_temp, sub_temp = templates.pop(), templates.pop()
    supers = list_supers(sub_temp)
    seen = set()
    for name in sub_re.findall(super_temp):
        if name not in supers or name in seen:
            continue
        replace = supers[name]
        super_temp = re.sub('\{%\s*block\s+' + name + '\s*%\}',
                            replace,
                            super_temp, flags=re.S)
        seen.add(name)
    templates.append(super_temp)
    return compile_inheritance(templates)

##################
# File Utilities #
##################

def file_exists(filename):
    """Checks if a file exists relative to os.getcwd().

    NOTE:
    This function exists to make test injection easier.

    RETURNS:
    bool; True if filename exists
    """
    return os.path.exists(filename)

def file_read(filename):
    """Reads contents of a specified file.

    NOTE:
    This function exists to make test injection easier.

    RETURNS:
    text -- str; contents of file
    """
    with open(filename, 'r') as f:
        return f.read()

def file_write(filename, text):
    """Writes text to a specified file.

    NOTE:
    This function exists to make test injection easier.
    """
    dirname = os.path.dirname(filename)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(text)

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
        if not file_exists(args.source):
            log.warn('File ' + args.source + ' does not exist.')
            exit(1)
        elif not os.path.isfile(args.source):
            log.warn(args.source + ' is not a valid file')
            exit(1)
        result = link.link(args.source)
        if args.markdown:
            markdown_obj = Markdown(result)
            for k, v in markdown_obj.variables.items():
                configs['VARIABLES'][k] = v
            result = markdown_obj.text
        result = link.substitutions(result,
                                    configs.get('SUBSTITUTIONS', []),
                                    args)
        result, cache = link.retrieve_blocks(result)
        if 'TOC_BUILDER' in configs:
            configs['VARIABLES']['table-of-contents'] = link.scrape_headers(result, configs['TOC_BUILDER'])
            for import_stmt in (
                    'from datetime import datetime',
                    ):
                exec(import_stmt, configs)
        for k, v in cache.items():
            configs['VARIABLES'][k] = v

    result = compile(args.template, configs)
    if not args.destination:
        log.log(result)
        return
    file_write(args.destination, result)
    log.info('Result can be found at ' + args.destination)

