"""End-to-end test for templar/cli/templar.py"""

from templar.api.config import ConfigBuilderError
from templar.cli import templar

import io
import mock
import os.path
import shutil
import unittest

STAGING_DIR = os.path.join('tests', 'cli', 'staging')
TEST_DATA = os.path.join('tests', 'cli', 'test_data')

class TemplarTest(unittest.TestCase):
    def setUp(self):
        os.mkdir(STAGING_DIR)

    def tearDown(self):
        shutil.rmtree(STAGING_DIR)

    def testConfigNotFound(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            templar.run(templar.flags([
                '-s', os.path.join(TEST_DATA, 'file.md'),
                '-c', os.path.join('no', 'such', 'config.py'),
                '--debug',
            ]))
        self.assertEqual('Could not find config file: no/such/config.py', str(cm.exception))

    def testConfig_withNoVariableFails(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            templar.run(templar.flags([
                '-s', os.path.join(TEST_DATA, 'file.md'),
                '-c', os.path.join(TEST_DATA, 'no_variable_config.py'),
                '--debug',
            ]))
        self.assertEqual(
                'Could not load config file "tests/cli/test_data/no_variable_config.py": '
                'config files must contain a variable called "config" that is assigned to '
                'a Config object.',
                str(cm.exception))

    def testConfig_whoseVariableIsNotAConfig(self):
        with self.assertRaises(ConfigBuilderError) as cm:
            templar.run(templar.flags([
                '-s', os.path.join(TEST_DATA, 'file.md'),
                '-c', os.path.join(TEST_DATA, 'invalid_variable_config.py'),
                '--debug',
            ]))
        self.assertEqual(
                'Could not load config file "tests/cli/test_data/invalid_variable_config.py": '
                'config files must contain a variable called "config" that is assigned to '
                'a Config object.',
                str(cm.exception))

    def testWriteToDestination(self):
        destination_file = os.path.join(STAGING_DIR, 'destination.html')
        templar.run(templar.flags([
            '-s', os.path.join(TEST_DATA, 'file.md'),
            '-c', os.path.join(TEST_DATA, 'config.py'),
            '-t', 'template.html',
            '-d', destination_file,
            '--debug',
        ]))
        self.assertTrue(os.path.isfile(destination_file))
        with open(os.path.join(destination_file), 'r') as f:
            self.assertEqual('<p>Content in my block.</p>', f.read())

    def testPrint(self):
        destination_file = os.path.join(STAGING_DIR, 'destination.html')
        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            templar.run(templar.flags([
                '-s', os.path.join(TEST_DATA, 'file.md'),
                '-c', os.path.join(TEST_DATA, 'config.py'),
                '-t', 'template.html',
                '-d', destination_file,
                '--print',
                '--debug',
            ]))
        # Using --print should prevent writing to the destination.
        self.assertFalse(os.path.isfile(destination_file))
        # There should be trailing newline because the print function adds a
        # newline at the end.
        self.assertEqual('<p>Content in my block.</p>\n', mock_stdout.getvalue())

    def testPrintErrorIfDebugFlagNotUsed(self):
        destination_file = os.path.join(STAGING_DIR, 'destination.html')
        with self.assertRaises(SystemExit) as cm:
            with mock.patch('sys.stderr', new_callable=io.StringIO) as mock_stdout:
                templar.run(templar.flags([
                    # Missing both source and template causes an error.
                    '-c', os.path.join(TEST_DATA, 'config.py'),
                ]))
        self.assertFalse(os.path.isfile(destination_file))
        self.assertEqual(
                'PublishError: When publishing, source and template cannot both be omitted.\n',
                mock_stdout.getvalue())
        self.assertNotEqual(cm.exception.code, 0)


    def testCreateDestinationNonExistentDirectory(self):
        # The directiory STAGING_DIR/dir does not exist beforehand.
        self.assertFalse(os.path.isdir(os.path.join(STAGING_DIR, 'dir')))

        destination_file = os.path.join(STAGING_DIR, 'dir', 'destination.html')
        templar.run(templar.flags([
            '-s', os.path.join(TEST_DATA, 'file.md'),
            '-c', os.path.join(TEST_DATA, 'config.py'),
            '-t', 'template.html',
            '-d', destination_file,
            '--debug',
        ]))
        self.assertTrue(os.path.isfile(destination_file))
        with open(os.path.join(destination_file), 'r') as f:
            self.assertEqual('<p>Content in my block.</p>', f.read())



