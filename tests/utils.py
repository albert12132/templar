import sys
sys.path.insert(0, '..')

import os
import unittest
import re
from markdown import convert, Markdown
import link

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
    def setUp(self):
        self.files = {}
        self.old_file = link.file_read, link.file_write, link.file_exists
        link.file_read = self._read
        link.file_exists = self._file_exists
        # link.file_write = # TODO

    def teardDown(self):
        link.file_read, link.file_write = self.old_file
        self.files = None

    def register_read(self, files):
        for filename, contents in files.items():
            self.files[filename] = self.stripLeadingWhitespace(contents)

    def _read(self, filename):
        return self.files[filename]

    def _file_exists(self, filename):
        return filename in self.files

    def assertLink(self, src, output, files=None):
        if files:
            self.register_read(files)
        result = link.link(self.stripLeadingWhitespace(src)) + '\n'
        output = self.stripLeadingWhitespace(output) + '\n'
        self.assertEqual(result, output)

    def assertBlock(self, src, output, expect_cache):
        result, cache = link.retrieve_blocks(self.stripLeadingWhitespace(src))
        result += '\n'
        output = self.stripLeadingWhitespace(output) + '\n'
        self.assertEqual(result, output)
        self.assertDictEqual(expect_cache, cache)

    def assertSubstitution(self, src, output, subs, files=None, args=None):
        if files:
            self.register_read(files)
        if not args:
            args = []
        result = link.link(self.stripLeadingWhitespace(src)) + '\n'
        result = link.substitutions(result, subs, args)
        output = self.stripLeadingWhitespace(output) + '\n'
        self.assertEqual(result, output)

    def assertDictEqual(self, dict1, dict2):
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        self.assertEqual(keys1, keys2)

        for k in keys1:
            self.assertEqual(self.stripLeadingWhitespace(dict1[k]),
                             self.stripLeadingWhitespace(dict2[k]))

    def assertHeaders(self, text, regex, translate, expect):
        self.assertEqual(link.scrape_headers(text, regex, translate),
                         expect)

def main():
    unittest.main()
