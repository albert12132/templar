import os
import unittest
import re
import textwrap

from templar.markdown import convert, Markdown

class TemplarTest(unittest.TestCase):
    def dedent(self, text):
        return textwrap.dedent(text).lstrip('\n').rstrip()

    def ignoreWhitespace(self, text):
        text = self.dedent(text)
        return re.sub('\s+', '', text, flags=re.S)

class MarkdownTest(TemplarTest):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertMarkdown(self, markdown, output):
        markdown = self.dedent(markdown)
        output = self.dedent(output)
        try:
            self.assertEqual(output + '\n', convert(markdown) + '\n')
        except AssertionError:
            raise

    def assertMarkdownNotEqual(self, markdown, output):
        markdown = self.dedent(markdown)
        output = self.dedent(output)
        try:
            self.assertNotEqual(output, convert(markdown))
        except AssertionError:
            raise

    def assertMarkdownIgnoreWS(self, markdown, output):
        markdown = self.dedent(markdown)
        try:
            self.assertEqual(self.ignoreWhitespace(output),
                             self.ignoreWhitespace(convert(markdown)))
        except AssertionError:
            raise

