"""Tests templar/api/rules/table_of_contents.py"""

from templar.api.rules.table_of_contents import HtmlTableOfContents

import unittest
import mock

class HtmlTableOfContentsTest(unittest.TestCase):
    def setUp(self):
        self.rule = HtmlTableOfContents()
        self.variables = {}
        self.maxDiff = None

    def testAppliesOnlyToHtmlByDefault(self):
        self.assertTrue(self.rule.applies('some_file', 'file.html'))
        self.assertFalse(self.rule.applies('some_file', 'file.py'))

    def testNoHeaders(self):
        self.verifyApply('<p>No headers</p>', '<ul>\n</ul>')

    def testCapturesIds(self):
        self.verifyApply(
            self.join_lines(
                '<h1 id="first">First header</h1>',
                "<h1 id='second'>Second header</h1>"),
            self.join_lines(
                '<ul>',
                '  <li><a href="#first">First header</a></li>',
                '  <li><a href="#second">Second header</a></li>',
                '</ul>'))

    def testDisplaysHeadersWithNoIds(self):
        self.verifyApply(
            self.join_lines(
                '<h1>First header</h1>',
                "<h1>Second header</h1>"),
            self.join_lines(
                '<ul>',
                '  <li>First header</li>',
                '  <li>Second header</li>',
                '</ul>'))

    def testCanStartWithAnyLevelHeader(self):
        for i in range(1, 6):
            self.verifyApply(
                '<h{0}>Header</h{0}>'.format(i),
                self.join_lines(
                    '<ul>',
                    '  <li>Header</li>',
                    '</ul>'))

    def testNestedHeaders(self):
        self.verifyApply(
            self.join_lines(
                '<h1>First header</h1>',
                "<h2>Second header</h2>",
                "<h3>Third header</h3>",
                "<h2>Fourth header</h2>",
                "<h1>Fifth header</h1>",
                "<h2>Sixth header</h2>"),
            self.join_lines(
                '<ul>',
                '  <li>First header</li>',
                '  <ul>',
                '    <li>Second header</li>',
                '    <ul>',
                '      <li>Third header</li>',
                '    </ul>',
                '    <li>Fourth header</li>',
                '  </ul>',
                '  <li>Fifth header</li>',
                '  <ul>',
                '    <li>Sixth header</li>',
                '  </ul>',
                '</ul>'))


    def testNestedHeaders_beginsWithHeaderThatIsTooSmall(self):
        self.verifyApply(
            self.join_lines(
                '<h2>First header</h2>',
                "<h3>Second header</h3>",
                "<h1>Third header</h1>",
                "<h2>Fourth header</h2>"),
            self.join_lines(
                '<ul>',
                '  <li>First header</li>',
                '  <ul>',
                '    <li>Second header</li>',
                '  </ul>',
                '  <li>Third header</li>',
                '  <ul>',
                '    <li>Fourth header</li>',
                '  </ul>',
                '</ul>'))

    def verifyApply(self, contents, expect):
        self.rule.apply(contents, self.variables)
        self.assertEqual({
            'table_of_contents': expect,
        }, self.variables)

    def join_lines(self, *lines):
        return '\n'.join(lines)
