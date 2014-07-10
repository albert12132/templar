from tests.test_utils import ConfigTest, main
from templar.__main__ import get_paths, configure
from templar.utils.html import HeaderParser

class ConfigPathTest(ConfigTest):
    def testTemplarIsRoot(self):
        templar_path = 'templar/__main__.py'
        source_path = 'templar/test/src/markdown'
        expect = [
            'templar',
            'templar/test',
            'templar/test/src',
            'templar/test/src/markdown',
        ]
        self.assertEqual(get_paths(templar_path, source_path), expect)

    def testTemplarAncestorIsRoot(self):
        templar_path = 'home/templar/__main__.py'
        source_path = 'home/test/src/markdown'
        expect = [
            'home',
            'home/test',
            'home/test/src',
            'home/test/src/markdown',
        ]
        self.assertEqual(get_paths(templar_path, source_path), expect)

    def testTemplarAncestorIsNotRoot(self):
        templar_path = 'home/project/templar/__main__.py'
        source_path = 'home/project/test/src/markdown'
        expect = [
            'home/project',
            'home/project/test',
            'home/project/test/src',
            'home/project/test/src/markdown',
        ]
        self.assertEqual(get_paths(templar_path, source_path), expect)

    def testSourceIsRoot(self):
        templar_path = 'home/project/templar/__main__.py'
        source_path = 'home'
        expect = [
            'home',
        ]
        self.assertEqual(get_paths(templar_path, source_path), expect)

class ConfigImportTest(ConfigTest):
    def testBasic(self):
        paths = [
            'home',
        ]
        files = {
            'home/config.py': {
                'VARIABLES': {
                    'hello': 'world',
                },
                'SUBSTITUTIONS': [
                    ('regex', 'sub'),
                ],
                'TEMPLATE_DIRS': [
                    'test.html',
                ],
            }
        }
        self.assertConfig(files['home/config.py'], paths, files=files)

    def testMissingConfigAtRoot(self):
        paths = [
            'home',
            'home/test',
        ]
        files = {
            'home/test/config.py': {
                'VARIABLES': {
                    'hello': 'world',
                },
                'SUBSTITUTIONS': [
                    ('regex', 'sub'),
                ],
                'TEMPLATE_DIRS': [
                    'test.html',
                ],
            }
        }
        self.assertConfig(files['home/test/config.py'],
                          paths, files=files)

    def testMissingConfigAtSource(self):
        paths = [
            'home',
            'home/test',
        ]
        files = {
            'home/config.py': {
                'VARIABLES': {
                    'hello': 'world',
                },
                'SUBSTITUTIONS': [
                    ('regex', 'sub'),
                ],
                'TEMPLATE_DIRS': [
                    'test.html',
                ],
            }
        }
        self.assertConfig(files['home/config.py'],
                          paths, files=files)

    def testMultipleConfigs(self):
        paths = [
            'home',
            'home/test',
        ]
        files = {
            'home/config.py': {
                'VARIABLES': {
                    'hello': 'world',
                },
                'SUBSTITUTIONS': [
                    ('regex', 'sub'),
                ],
                'TEMPLATE_DIRS': [
                    'test.html',
                ],
            },
            'home/test/config.py': {
                'VARIABLES': {
                    'auto': 'maton',
                },
                'SUBSTITUTIONS': [
                    ('stuff', 'here'),
                ],
                'TEMPLATE_DIRS': [
                    'test2.html',
                ],
            }
        }
        self.assertConfig({
            'VARIABLES': {
                'auto': 'maton',
                'hello': 'world',
            },
            'SUBSTITUTIONS': [
                ('regex', 'sub'),
                ('stuff', 'here'),
            ],
            'TEMPLATE_DIRS': [
                'test.html',
                'test2.html',
            ]
        }, paths, files=files)

    def testNoConfigs(self):
        paths = [
            'home',
            'home/test',
        ]
        self.assertConfig({
            'VARIABLES': {
            },
        }, paths)

    def testTocBuilder(self):
        paths = [
            'home',
            'home/test',
        ]
        files = {
            'home/config.py': {
                'VARIABLES': {
                    'hello': 'world',
                },
                'SUBSTITUTIONS': [
                ],
                'TEMPLATE_DIRS': [
                ],
                'TOC_BUILDER': HeaderParser,
            },
        }
        self.assertConfig(files['home/config.py'], paths, files=files)


if __name__ == '__main__':
    main()

