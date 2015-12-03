"""
The public API for Templar pre/post-processor rules.

Users can use this module with the following import statement:

    from templar.api.rules import core
"""

import re


class Rule:
    """Represents a preprocessor or postprocessor rule. Rules are applied in the order that they
    are listed in the Config.

    When constructing a rule, the arguments `src` and `dst` are regular expressions; Templar will
    only apply a rule if the source and destination of the publishing pipeline match the regexes.
    """
    def __init__(self, src=None, dst=None):
        self._src_pattern = src
        self._dst_pattern = dst

    def applies(self, src, dst):
        """Checks if this rule applies to the given src and dst paths, based on the src pattern and
        dst pattern given in the constructor.

        If src pattern was None, this rule will apply to any given src path (same for dst).
        """
        if self._src_pattern and re.search(self._src_pattern, src) is None:
            return False
        elif self._dst_pattern and re.search(self._dst_pattern, dst) is None:
            return False
        return True

    def apply(self, content, variables):
        """Applies this rule to the given content. A rule can do one or more of the following:

        - Return a string; this is taken to be the transformed version of content, and will be used
          as the new content after applying this rule.
        - Modify variables (a dict). Usually, Rules that modify this dictionary will add new
          variables. However, a Rule can also delete or update key/value pairs in the dictionary.
        """
        raise NotImplementedError


class SubstitutionRule(Rule):
    """An abstract class that represents a rule that transforms the content that is being processed,
    based on a regex pattern and a substitution function. The substitution behaves exactly like
    re.sub.
    """
    pattern = None  # Subclasses should override this variable with a regex string.

    def substitute(self, match):
        """A substitution function that returns the text with which to replace the given match.
        Subclasses should implement this method.
        """
        raise InvalidRule(
                '{} must implement the substitute method to be '
                'a valid SubstitutionRule'.format(type(self).__name__))

    def apply(self, content, variables):
        if not isinstance(self.pattern, str):
            raise InvalidRule("{}'s pattern has type '{}', but expected a string.".format(
                    type(self).__name__, type(self.pattern).__name__))
        return re.sub(self.pattern, self.substitute, content)


class InvalidRule(Exception):
    pass
