"""Tests templar/api/rules/core.py"""

from templar.api.rules.compiler_rules import MarkdownToHtmlRule

import unittest

class MarkdownToHtmlRuleTest(unittest.TestCase):
    def setUp(self):
        self.rule = MarkdownToHtmlRule()

    def testApplies_default(self):
        self.assertTrue(self.rule.applies('source.md', 'destination.html'))
        self.assertFalse(self.rule.applies('source.py', 'destination.html'))
        self.assertFalse(self.rule.applies('source.md', 'destination.py'))

    def testApply(self):
        # Basic test to make sure markdown library is called correctly.
        content = 'This is *a paragraph* with `code`.'
        result = self.rule.apply(content, {})
        self.assertEqual('<p>This is <em>a paragraph</em> with <code>code</code>.</p>', result)
