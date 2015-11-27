"""
The public API for Templar publishing.

Users can use this module with the following import statement:

    from templar.api import publish
"""

from templar import linker

def publish(config, source=None, template=None):
    """Given a config, performs an end-to-end publishing pipeline:

        link -> pre-process -> compile -> post-process -> template

    NOTE: at most one of source and template can be None. If both are None, the publisher
    effectively has nothing to do; an exception is raised.

    PARAMETERS:
    config   -- Config; a context that includes variables, compiler options, and templater
                information.
    source   -- str; path to a source file, relative to the current working directory. If None, the
                publisher effectively becomes a templating engine.
    template -- str; path to a Jinja template file. Templar treats the path as relative to the list
                of template directories in config. If the template cannot be found relative to those
                directories, Templar finally tries the path relative to the current directory.

                If template is None, the publisher effectively becomes a linker and compiler.

    RETURNS:
    str; the result of the publishing pipeline.
    """
    if source is None and template is None:
        raise PublishError('When publishing, source and template cannot both be omitted.')

    variables = config.variables
    if source:
        block_map = blocks.get_block_map(source)
        # Blocks are namespaced with 'blocks'.
        variables['blocks'] = compiler.compile(block_map.get_block_variables(), config)
        variables.update(block_map.get_variables())

    if template:
        result = None # TODO: use jinja
    else:
        # template is None implies content is not None, so variables['blocks'] must exist.
        result = variables['blocks']['all']
    return result


class PublishError(Exception):
    pass
