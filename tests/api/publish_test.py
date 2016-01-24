"""Integration tests using templar/api/publish.py"""

from templar.api.config import ConfigBuilder
from templar.api.publish import PublishError
from templar.api.publish import publish
from templar.api.rules.core import Rule
from templar.api.rules.core import VariableRule

import jinja2
import unittest
import mock

class PublishTest(unittest.TestCase):
    def setUp(self):
        self.is_file_patcher = mock.patch('os.path.isfile')
        self.mock_is_file = self.is_file_patcher.start()
        self.mock_is_file.return_value = True

    def tearDown(self):
        self.is_file_patcher.stop()

    def testInvalidConfigType(self):
        invalid_config = {'template_dirs': ['some/path']}
        with self.assertRaises(PublishError) as cm:
            publish(invalid_config, source='some/path', no_write=True)
        self.assertEquals(
                "config must be a Config object, but instead was type 'dict'",
                str(cm.exception))

    def testMissingSourceAndTemplate(self):
        with self.assertRaises(PublishError) as cm:
            publish(ConfigBuilder().build(), no_write=True)
        self.assertEquals(
                "When publishing, source and template cannot both be omitted.",
                str(cm.exception))

    def testOnlyTemplate_success(self):
        template_loader = jinja2.DictLoader({
            'some/path': self.join_lines(
                '<title>{{ title }}</title>',
                '<ul>',
                '{% for user in users -%}',
                '<li><a href="{{ user.url }}">{{ user.username }}</a></li>',
                '{% endfor -%}',
                '</ul>')
        })
        jinja_env = jinja2.Environment(loader=template_loader)
        class User(object):
            def __init__(self, url, username):
                self.url = url
                self.username = username
        # Build Templar config.
        config_builder = ConfigBuilder()
        config_builder.add_variable('title', 'Test')
        config_builder.add_variable('users', [User('url1', 'user1'), User('url2', 'user2')])
        config = config_builder.build()

        result = publish(config, template='some/path', jinja_env=jinja_env, no_write=True)
        self.assertEqual(
                self.join_lines(
                    '<title>Test</title>',
                    '<ul>',
                    '<li><a href="url1">user1</a></li>',
                    '<li><a href="url2">user2</a></li>',
                    '</ul>'),
                result)

    def testOnlySource_withLinks(self):
        file_map = {
            'docA.md': self.join_lines(
                'To be or not to be',
                '<include docB.md:hamlet>'),
            'docB.md': self.join_lines(
                'Catchphrases',
                '<block hamlet>',
                'That is the question',
                '</block hamlet>'),
        }
        with self.mock_open(file_map):
            result = publish(ConfigBuilder().build(), source='docA.md', no_write=True)
        self.assertEquals(self.join_lines('To be or not to be', 'That is the question'), result)

    def testOnlySource_withRules(self):
        file_map = {
            'docA.md': 'original content',
        }
        class AppliedRule(Rule):
            def apply(self, content):
                return content + ' rule1'
        class NotAppliedRule(Rule):
            def apply(self, content):
                return content + 'rule2'
        config_builder = ConfigBuilder()
        config_builder.append_preprocess_rules(
                AppliedRule(src=r'\.md'),
                NotAppliedRule(dst=r'\.html'))
        config_builder.append_postprocess_rules(AppliedRule(), NotAppliedRule(src=r'\.py'))

        with self.mock_open(file_map):
            result = publish(config_builder.build(), source='docA.md', no_write=True)
        self.assertEquals('original content rule1 rule1', result)

    def testOnlySource_withRulesAndBlocks(self):
        file_map = {
            'docA.md': self.join_lines(
                'outer content',
                '<block blockA>',
                'inner content',
                '</block blockA>',
                'outer content'),
        }
        class AppliedRule(Rule):
            counter = 0
            def apply(self, content):
                self.counter += 1
                return 'segment {}: '.format(self.counter) + content
        config_builder = ConfigBuilder()
        config_builder.append_postprocess_rules(AppliedRule())

        with self.mock_open(file_map):
            result = publish(config_builder.build(), source='docA.md', no_write=True)
        self.assertEquals(
            self.join_lines(
                'segment 1: outer content',
                'segment 2: inner content',
                'segment 3: outer content'),
            result)

    def testSourceAndTemplate(self):
        file_map = {
            'docA.md': self.join_lines(
                '~ title: Test',    # Creates a variable called 'title'
                'outside block',
                '<block first>',
                'inside block',
                '</block first>'),
        }
        template_loader = jinja2.DictLoader({
            'some/path': self.join_lines(
                '<title>{{ title }}</title>',  # Use the variable defined in the content.
                '<p>',
                '{{ blocks.first }}',   # Use the block defined in the content.
                '{{ var }}',            # Use the variable defined by VarRule, below.
                '</p>')
        })
        jinja_env = jinja2.Environment(loader=template_loader)

        # Test rule application.
        class UpperCaseRule(Rule):
            def apply(self, content):
                return content.upper()
        class VarRule(VariableRule):
            def extract(self, content):
                return {'var': 'val'}
        config_builder = ConfigBuilder()
        config_builder.append_preprocess_rules(UpperCaseRule(), VarRule())

        with self.mock_open(file_map):
            result = publish(
                    config_builder.build(),
                    source='docA.md',
                    template='some/path',
                    jinja_env=jinja_env,
                    no_write=True)
        self.assertEquals(
                self.join_lines(
                    '<title>Test</title>',
                    '<p>',
                    'INSIDE BLOCK',
                    'val',
                    '</p>'),
                result)

    def testRecursivelyEvaluateJinjaExpressions(self):
        file_map = {
            'docA.md': self.join_lines(
                '~ title: test',    # Creates a variable called 'title'
                '{{ title|capitalize }}'),
        }
        template_loader = jinja2.DictLoader({
            'some/path': '{{ blocks["all"] }}',   # Use the block defined in the content.
        })
        jinja_env = jinja2.Environment(loader=template_loader)

        # By default, should not recursively evaluate Jinja expressions.
        with self.mock_open(file_map):
            result = publish(
                    ConfigBuilder().build(),
                    source='docA.md',
                    template='some/path',
                    jinja_env=jinja_env,
                    no_write=True)
        self.assertEquals('{{ title|capitalize }}', result)

        # Set recursively_evaluate_jinja_expressions to True.
        config = ConfigBuilder().set_recursively_evaluate_jinja_expressions(True).build()
        with self.mock_open(file_map):
            result = publish(
                    config,
                    source='docA.md',
                    template='some/path',
                    jinja_env=jinja_env,
                    no_write=True)
        self.assertEquals('Test', result)

    def testRecursivelyEvaluateJinjaExpressions_preventInfiniteLoop(self):
        file_map = {
            'docA.md': '{{ blocks["all"] }}',   # Refers to itself.
        }
        template_loader = jinja2.DictLoader({
            'some/path': '{{ blocks["all"] }}',   # Use the block defined in the content.
        })
        jinja_env = jinja2.Environment(loader=template_loader)

        # Set recursively_evaluate_jinja_expressions to True.
        config = ConfigBuilder().set_recursively_evaluate_jinja_expressions(True).build()
        with self.assertRaises(PublishError) as cm:
            with self.mock_open(file_map):
                result = publish(
                        config,
                        source='docA.md',
                        template='some/path',
                        jinja_env=jinja_env,
                        no_write=True)
        self.assertEquals(
                self.join_lines(
                    'Recursive Jinja expression evaluation exceeded the allowed number of '
                        'iterations. Last state of template:',
                    '{{ blocks["all"] }}')
                , str(cm.exception))

    def testWrite(self):
        template_loader = jinja2.DictLoader({
            'some/path': 'content',
        })
        jinja_env = jinja2.Environment(loader=template_loader)

        # Use a simple mock_open instead of this test's mock_open method, since we don't need to
        # open multiple files.
        mock_open = mock.mock_open()
        with mock.patch('builtins.open', mock_open):
            result = publish(
                    ConfigBuilder().build(),
                    template='some/path',
                    destination='dest.html',
                    jinja_env=jinja_env)

        # Verify a file handle to the destination file was opened.
        mock_open.assert_called_once_with('dest.html', 'w')
        # Verify the result was actually written to the destination fie handle.
        handle = mock_open()
        handle.write.assert_called_once_with('content')

    ##################
    # Test utilities #
    ##################

    def mock_open(self, file_map):
        """Creates a patch object for the built in open function that maps filenames to file
        contents.
        """
        def side_effect(filename, mode):
            if mode == 'r':
                assert filename in file_map, \
                        'File ' + filename + ' not found in ' + str(list(file_map))
            self.mock_is_file.side_effect = lambda f: f in file_map
            return mock.mock_open(read_data=file_map[filename])(filename, mode)

        return mock.patch('builtins.open', mock.Mock(side_effect=side_effect))

    def join_lines(self, *lines):
        return '\n'.join(lines)
