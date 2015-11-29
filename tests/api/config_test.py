"""Tests templar/api/config.py"""

from templar.api.config import ConfigBuilder
from templar.api.config import ConfigBuilderError
from templar.api.rules import Rule
from templar.api.rules import CompilerRule

import unittest
import mock

class ConfigBuilderTest(unittest.TestCase):
    def testEmptyBuilder(self):
        config = ConfigBuilder().build()
        self.assertSequenceEqual([], config.template_dirs)
        self.assertDictEqual({}, config.variables)
        self.assertSequenceEqual([], config.preprocess_rules)
        self.assertSequenceEqual([], config.postprocess_rules)

    def testTemplateDirs(self):
        with mock.patch('os.path.isdir', lambda s: True):
            builder = ConfigBuilder().add_template_dirs('template/path1', 'template/path2')
        self.assertSequenceEqual(
                ['template/path1', 'template/path2'],
                builder.build().template_dirs)

        builder.clear_template_dirs()
        self.assertSequenceEqual([], builder.build().template_dirs)

    def testTemplateDirs_preventNonStrings(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            ConfigBuilder().add_template_dirs(4)
        self.assertEqual(
                'template_dir must be a string, but instead was: 4',
                str(cm.exception))

    def testTemplateDirs_preventNonExistentPath(self):
        with mock.patch('os.path.isdir', lambda s: False):
            with self.assertRaises(ConfigBuilderError) as cm:
                ConfigBuilder().add_template_dirs('no/such/path')
        self.assertEqual(
                'template_dir path is not a directory: no/such/path',
                str(cm.exception))

    def testVariables(self):
        builder = ConfigBuilder().add_variable('var1', 'val1').add_variable('var2', 'val2')
        self.assertDictEqual({'var1': 'val1', 'var2': 'val2'}, builder.build().variables)

        builder.clear_variables()
        self.assertDictEqual({}, builder.build().variables)

    def testVariables_preventNonStrings(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            ConfigBuilder().add_variable(4, 'val1')
        self.assertEqual('variable must be a string, but instead was: 4', str(cm.exception))

    def testCompilerRules(self):
        rule1, rule2 = CompilerRule(), CompilerRule()
        builder = ConfigBuilder().add_compiler_rules(rule1, rule2)
        self.assertSequenceEqual([rule1, rule2], builder.build().compiler_rules)

        builder.clear_compiler_rules()
        self.assertSequenceEqual([], builder.build().compiler_rules)

    def testCompilerRules_preventNonRules(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            ConfigBuilder().add_compiler_rules(4)
        self.assertEqual(
                'compiler_rule must be a CompilerRule, but instead was: 4',
                str(cm.exception))

    def testPreprocessRules(self):
        rule1, rule2 = Rule(), Rule()
        builder = ConfigBuilder().add_preprocess_rules(rule1, rule2)
        self.assertSequenceEqual([rule1, rule2], builder.build().preprocess_rules)

        builder.clear_preprocess_rules()
        self.assertSequenceEqual([], builder.build().preprocess_rules)

    def testPreprocessRules_preventNonRules(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            ConfigBuilder().add_preprocess_rules(4)
        self.assertEqual(
                'preprocess_rule must be a Rule object, but instead was: 4',
                str(cm.exception))

    def testPostprocessRules(self):
        rule1, rule2 = Rule(), Rule()
        builder = ConfigBuilder().add_postprocess_rules(rule1, rule2)
        self.assertSequenceEqual([rule1, rule2], builder.build().postprocess_rules)

        builder.clear_postprocess_rules()
        self.assertSequenceEqual([], builder.build().postprocess_rules)

    def testPostprocessRules_preventNonRules(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            ConfigBuilder().add_postprocess_rules(4)
        self.assertEqual(
                'postprocess_rule must be a Rule object, but instead was: 4',
                str(cm.exception))

    def testRules(self):
        rule1, rule2, rule3, = Rule(), CompilerRule(), Rule()
        builder = ConfigBuilder().add_preprocess_rules(rule1)
        builder.add_compiler_rules(rule2)
        builder.add_postprocess_rules(rule3)
        self.assertSequenceEqual([rule1, rule2, rule3], builder.build().rules)

    def testConfigIsImmutable(self):
        with mock.patch('os.path.isdir', lambda s: True):
            builder = ConfigBuilder().add_template_dirs('template/path1', 'template/path2')
        builder.add_variable('var1', 'val1')
        config = builder.build()

        # Verify config was constructed correctly.
        self.assertSequenceEqual(['template/path1', 'template/path2'], config.template_dirs)
        self.assertDictEqual({'var1': 'val1'}, config.variables)

        new_builder = config.to_builder()
        new_builder.clear_template_dirs()
        new_builder.add_variable('var2', 'val2')

        # Verify previously built config was not affected by changes to new_builder.
        self.assertSequenceEqual(['template/path1', 'template/path2'], config.template_dirs)
        self.assertDictEqual({'var1': 'val1'}, config.variables)
