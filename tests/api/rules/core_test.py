"""Tests templar/api/rules/core.py"""

from templar.api.rules.core import Rule
from templar.api.rules.core import SubstitutionRule
from templar.api.rules.core import InvalidRule

import unittest

class RuleTest(unittest.TestCase):
    def testApplies_withSrcRegex(self):
        rule = Rule(src='.html')
        self.assertTrue(rule.applies('source.html', 'destination'))
        self.assertFalse(rule.applies('source.py', 'destination'))

    def testApplies_withDestRegex(self):
        rule = Rule(dst='.html')
        self.assertTrue(rule.applies('source', 'destination.html'))
        self.assertFalse(rule.applies('source', 'destination.py'))

class SubstitutionRuleTest(unittest.TestCase):
    def testInvalidPattern(self):
        class TestRule(SubstitutionRule):
            pattern = 3

        rule = TestRule()
        with self.assertRaises(InvalidRule) as cm:
            rule.apply('content', {})
        self.assertEqual(
                "TestRule's pattern has type 'int', but expected a string.",
                str(cm.exception))

    def testUnimplementedSubstituteMethod(self):
        class TestRule(SubstitutionRule):
            pattern = r'\w'

        rule = TestRule()
        with self.assertRaises(InvalidRule) as cm:
            rule.apply('content', {})
        self.assertEqual(
                'TestRule must implement the substitute method to be a valid SubstitutionRule',
                str(cm.exception))

    def testWithProperRegexAndSubstitute(self):
        class TestRule(SubstitutionRule):
            pattern = r'(\w*)'
            def substitute(self, match):
                return match.group(1).upper()

        rule = TestRule()
        result = rule.apply('this is spot. see spot run.', {})
        self.assertEqual('THIS IS SPOT. SEE SPOT RUN.', result)
