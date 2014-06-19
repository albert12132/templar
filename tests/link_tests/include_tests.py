from utils import LinkTest, main

class IncludeTest(LinkTest):
    def testBasic(self):
        text = """
        <include test.md>
        """
        files = {
            'test.md': """
            Hello world!
            """,
        }
        expect = """
        Hello world!
        """
        self.assertLink(text, expect, files)

        text = """
        <include path/to/test.md>
        """
        files = {
            'path/to/test.md': """
            Hello world!
            """,
        }
        expect = """
        Hello world!
        """
        self.assertLink(text, expect, files)

    def testNoIncludes(self):
        text = """
        No includes
        can be found here
        """
        expect = text
        self.assertLink(text, expect)

    def testSurroundingText(self):
        text = """
        Begin
        <include test.md>
        Close
        """
        files = {
            'test.md': """
            Hello world!
            """,
        }
        expect = """
        Begin
        Hello world!
        Close
        """
        self.assertLink(text, expect, files)

    def testNewline(self):
        text = """
        Begin

        <include test.md>

        Close
        """
        files = {
            'test.md': """
            Hello world!
            """,
        }
        expect = """
        Begin

        Hello world!

        Close
        """
        self.assertLink(text, expect, files)

    def testLeadingWhitespace(self):
        text = """
        Begin

            <include test.py>

        Close
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testNestedIncludes(self):
        text = """
        <include fileA>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testBlock(self):
        text = """
        <include test.md:blockA>
        """
        files = {
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
        self.assertLink(text, expect, files)

        text = """
        <include test.md:blockA>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testMultipleBlocksInSameFile(self):
        text = """
        <include test.md:blockA>

        In between

        <include test.md:blockB>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testSameBlockMultipleTimes(self):
        text = """
        <include test.md:blockA>

        In between

        <include test.md:blockA>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testMultipleFilesSameBlockName(self):
        text = """
        <include test.md:blockA>

        In between

        <include foo.md:blockA>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testBlockRegex(self):
        text = """
        <include test.md:block\d>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testBlockRegexExcludeAll(self):
        text = """
        <include test.md:.*>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testExplicitAll(self):
        text = """
        <include test.md:all>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testRelativePath(self):
        text = """
        <include stuff/test.md>
        """
        files = {
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
        self.assertLink(text, expect, files)

    def testPreserveBlocks(self):
        text = """
        <block hello>
        Hello
        </block hello>
        """
        expect = text
        self.assertLink(text, expect)

    def testRemoveIncludedBlocks(self):
        text = """
        <include test.md>
        """
        files = {
            'test.md': """
            <block blockA>
            Hello
            </block blockA>
            """,
        }
        expect = """
        Hello
        """
        self.assertLink(text, expect, files)


if __name__ == '__main__':
    main()

