"""
The public API for Templar pre/post-processor rules.

Users can use this module with the following import statement:

    from templar.api import rules
"""

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
        raise NotImplementedError


class SubstitutionRule(Rule):
    """A rule that transforms the content that is being processed, based on a regex pattern and a
    substitution function. The substitution behaves exactly like re.sub.
    """
    def __init__(self, pattern, substitution, src=None, dst=None):
        super().__init__(src, dst)
        self.pattern = pattern
        self.substitution = substitution


class VariableRule(Rule):
    """A rule that adds one or more Config variables by applying a transformation on the content
    that is being processed.
    """
    def __init__(self, transform, src=None, dst=None):
        super().__init__(src, dst)
        self.transform = transform


class HtmlTableOfContents(VariableRule):
    """A variable rule that constructs a table of contents based on all HTML headers found in the
    content.

    This rule adds a Config variable called "table_of_contents". By default, this rule only applies
    to destinations with a .html extension.
    """
    def __init__(self, src=None, dst=r'.*\.html'):
        super().__init(src, dst)


class CompilerRule(Rule):
    def __init__(self, src=None, dst=None):
        pass
