"""Tests template/linker/blocks.py"""

from templar.linker import link
from templar.linker import get_block_dict
from templar.linker import Block
from templar.linker import SourceNotFound
from templar.linker import InvalidBlockName
from templar.linker import IncludeNonExistentBlock
from templar.linker import CyclicalIncludeError

import unittest
import mock

class LinkTest(unittest.TestCase):
    def setUp(self):
        self.is_file_patcher = mock.patch('os.path.isfile')
        self.mock_is_file = self.is_file_patcher.start()
        self.mock_is_file.return_value = True

    def tearDown(self):
        self.is_file_patcher.stop()

    def testNonExistentSourceFile(self):
        self.mock_is_file.return_value = False
        with self.assertRaises(SourceNotFound) as cm:
            link('no/such/path')
        self.assertEqual('Could not find source file: no/such/path', str(cm.exception))

    def testNoBlocksAndIncludes(self):
        data = self.join_lines(
        'Hello world',
        'Second line')
        with self.mock_open({'some/path': data}):
            block, variables = link('some/path')

        self.assertEqual({}, variables)
        block_all = Block('some/path', 'all', [data])
        self.assertBlockEqual(block_all, block)

    def testBlocks_emptyBlock(self):
        data = self.join_lines(
        '<block foo>',
        '</block foo>')
        with self.mock_open({'some/path': data}):
            block, variables = link('some/path')

        self.assertEqual({}, variables)
        block_foo = Block('some/path', 'foo', [])  # Block should be empty.
        block_all = Block('some/path', 'all', [block_foo])
        self.assertBlockEqual(block_all, block)

    def testBlocks_multipleBlocks(self):
        data = self.join_lines(
        '<block one>',
        'def one():',
        '    return 1',
        '</block one>',
        'Intervening text',
        '<block two>',
        'def two():',
        '    return 2',
        '</block two>',
        '<block three>',
        'content',
        '</block three>')
        with self.mock_open({'some/path': data}):
            block, variables = link('some/path')

        self.assertEqual({}, variables)
        block_one = Block('some/path', 'one', [self.join_lines(
            'def one():',
            '    return 1')])
        block_two = Block('some/path', 'two', [self.join_lines(
            'def two():',
            '    return 2')])
        block_three = Block('some/path', 'three', ['content'])
        block_all = Block('some/path', 'all', [
            block_one,
            'Intervening text',
            block_two,
            block_three
        ])
        self.assertBlockEqual(block_all, block)

    def testBlocks_stripLeadingCharacters(self):
        data = self.join_lines(
        '# <block foo>',
        'def foo():',
        '    return None',
        '# </block foo>')
        with self.mock_open({'some/path': data}):
            block, variables = link('some/path')

        self.assertEqual({}, variables)
        block_foo = Block('some/path', 'foo', [self.join_lines(
            'def foo():',
            '    return None')])
        block_all = Block('some/path', 'all', [block_foo])
        self.assertBlockEqual(block_all, block)

    def testBlocks_nested(self):
        data = self.join_lines(
        '<block outer>',
        'outer content',
        '<block inner>',
        'inner content',
        '</block inner>',
        'outer content',
        '</block outer>')
        with self.mock_open({'some/path': data}):
            block, variables = link('some/path')

        self.assertEqual({}, variables)
        block_inner = Block('some/path', 'inner', ['inner content'])
        block_outer = Block('some/path', 'outer', [
            'outer content',
            block_inner,
            'outer content'])
        block_all = Block('some/path', 'all', [block_outer])
        self.assertBlockEqual(block_all, block)

    def testBlocks_preventBlockCalledAll(self):
        data = self.join_lines(
        '<block all>',
        'content',
        '</block all>')
        with self.mock_open({'some/path': data}):
            with self.assertRaises(InvalidBlockName) as cm:
                link('some/path')
        self.assertEqual(
                '"all" is a reserved block name, but found block named "all" in some/path',
                str(cm.exception))

    def testBlocks_preventMutlipleBlocksWithSameName(self):
        data = self.join_lines(
        '<block foo>',
        'content',
        '</block foo>',
        '<block foo>',
        'content',
        '</block foo>')
        with self.mock_open({'some/path': data}):
            with self.assertRaises(InvalidBlockName) as cm:
                link('some/path')
        self.assertEqual('Found multiple blocks with name "foo" in some/path', str(cm.exception))

    def testBlocks_catchMissingClosingBlock(self):
        data = self.join_lines(
        '<block foo>',
        'content')
        with self.mock_open({'some/path': data}):
            with self.assertRaises(InvalidBlockName) as cm:
                link('some/path')
        self.assertEqual('Expected closing block called "foo" in some/path', str(cm.exception))


    def testIncludes_omitBlockName(self):
        mock_open = self.mock_open({
            'path/docA.md': self.join_lines(
                'content',
                '<include path/to/docB.md>',
                'more content'),
            'path/to/docB.md': 'docB content',
        })
        with mock_open:
            block, variables = link('path/docA.md')

        self.assertEqual({}, variables)
        block_all = Block('path/docA.md', 'all', [self.join_lines(
            'content',
            'docB content',
            'more content')])
        self.assertBlockEqual(block_all, block)

    def testIncludes_withBlockName(self):
        mock_open = self.mock_open({
            'docA.md': '<include docB.md:foo-bar>',
            'docB.md': self.join_lines(
                'content not in block',
                '<block foo-bar>',
                'content in block',
                '</block foo-bar>')
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({}, variables)
        block_all = Block('docA.md', 'all', ['content in block'])
        self.assertBlockEqual(block_all, block)

    def testIncludes_stripWhiteSpaceInTag(self):
        mock_open = self.mock_open({
            'docA.md': '< include docB.md : foo >',
            'docB.md': self.join_lines(
                'content not in block',
                '<block foo>',
                'content in block',
                '</block foo>')
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({}, variables)
        block_all = Block('docA.md', 'all', ['content in block'])
        self.assertBlockEqual(block_all, block)

    def testIncludes_relativeToSource(self):
        mock_open = self.mock_open({
            'path/to/docA.md': '<include docB.md>',
            'path/to/docB.md': 'content',
        })
        with mock_open:
            block, variables = link('path/to/docA.md')

        self.assertEqual({}, variables)
        block_all = Block('path/to/docA.md', 'all', ['content'])
        self.assertBlockEqual(block_all, block)

    def testIncludes_leadingWhitespace(self):
        mock_open = self.mock_open({
            'docA.md': '    <include docB.md>',  # Indented four spaces
            'docB.md': 'content',
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({}, variables)
        block_all = Block('docA.md', 'all', ['    content'])
        self.assertBlockEqual(block_all, block)

    def testIncludes_preventNonExistentFile(self):
        mock_open = self.mock_open({
            'docA.md': '<include docB.md>',  # docB.md doesn't exist.
        })
        with mock_open:
            with self.assertRaises(IncludeNonExistentBlock) as cm:
                link('docA.md')
        self.assertEqual('docA.md tried to include a non-existent file: docB.md', str(cm.exception))

    def testIncludes_preventNonExistentBlock(self):
        mock_open = self.mock_open({
            'docA.md': '<include docB.md:foo>',  # docB.md:foo doesn't exist.
            'docB.md': 'contents',
        })
        with mock_open:
            with self.assertRaises(IncludeNonExistentBlock) as cm:
                link('docA.md')
        self.assertEqual(
            'docA.md tried to include a non-existent block: docB.md:foo',
            str(cm.exception))

    def testIncludes_preventCycle(self):
        mock_open = self.mock_open({
            'docA.md': '<include docB.md>',
            'docB.md': '<include docC.md>',
            'docC.md': '<include docB.md>',
        })
        with mock_open:
            with self.assertRaises(CyclicalIncludeError) as cm:
                link('docA.md')
        self.assertEqual('docA.md -> docB.md -> docC.md -> docB.md', str(cm.exception))

    def testVariables_noIncludes(self):
        mock_open = self.mock_open({
            'docA.md': self.join_lines(
                '~ title: foo',
                '~ author: bar')
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({
            'title': 'foo',
            'author': 'bar',
        }, variables)
        block_all = Block('docA.md', 'all', [])
        self.assertBlockEqual(block_all, block)

    def testVariables_handleWhitespace(self):
        mock_open = self.mock_open({
            'docA.md': '~     title   :     foo bar ',
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({
            'title': 'foo bar',
        }, variables)
        block_all = Block('docA.md', 'all', [])
        self.assertBlockEqual(block_all, block)

    def testVariables_variablesInAnyLocation(self):
        mock_open = self.mock_open({
            'docA.md': self.join_lines(
                '~ title: foo ',
                'Some text',
                '~ author: bar ',
                'More text')
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({
            'title': 'foo',
            'author': 'bar',
        }, variables)
        block_all = Block('docA.md', 'all', [self.join_lines(
            'Some text',
            'More text')])
        self.assertBlockEqual(block_all, block)

    def testVariables_includeVariablesFromOtherFiles(self):
        mock_open = self.mock_open({
            'docA.md': self.join_lines(
                '~ title: foo ',
                '<include docB.md>'),
            'docB.md': '~ author: bar '
        })
        with mock_open:
            block, variables = link('docA.md')

        self.assertEqual({
            'title': 'foo',
            'author': 'bar',
        }, variables)
        block_all = Block('docA.md', 'all', [])
        self.assertBlockEqual(block_all, block)


    #############
    # Utilities #
    #############

    def mock_open(self, file_map):
        """Creates a patch object for the built in open function that maps filenames to file
        contents.
        """
        def side_effect(filename, *options):
            assert filename in file_map, 'File ' + filename + ' not found in ' + str(list(file_map))
            return mock.mock_open(read_data=file_map[filename])(filename, *options)

        self.mock_is_file.side_effect = lambda f: f in file_map
        return mock.patch('builtins.open', mock.Mock(side_effect=side_effect))

    def assertBlockEqual(self, expected, actual):
        self.assertEqual(expected.source_path, actual.source_path)
        self.assertEqual(expected.name, actual.name)
        self.assertEqual(len(expected.segments), len(actual.segments))
        for expected_segment, actual_segment in zip(expected.segments, actual.segments):
            if isinstance(expected_segment, str):
                self.assertEqual(expected_segment, actual_segment)
            elif isinstance(expected_segment, Block):
                self.assertBlockEqual(expected_segment, actual_segment)
            else:
                self.fail('Encountered segment of type "{}"'.format(expected_segment))

    def join_lines(self, *lines):
        """Concatenates multiple strings together with newlines in between.

        Using this method is cleaner than using multiline strings (since we need to handle
        indentation and leading/trailing newlines).
        """
        return '\n'.join(lines)

class GetBlockDictTest(unittest.TestCase):
    def testNoNestedBlocks(self):
        block_all = Block('some/path', 'all', ['all content'])
        block_dict = get_block_dict(block_all)
        self.assertEqual({
            'all': 'all content',
        }, block_dict)

    def testNestedBlocks(self):
        block_inner = Block('some/path', 'inner', ['inner content'])
        block_outer = Block('some/path', 'outer', [
            'outer content',
            block_inner,
            'outer content'])
        block_all = Block('some/path', 'all', [
            'all content',
            block_outer,
            'all content'])

        block_dict = get_block_dict(block_all)
        self.assertEqual({
            'all': self.join_lines(
                'all content',
                'outer content',
                'inner content',
                'outer content',
                'all content'),
            'outer': self.join_lines(
                'outer content',
                'inner content',
                'outer content'),
            'inner': 'inner content',
        }, block_dict)

    def join_lines(self, *lines):
        """Concatenates multiple strings together with newlines in between.

        Using this method is cleaner than using multiline strings (since we need to handle
        indentation and leading/trailing newlines).
        """
        return '\n'.join(lines)

