import os
import unittest
import re
import templar.link as link
import templar.compile as compile
import templar.__main__ as config

from templar.markdown import convert, Markdown
from templar.utils.core import TableOfContents

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
        self.old_file = link.file_read, link.file_exists
        link.file_read = self._read
        link.file_exists = self._file_exists

    def tearDown(self):
        link.file_read, link.file_exists = self.old_file
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
        args = MockArgparseObject(args)
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

    def assertHeaders(self, text, regex, translate, build, expect):
        toc_builder = make_mock_toc_builder(regex, translate, build)
        expect = self.stripLeadingWhitespace(expect)
        self.assertEqual(expect,
                         link.scrape_headers(text, toc_builder))

def make_mock_toc_builder(regex, translate, build):
    class MockTocBuilder(TableOfContents):
        @property
        def pattern(self):
            return regex
        def translate(self, match):
            return translate(match)
        def build(self, lst):
            return build(lst)
    return MockTocBuilder


class CompileTest(TemplarTest):
    def setUp(self):
        self.files = {}
        self.old_file = compile.file_read, compile.file_exists
        compile.file_read = self._read
        compile.file_exists = self._file_exists

    def teardDown(self):
        compile.file_read, compile.file_exists = self.old_file
        self.files = None

    def register_read(self, files):
        for filename, contents in files.items():
            self.files[filename] = self.stripLeadingWhitespace(contents)

    def _read(self, filename):
        return self.files[filename]

    def _file_exists(self, filename):
        return filename in self.files

    def assertInheritance(self, template_path, template_dirs, expect, files=None):
        template_path = os.path.basename(template_path)
        if files:
            self.register_read(files)
        actual = self.stripLeadingWhitespace(
                    compile.process_inheritance(
                             template_path, template_dirs))
        expect = self.stripLeadingWhitespace(expect)
        self.assertEqual(actual, expect)

    def assertProcess(self, template, attrs, expect):
        template = self.stripLeadingWhitespace(template)
        actual = self.stripLeadingWhitespace(
                            compile.process(template, attrs))
        expect = self.stripLeadingWhitespace(expect)
        self.assertEqual(actual, expect)

class ConfigTest(TemplarTest):
    def setUp(self):
        self.files = {}
        self.old_functions = config.import_config, config.file_exists
        config.import_config = self._import_config
        config.file_exists = self._file_exists

    def teardDown(self):
        self.files = None
        config.import_config, config.file_exists = self.old_functions

    def register_read(self, files):
        self.files = files

    def _import_config(self, filename, root):
        filename = os.path.join(filename, config.CONFIG_NAME)
        return self.files[filename]

    def _file_exists(self, filename):
        return filename in self.files

    def assertConfig(self, expect, paths, files=None):
        if files:
            self.register_read(files)
        actual = config.configure(paths)
        self.assertEqual(expect, actual)

class MockArgparseObject:
    def __init__(self, conditions):
        self.conditions = conditions

def main():
    unittest.main()
