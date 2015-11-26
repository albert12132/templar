"""
The public API for Templar publishing.

Users can use this module with the following import statement:

    from templar.api import publish
"""

##################
# Publishing API #
##################

def publish_file(config, source=None, template=None):
    """Given a config, performs an end-to-end publishing pipeline.

    See the publish_string function.

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
    if source:
        with open(source, 'r') as f:
            content = f.read()
    else:
        content = None
    return publish(config, content, template)

def publish_string(config, content=None, template=None):
    """Given a config, performs an end-to-end publishing pipeline:

        link -> pre-process -> compile -> post-process -> template

    NOTE: at most one of content and template can be None. If both are None, the publisher
    effectively has nothing to do; an exception is raised.

    PARAMETERS:
    config   -- Config; a context that includes variables, compiler options, and templater
                information.
    content  -- str; contents to publish. If None, the publisher effectively becomes a templating
                engine.
    template -- str; path to a Jinja template file. Templar treats the path as relative to the list
                of template directories in config. If the template cannot be found relative to those
                directories, Templar finally tries the path relative to the current directory.

                If template is None, the publisher effectively becomes a linker and compiler.

    RETURNS:
    str; the result of the publishing pipeline.
    """
    # Get variables from config.
    if content:
        blocks = linker.get_blocks(content)  # Block object, top-level :all
        compiler.compile(blocks, config)     # handles pre/post substitutions and markdown comp
        # convert blocks into variables to pass to jinja
        # Add variables in the blocks to config
    else:
        # get variables to pass to jinja
        pass

    if template:
        # use jinja
        pass
    else:
        # use blocks.all
        pass
    return # result

