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
        self.src = src
        self.dst = dst


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
