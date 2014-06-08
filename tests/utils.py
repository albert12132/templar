import sys
sys.path.insert(0, '..')

import os
import unittest
import re
from markdown import convert, Markdown
from link import link, retrieve_blocks, substitutions, scrape_headers

class TemplarTest(unittest.TestCase):
    @staticmethod
    def openData(filename):
        path = os.path.join(os.path.dirname(__file__), 'test-data')
        if not os.path.exists(os.path.join(path, filename)):
            print('No file', filename, 'found in', path)
        with open(os.path.join(path, filename), 'r') as f:
            return f.read()

    def stripLeadingWhitespace(self, text):
        text = text.strip('\n')
        length = len(re.match('\s*', text).group(0))
        return '\n'.join(line[length:]
                         for line in text.split('\n')).strip()

    def ignoreWhitespace(self, text):
        text = self.stripLeadingWhitespace(text)
        return re.sub('\s+', '', text, flags=re.S)


class MarkdownTest(TemplarTest):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertMarkdown(self, markdown, output):
        markdown = self.stripLeadingWhitespace(markdown)
        output = self.stripLeadingWhitespace(output)
        try:
            self.assertEqual(convert(markdown) + '\n', output + '\n')
        except AssertionError:
            raise

    def assertMarkdownNotEqual(self, markdown, output):
        markdown = self.stripLeadingWhitespace(markdown)
        output = self.stripLeadingWhitespace(output)
        try:
            self.assertNotEqual(convert(markdown), output)
        except AssertionError:
            raise

    def assertMarkdownIgnoreWS(self, markdown, output):
        markdown = self.stripLeadingWhitespace(markdown)
        try:
            self.assertEqual(self.ignoreWhitespace(convert(markdown)),
                             self.ignoreWhitespace(output))
        except AssertionError:
            raise

class LinkTest(TemplarTest):
    def setup(self):
        pass

    def teardDown(self):
        pass

    def assertLink(self, src, output):
        result = link(self.stripLeadingWhitespace(src)) + '\n'
        output = self.stripLeadingWhitespace(output) + '\n'
        try:
            self.assertEqual(result, output)
        except AssertionError:
            raise

    def assertBlock(self, src, output, expect_cache):
        result, cache = retrieve_blocks(self.stripLeadingWhitespace(src))
        result += '\n'
        output = self.stripLeadingWhitespace(output) + '\n'
        try:
            self.assertEqual(result, output)
            self.assertDictEqual(expect_cache, cache)
        except AssertionError:
            raise

    def assertDictEqual(self, dict1, dict2):
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        try:
            self.assertEqual(keys1, keys2)
        except AssertionError:
            raise

        for k in keys1:
            try:
                self.assertEqual(self.stripLeadingWhitespace(dict1[k]),
                                 self.stripLeadingWhitespace(dict2[k]))
            except AssertionError:
                raise

def main():
    unittest.main()
