"""
The public API for Templar publishing.

Users can use this module with the following import statement:

    from templar.api import publish
"""

from templar import linker

import jinja2

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
    if source is None and template is None:
        raise PublishError('When publishing, source and template cannot both be omitted.')

    variables = config.variables
    if source:
        # Linking stage.
        block_map = linker.get_block_map(source)
        variables.update(block_map.get_variables())

        # Compiling stage.
        block_variables = {}
        for name, content in block_map.get_block_variables().items():
            for rule in config.rules:
                if rule.applies(source, destination):
                    content = rule.apply(content, variables)
            block_variables[name] = content
        variables['blocks'] = block_variables   # Blocks are namespaced with 'blocks'.

    # Templating stage.
    if template:
        if not jinja_env:
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(config.template_dirs))
        jinja_template = jinja_env.get_template(template)
        result = jinja_template.render(variables)
    else:
        # template is None implies source is not None, so variables['blocks'] must exist.
        result = variables['blocks']['all']

    # Writing stage.
    if not no_write and destination:
        with open(destination, 'w') as f:
            f.write(result)
    return result


class PublishError(Exception):
    pass
