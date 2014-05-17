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

##################
# REGEX PATTERNS #
##################

extend_tag_re = re.compile(r'<%\s*extends\s*(.+?)\s*%>\n')

super_open_re= re.compile(r'<%\s*(.+?)\s*%>')
super_close_re = re.compile(r'<%/\s*(.+?)\s*%>')

sub_tag_re = re.compile('\{%\s*(.+?)\s*%\}')

expr_re = re.compile('\{{2}\s*(.+?)\s*\}{2}')


#####################
# TEMPLATE RERIEVAL #
#####################

def get_template(filename):
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
        dirs = [os.path.join(BASE_PATH, app)]
    else:
        dirs = TEMPLATE_DIRS
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


def get_all_templates(filename, templates):
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
    contents = get_template(filename)
    match = extend_tag_re.match(extends)
    if match:
        contents = contents[len(match.group(0)):]
        parent = match.group(1)
        get_all_templates(parent, templates)
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


def compile(templates, attrs, dest):
    # process template inheritance first
    templates.reverse()
    template = compile_inheritance(templates)
    for config in CONFIGS:
        attrs[config] = CONFIGS[config]

    while expr_re.search(template):
        for tag in expr_re.findall(template):
            val = eval(tag, attrs)
            template = re.sub('\{\{\s.+?\s\}\}', str(val), template,
                              count=1)
    with open(dest, 'w') as f:
        f.write(template)
        print('Finished compiliing')
        print('Result can be found at ' + dest)

##########################
# COMMAND LINE UTILITIES #
##########################


def parse_content(content):
    """Retrieves variable bindings from CONTENT. If CONTENT is None,
    return an empty dictionary (no variable bindings).

    PARAMETERS:
    content -- the name of a Python module or an empty string.
    """
    if not content:
        return {}
    if content.endswith('.py'):
        content = content[:-3]
    if os.getcwd() != BASE_PATH:
        content = os.path.join(os.path.split(os.getcwd())[1], content)
    content = content.split('/')
    content = '.'.join(content)
    bindings = __import__(content, fromlist=['attrs'])
    return bindings.attrs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', help="The template's filename")
    parser.add_argument('-c', '--content', type=str, default='',
                        help="A Python file with controller logic.")
    parser.add_argument('dest', help='The destination directory')
    args = parser.parse_args()

    templates = get_all_templates(args.template, [])
    tag_names = parse_content(args.content)
    compile(templates, tag_names, args.dest)

if __name__ == '__main__':
    main()
