from tests.test_utils import LinkTest, main

class IncludeTest(LinkTest):
    def testBasic(self):
        files = {
            'text': """
            <include test.md>
            """,
            'test.md': """
            Hello world!
            """,
        }
        expect = """
        Hello world!
        """
        self.assertLink('text', expect, files)

        files = {
            'text': """
            <include path/to/test.md>
            """,
            'path/to/test.md': """
            Hello world!
            """,
        }
        expect = """
        Hello world!
        """
        self.assertLink('text', expect, files)

    def testNoIncludes(self):
        files = {
            'text': """
            No includes
            can be found here
            """
        }
        expect = files['text']
        self.assertLink('text', expect, files)

    def testSurroundingText(self):
        files = {
            'text': """
            Begin
            <include test.md>
            Close
            """,
            'test.md': """
            Hello world!
            """,
        }
        expect = """
        Begin
        Hello world!
        Close
        """
        self.assertLink('text', expect, files)

    def testNewline(self):
        files = {
            'text': """
            Begin

            <include test.md>

            Close
            """,
            'test.md': """
            Hello world!
            """,
        }
        expect = """
        Begin

        Hello world!

        Close
        """
        self.assertLink('text', expect, files)

    def testLeadingWhitespace(self):
        files = {
            'text': """
            Begin

                <include test.py>

            Close
            """,
            'test.py': """
            def hello(world):
                return hi
            """,
        }
        expect = """
        Begin

            def hello(world):
                return hi

        Close
        """
        self.assertLink('text', expect, files)

    def testNestedIncludes(self):
        files = {
            'text': """
            <include fileA>
            """,
            'fileA': """
            <include fileB>
            """,
            'fileB': """
            <include fileC>
            """,
            'fileC': """
            <include fileD>
            """,
            'fileD': """
            Target!
            """,
        }
        expect = """
        Target!
        """
        self.assertLink('text', expect, files)

    def testBlock(self):
        files = {
            'text': """
            <include test.md:blockA>
            """,
            'test.md': """
            Hello
            <block blockA>
            World!
            </block blockA>
            """,
        }
        expect = """
        World!
        """
        self.assertLink('text', expect, files)

        files = {
            'text': """
            <include test.md:blockA>
            """,
            'test.md': """
            Hello
            <block blockA>
            Header
            ------

            World!
            </block blockA>
            """,
        }
        expect = """
        Header
        ------

        World!
        """
        self.assertLink('text', expect, files)

    def testMultipleBlocksInSameFile(self):
        files = {
            'text': """
            <include test.md:blockA>

            In between

            <include test.md:blockB>
            """,
            'test.md': """
            Hello
            <block blockA>
            World!
            </block blockA>

            <block blockB>
            Stuff here
            </block blockB>
            """,
        }
        expect = """
        World!

        In between

        Stuff here
        """
        self.assertLink('text', expect, files)

    def testSameBlockMultipleTimes(self):
        files = {
            'text': """
            <include test.md:blockA>

            In between

            <include test.md:blockA>
            """,
            'test.md': """
            Hello
            <block blockA>
            World!
            </block blockA>
            """,
        }
        expect = """
        World!

        In between

        World!
        """
        self.assertLink('text', expect, files)

    def testMultipleFilesSameBlockName(self):
        files = {
            'text': """
            <include test.md:blockA>

            In between

            <include foo.md:blockA>
            """,
            'test.md': """
            <block blockA>
            Test
            </block blockA>
            """,
            'foo.md': """
            <block blockA>
            Foo
            </block blockA>
            """,
        }
        expect = """
        Test

        In between

        Foo
        """
        self.assertLink('text', expect, files)

    def testBlockRegex(self):
        files = {
            'text': """
            <include test.md:block\d>
            """,
            'test.md': """
            <block block0>
            Zero
            </block block0>
            <block blockA>
            A
            </block blockA>
            <block block2>
            Two
            </block block2>
            """,
        }
        expect = """
        Zero
        Two
        """
        self.assertLink('text', expect, files)

    def testBlockRegexExcludeAll(self):
        files = {
            'text': """
            <include test.md:.*>
            """,
            'test.md': """
            <block block0>
            Zero
            </block block0>
            <block blockA>
            A
            </block blockA>
            <block block2>
            Two
            </block block2>
            """,
        }
        expect = """
        Zero
        A
        Two
        """
        self.assertLink('text', expect, files)

    def testExplicitAll(self):
        files = {
            'text': """
            <include test.md:all>
            """,
            'test.md': """
            Hello world
            <block blockA>
            Here we go
            </block blockA>
            """,
        }
        expect = """
        Hello world
        Here we go
        """
        self.assertLink('text', expect, files)

    def testRelativePath(self):
        files = {
            'text': """
            <include stuff/test.md>
            """,
            'stuff/test.md': """
            Hello world!
            <include test.py>
            """,
            'stuff/test.py': """
            New Age
            """,
        }
        expect = """
        Hello world!
        New Age
        """
        self.assertLink('text', expect, files)

    def testPreserveBlocks(self):
        files = {
            'text': """
            <block hello>
            Hello
            </block hello>
            """
        }
        expect = files['text']
        self.assertLink('text', expect, files)

    def testRemoveIncludedBlocks(self):
        files = {
            'text': """
            <include test.md>
            """,
            'test.md': """
            <block blockA>
            Hello
            </block blockA>
            """,
        }
        expect = """
        Hello
        """
        self.assertLink('text', expect, files)


if __name__ == '__main__':
    main()

