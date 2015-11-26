"""
The public API for Templar pre/post-processor rules.

Users can use this module with the following import statement:

    from templar.api import rules
"""

class Rule:
    pass

class SubstitutionRule(Rule):
    pass

class VariableRule(Rule):
    pass

class MarkdownToHtmlToc(VariableRule):
    pass
