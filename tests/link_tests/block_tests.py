from utils import LinkTest, main

class BlockTest(LinkTest):
    def testBasic(self):
        text = """
        <block blockA>
        This is block content
        </block blockA>
        """
        expect = """
        This is block content
        """
        expect_cache = {
            ':blockA': "This is block content",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testNoBlocks(self):
        text = """
        There are no
        blocks here
        """
        expect = text
        expect_cache = {
            ':all': text,
        }
        self.assertBlock(text, expect, expect_cache)

    def testContents(self):
        text = """
        Begin
        <block blockA>
        This is block content
        </block blockA>
        End
        """
        expect = """
        Begin
        This is block content
        End
        """
        expect_cache = {
            ':blockA': "This is block content",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testInternalWhitespace(self):
        text = """
        Begin
        <block blockA>

        This is block content

        </block blockA>
        End
        """
        expect = """
        Begin

        This is block content

        End
        """
        expect_cache = {
            ':blockA': "\nThis is block content\n",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testExternalWhitespace(self):
        text = """
        Begin

        <block blockA>
        This is block content
        </block blockA>

        End
        """
        expect = """
        Begin

        This is block content

        End
        """
        expect_cache = {
            ':blockA': "This is block content",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testConsecutiveBlocks(self):
        text = """
        <block blockA>
        This is block A content
        </block blockA>

        <block blockB>
        This is block B content
        </block blockB>
        """
        expect = """
        This is block A content

        This is block B content
        """
        expect_cache = {
            ':blockA': "This is block A content",
            ':blockB': "This is block B content",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testNestedBlocks(self):
        text = """
        <block blockA>
        This is block A content
        <block blockB>
        This is block B content
        </block blockB>
        </block blockA>

        """
        expect = """
        This is block A content
        This is block B content
        """
        expect_cache = {
            ':blockA': expect,
            ':blockB': "This is block B content",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testOverlapBlocks(self):
        text = """
        <block blockA>
        This is block A content
        <block blockB>
        This is block A and B content
        </block blockA>
        This is block B content
        </block blockB>

        """
        expect = """
        This is block A content
        This is block A and B content
        This is block B content
        """
        expect_cache = {
            ':blockA': """
            This is block A content
            This is block A and B content
            """,
            ':blockB': """
            This is block A and B content
            This is block B content
            """,
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testCaseSensitive(self):
        text = """
        <block blockA>
        This is block A content
        </block blockA>

        <block blocka>
        This is block a content
        </block blocka>

        """
        expect = """
        This is block A content

        This is block a content
        """
        expect_cache = {
            ':blockA': """
            This is block A content
            """,
            ':blocka': """
            This is block a content
            """,
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testCaseSensitive(self):
        text = """
        <block blockA>
        This is block A content
        </block blockA>

        <block blocka>
        This is block a content
        </block blocka>

        """
        expect = """
        This is block A content

        This is block a content
        """
        expect_cache = {
            ':blockA': """
            This is block A content
            """,
            ':blocka': """
            This is block a content
            """,
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

    def testExtraCharacers(self):
        text = """
        # <block python>
        def hello(world):
            "*** YOUR CODE HERE ***"
            return hi
        # </block python> #
        """
        expect = """
        def hello(world):
            "*** YOUR CODE HERE ***"
            return hi
        """
        expect_cache = {
            ':python': expect,
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

        text = """
        # <block python>
        def hello(world):
            "*** YOUR CODE HERE ***"
        # <block python-sol>
            return hi
        # </block python-sol>
        # </block python>
        """
        expect = """
        def hello(world):
            "*** YOUR CODE HERE ***"
            return hi
        """
        expect_cache = {
            ':python': expect,
            ':python-sol': "    return hi",
            ':all': expect,
        }
        self.assertBlock(text, expect, expect_cache)

if __name__ == '__main__':
    main()

