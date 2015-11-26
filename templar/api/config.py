"""
The public API for Templar configuration.

Users can use this module with the following import statement:

    from templar.api import config
"""

import importlib.machinery

class Config(object):
    """Contains configurations for Templar's publishing pipeline."""
    pass

def import_config(config_path):
    """Import a Config from a given path, relative to the current directory.

    The module specified by the config file must contain a variable called
    `config` that is assigned to a Config object.
    """
    # TODO: check if config_path is a file.
    loader = importlib.machinery.SourceFileLoader(config_path, config_path)
    return loader.load_module().config

