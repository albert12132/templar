import os
import unittest
import re
import templar.link as link
import templar.compile as compile
import templar.__main__ as config
import textwrap

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
            self.files[filename] = self.dedent(contents)

    def _read(self, filename):
        return self.files[filename]

    def _file_exists(self, filename):
        return filename in self.files

    def assertLink(self, src, output, files=None):
        if files:
            self.register_read(files)
        result = link.link(src) + '\n'
        output = self.dedent(output) + '\n'
        self.assertEqual(output, result)

    def assertBlock(self, src, output, expect_cache, no_dedent=False):
        result, cache = link.retrieve_blocks(self.dedent(src))
        if not no_dedent:
            expect_cache = {k: self.dedent(v) for k, v in expect_cache.items()}
        result += '\n'
        output = self.dedent(output) + '\n'
        self.assertEqual(output, result)
        self.assertEqual(expect_cache, cache)

    def assertSubstitution(self, src, output, subs, files=None, args=None):
        if files:
            self.register_read(files)
        if not args:
            args = []
        args = MockArgparseObject(args)
        result = self.dedent(src) + '\n'
        result = link.substitutions(result, subs, args)
        output = self.dedent(output) + '\n'
        self.assertEqual(output, result)

    def assertHeaders(self, text, regex, translate, build, expect):
        toc_builder = make_mock_toc_builder(regex, translate, build)
        expect = self.dedent(expect)
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
            self.files[filename] = self.dedent(contents)

    def _read(self, filename):
        return self.files[filename]

    def _file_exists(self, filename):
        return filename in self.files

    def assertInheritance(self, template_path, template_dirs, expect, files=None):
        template_path = os.path.basename(template_path)
        if files:
            self.register_read(files)
        actual = self.dedent(
                    compile.process_inheritance(
                             template_path, template_dirs))
        expect = self.dedent(expect)
        self.assertEqual(expect, actual)

    def assertProcess(self, template, attrs, expect):
        template = self.dedent(template)
        actual = self.dedent(
                            compile.process(template, attrs))
        expect = self.dedent(expect)
        self.assertEqual(expect, actual)

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
