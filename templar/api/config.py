"""
The public API for Templar configuration.

Users can use this module with the following import statement:

    from templar.api import config
"""

from templar.api.rules.core import Rule
from templar.exceptions import TemplarError

import importlib.machinery
import os.path

class ConfigBuilder(object):
    """Builds a Config for Templar's publishing pipeline.

    A Templar Config consists of the following components:
    - template_dirs
    - variables
    - preprocess_rules
    - compiler_rules
    - postprocess_rules

    Example usage:

        builder = ConfigBuilder()
        builder.add_template_dirs(
            'template/dir1',
            'template/dir2')
        builder.add_variable('var1', 'value1')
        builder.add_variable('var2', 'value2')
        config = builder.build()
    """
    def __init__(self,
            template_dirs=None,
            variables=None,
            recursively_evaluate_jinja_expressions=False,
            compiler_rules=None,
            preprocess_rules=None,
            postprocess_rules=None):
        self._template_dirs = list(template_dirs) if template_dirs else []
        self._variables = variables.copy() if variables else {}
        self._recursively_evaluate_jinja_expressions = recursively_evaluate_jinja_expressions
        self._compiler_rules = list(compiler_rules) if compiler_rules else []
        self._preprocess_rules = list(preprocess_rules) if preprocess_rules else []
        self._postprocess_rules = list(postprocess_rules) if postprocess_rules else []

    def add_template_dirs(self, *template_dirs):
        for template_dir in template_dirs:
            if not isinstance(template_dir, str):
                raise ConfigBuilderError(
                        'template_dir must be a string, but instead was: ' + repr(template_dir))
            elif not os.path.isdir(template_dir):
                raise ConfigBuilderError('template_dir path is not a directory: ' + template_dir)
        self._template_dirs.extend(template_dirs)
        return self

    def clear_template_dirs(self):
        self._template_dirs = []
        return self

    def add_variable(self, variable, value):
        if not isinstance(variable, str):
            raise ConfigBuilderError(
                    'variable must be a string, but instead was: ' + repr(variable))
        # TODO: Coerce value into some string (possibly unicode, depending on Jinja)
        self._variables[variable] = value
        return self

    def add_variables(self, variable_map):
        # Loop through variables instead of using dict.update so we can validate each variable.
        for variable, value in variable_map.items():
            self.add_variable(variable, value)
        return self

    def set_recursively_evaluate_jinja_expressions(self, recursively_evaluate_jinja_expressions):
        if not isinstance(recursively_evaluate_jinja_expressions, bool):
            raise ConfigBuilderError(
                    'recursively_evaluate_jinja_expressions must be a boolean, '
                    'but instead was: ' + repr(recursively_evaluate_jinja_expressions))
        self._recursively_evaluate_jinja_expressions = recursively_evaluate_jinja_expressions
        return self

    def clear_variables(self):
        self._variables = {}
        return self

    def append_compiler_rules(self, *compiler_rules):
        for rule in compiler_rules:
            if not isinstance(rule, Rule):
                raise ConfigBuilderError(
                        'compiler_rule must be a Rule, but instead was: ' + repr(rule))
        self._compiler_rules.extend(compiler_rules)
        return self

    def prepend_compiler_rules(self, *compiler_rules):
        for rule in compiler_rules:
            if not isinstance(rule, Rule):
                raise ConfigBuilderError(
                        'compiler_rule must be a Rule, but instead was: ' + repr(rule))
        self._compiler_rules = list(compiler_rules) + self._compiler_rules
        return self

    def clear_compiler_rules(self):
        self._compiler_rules = []
        return self

    def append_preprocess_rules(self, *preprocess_rules):
        for rule in preprocess_rules:
            if not isinstance(rule, Rule):
                raise ConfigBuilderError(
                        'preprocess_rule must be a Rule object, but instead was: ' + repr(rule))
        self._preprocess_rules.extend(preprocess_rules)
        return self

    def prepend_preprocess_rules(self, *preprocess_rules):
        for rule in preprocess_rules:
            if not isinstance(rule, Rule):
                raise ConfigBuilderError(
                        'preprocess_rule must be a Rule object, but instead was: ' + repr(rule))
        self._preprocess_rules = list(preprocess_rules) + self._preprocess_rules
        return self

    def clear_preprocess_rules(self):
        self._preprocess_rules = []
        return self

    def append_postprocess_rules(self, *postprocess_rules):
        for rule in postprocess_rules:
            if not isinstance(rule, Rule):
                raise ConfigBuilderError(
                        'postprocess_rule must be a Rule object, but instead was: ' + repr(rule))
        self._postprocess_rules.extend(postprocess_rules)
        return self

    def prepend_postprocess_rules(self, *postprocess_rules):
        for rule in postprocess_rules:
            if not isinstance(rule, Rule):
                raise ConfigBuilderError(
                        'postprocess_rule must be a Rule object, but instead was: ' + repr(rule))
        self._postprocess_rules = list(postprocess_rules) + self._postprocess_rules
        return self

    def clear_postprocess_rules(self):
        self._postprocess_rules = []
        return self

    def build(self):
        return Config(
                self._template_dirs,
                self._variables,
                self._recursively_evaluate_jinja_expressions,
                self._compiler_rules,
                self._preprocess_rules,
                self._postprocess_rules)


class Config(object):
    """An immutable Templar configuration.

    A Config object should not be created directly. Instead, use ConfigBuilder.
    """
    def __init__(self,
            template_dirs,
            variables,
            recursively_evaluate_jinja_expressions,
            compiler_rules,
            preprocess_rules,
            postprocess_rules):
        self._template_dirs = template_dirs
        self._variables = variables
        self._recursively_evaluate_jinja_expressions = recursively_evaluate_jinja_expressions
        self._compiler_rules = compiler_rules
        self._preprocess_rules = preprocess_rules
        self._postprocess_rules = postprocess_rules

    @property
    def template_dirs(self):
        return tuple(self._template_dirs)

    @property
    def variables(self):
        return self._variables.copy()

    @property
    def recursively_evaluate_jinja_expressions(self):
        return self._recursively_evaluate_jinja_expressions

    @property
    def compiler_rules(self):
        return tuple(self._compiler_rules)

    @property
    def preprocess_rules(self):
        return tuple(self._preprocess_rules)

    @property
    def postprocess_rules(self):
        return tuple(self._postprocess_rules)

    @property
    def rules(self):
        return self._preprocess_rules + self._compiler_rules + self._postprocess_rules

    def to_builder(self):
        return ConfigBuilder(
                self._template_dirs,
                self._variables,
                self._recursively_evaluate_jinja_expressions,
                self._compiler_rules,
                self._preprocess_rules,
                self._postprocess_rules)


def import_config(config_path):
    """Import a Config from a given path, relative to the current directory.

    The module specified by the config file must contain a variable called `configuration` that is
    assigned to a Config object.
    """
    if not os.path.isfile(config_path):
        raise ConfigBuilderError(
                'Could not find config file: ' + config_path)
    loader = importlib.machinery.SourceFileLoader(config_path, config_path)
    module = loader.load_module()

    if not hasattr(module, 'config') or not isinstance(module.config, Config):
        raise ConfigBuilderError(
            'Could not load config file "{}": config files must contain '
            'a variable called "config" that is '
            'assigned to a Config object.'.format(config_path))
    return module.config


class ConfigBuilderError(TemplarError):
    pass

