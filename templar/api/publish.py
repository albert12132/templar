"""
The public API for Templar publishing.

Users can use this module with the following import statement:

    from templar.api import publish
"""

from templar import linker
from templar.api.config import Config
from templar.api.rules.core import VariableRule
from templar.exceptions import TemplarError

import jinja2
import os
import re

def publish(config, source=None, template=None, destination=None, jinja_env=None, no_write=False):
    """Given a config, performs an end-to-end publishing pipeline and returns the result:

        linking -> compiling -> templating -> writing

    NOTE: at most one of source and template can be None. If both are None, the publisher
    effectively has nothing to do; an exception is raised.

    PARAMETERS:
    config      -- Config; a context that includes variables, compiler options, and templater
                   information.
    source      -- str; path to a source file, relative to the current working directory. If None,
                   the publisher effectively becomes a templating engine.
    template    -- str; path to a Jinja template file. Templar treats the path as relative to the
                   list of template directories in config. If the template cannot be found relative
                   to those directories, Templar finally tries the path relative to the current
                   directory.

                   If template is None, the publisher effectively becomes a linker and compiler.
    destination -- str; path for the destination file.
    jinja_env   -- jinja2.Environment; if None, a Jinja2 Environment is created with a
                   FileSystemLoader that is configured with config.template_dirs. Otherwise, the
                   given Jinja2 Environment is used to retrieve and render the template.
    no_write    -- bool; if True, the result is not written to a file or printed. If False and
                   destination is provided, the result is written to the provided destination file.

    RETURNS:
    str; the result of the publishing pipeline.
    """
    if not isinstance(config, Config):
        raise PublishError(
                "config must be a Config object, "
                "but instead was type '{}'".format(type(config).__name__))

    if source is None and template is None:
        raise PublishError('When publishing, source and template cannot both be omitted.')

    variables = config.variables
    if source:
        # Linking stage.
        all_block, extracted_variables = linker.link(source)
        variables.update(extracted_variables)

        # Compiling stage.
        block_variables = {}
        for rule in config.rules:
            if rule.applies(source, destination):
                if isinstance(rule, VariableRule):
                    variables.update(rule.apply(str(all_block)))
                else:
                    all_block.apply_rule(rule)
        block_variables.update(linker.get_block_dict(all_block))
        variables['blocks'] = block_variables   # Blocks are namespaced with 'blocks'.

    # Templating stage.
    if template:
        if not jinja_env:
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(config.template_dirs))
        jinja_template = jinja_env.get_template(template)
        result = jinja_template.render(variables)

        # Handle recursive evaluation of Jinja expressions.
        iterations = 0
        while config.recursively_evaluate_jinja_expressions \
                and iterations < _MAX_JINJA_RECURSIVE_DEPTH + 1 \
                and  _jinja_expression_re.search(result):
            if iterations == _MAX_JINJA_RECURSIVE_DEPTH:
                raise PublishError('\n'.join([
                    'Recursive Jinja expression evaluation exceeded the allowed '
                        'number of iterations. Last state of template:',
                    result]))
            jinja_env = jinja2.Environment(loader=jinja2.DictLoader({'intermediate': result}))
            jinja_template = jinja_env.get_template('intermediate')
            result = jinja_template.render(variables)
            iterations += 1
    else:
        # template is None implies source is not None, so variables['blocks'] must exist.
        result = variables['blocks']['all']

    # Writing stage.
    if not no_write and destination:
        destination_dir = os.path.dirname(destination)
        if destination_dir != '' and not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)
        with open(destination, 'w') as f:
            f.write(result)
    return result


class PublishError(TemplarError):
    pass

_jinja_expression_re = re.compile(r'\{\{.*\}\}')
_MAX_JINJA_RECURSIVE_DEPTH = 10
