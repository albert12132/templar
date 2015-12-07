from tests.markdown_test.test_utils import MarkdownTest
from templar.markdown import convert, Markdown

class SetextTest(MarkdownTest):
    def testBasic(self):
        simple = """
        Hello World!
        ============
        """
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertMarkdown(simple, expect)

        simple = """
        Hello World!
        ------------
        """
        expect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertMarkdown(simple, expect)

    def testShortUnderline(self):
        simple = """
        Hello World!
        =
        """
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertMarkdown(simple, expect)

        simple = """
        Hello World!
        -
        """
        expect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertMarkdown(simple, expect)

    def testEmphasisH1(self):
        italics = """
        Some *italics*
        ==============
        """
        expect = '<h1 id="some-italics">Some <em>italics</em></h1>'
        self.assertMarkdown(italics, expect)

        bold = """
        Some **bold**
        =
        """
        expect = '<h1 id="some-bold">Some <strong>bold</strong></h1>'
        self.assertMarkdown(bold, expect)

        italics_bold = """
        Some ***italics bold***
        =
        """
        expect = '<h1 id="some-italics-bold">Some <strong><em>italics bold</em></strong></h1>'
        self.assertMarkdown(italics_bold, expect)

        code = """
        Some `code here`
        =
        """
        expect = '<h1 id="some-code-here">Some <code>code here</code></h1>'
        self.assertMarkdown(code, expect)

    def testEmphasisH2(self):
        italics = """
        Some *italics*
        --------------
        """
        expect = '<h2 id="some-italics">Some <em>italics</em></h2>'
        self.assertMarkdown(italics, expect)

        bold = """
        Some **bold**
        -
        """
        expect = '<h2 id="some-bold">Some <strong>bold</strong></h2>'
        self.assertMarkdown(bold, expect)

        italics_bold = """
        Some ***italics bold***
        -
        """
        expect = '<h2 id="some-italics-bold">Some <strong><em>italics bold</em></strong></h2>'
        self.assertMarkdown(italics_bold, expect)

        code = """
        Some `code here`
        -
        """
        expect = '<h2 id="some-code-here">Some <code>code here</code></h2>'
        self.assertMarkdown(code, expect)

    def testTwoNewlines(self):
        simple = """
        Hello World!

        =
        """
        notExpect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertMarkdownNotEqual(simple, notExpect)

        simple = """
        Hello World!

        -
        """
        notExpect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertMarkdownNotEqual(simple, notExpect)

    def testNoParagraph(self):
        text = """
        This should be one paragraph
        Header here
        ===========
        This should be another paragraph
        """
        expect = """
        <p>This should be one paragraph</p>

        <h1 id="header-here">Header here</h1>

        <p>This should be another paragraph</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        This should be one paragraph
        Header here
        -----------
        This should be another paragraph
        """
        expect = """
        <p>This should be one paragraph</p>

        <h2 id="header-here">Header here</h2>

        <p>This should be another paragraph</p>
        """
        self.assertMarkdown(text, expect)

    def testMixed(self):
        text = """
        Not a header
        =-
        """
        expect = """
        <p>Not a header
        =-</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        Not a header
        -=
        """
        expect = """
        <p>Not a header
        -=</p>
        """
        self.assertMarkdown(text, expect)

    def testEscaped(self):
        text = r"""
        Not a header
        \-----------
        """
        expect = """
        <p>Not a header
        -----------</p>
        """
        self.assertMarkdown(text, expect)

    def testOptionalId(self):
        text = r"""
        Header      { #test.class1 .class2 }
        ------
        """
        expect = """
        <h2 id="test" class="class1 class2">Header</h2>
        """
        self.assertMarkdown(text, expect)

class AtxHeaders(MarkdownTest):
    def testBasic(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertMarkdown('#'*i + ' ' + title, expect.format(i))

    def testNoLeadingWhitespace(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertMarkdown('#'*i + title, expect.format(i))

    def testExtraLeadingWhitespace(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertMarkdown('#'*i + '  ' + title, expect.format(i))

    def testTrailingHashes(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertMarkdown('#'*i + title + ' ####', expect.format(i))

        for i in range(1, 7):
            self.assertMarkdown('#'*i + title + '####', expect.format(i))

    def testNoParagraph(self):
        text = """
        This should be one paragraph
        ### Header here
        This should be another paragraph
        """
        expect = """
        <p>This should be one paragraph</p>

        <h3 id="header-here">Header here</h3>

        <p>This should be another paragraph</p>
        """
        self.assertMarkdown(text, expect)

    def testEscape(self):
        text = r"""
        \### Not a header
        """
        expect = """
        <p>### Not a header</p>
        """
        self.assertMarkdown(text, expect)

        text = r"""
        #\## This is a level 1 header
        """
        expect = """
        <h1 id="this-is-a-level-1-header">## This is a level 1 header</h1>
        """
        self.assertMarkdown(text, expect)

    def testOptionalId(self):
        text = r"""
        ### Header      { #test.class1 .class2 }
        """
        expect = """
        <h3 id="test" class="class1 class2">Header</h3>
        """
        self.assertMarkdown(text, expect)

    def testHashBlankLine(self):
        text = r"""
        #

        Stuff here
        """
        expect = """
        <h1></h1>


        <p>Stuff here</p>
        """
        self.assertMarkdown(text, expect)

class SlugTests(MarkdownTest):
    def testBasic(self):
        simple = """
        Hello World!
        =
        """
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertMarkdown(simple, expect)

        simple = """
        With some 1337 hax0r
        =
        """
        expect = '<h1 id="with-some-1337-hax0r">With some 1337 hax0r</h1>'
        self.assertMarkdown(simple, expect)

    def testPunctuation(self):
        simple = """
        He!1. ^0#r$
        =
        """
        expect = '<h1 id="he-1-0-r">He!1. ^0#r$</h1>'
        self.assertMarkdown(simple, expect)

    def testWhitespace(self):
        simple = """
        Lots       of  whitespace
        =
        """
        expect = '<h1 id="lots-of-whitespace">Lots       of  whitespace</h1>'
        self.assertMarkdown(simple, expect)

        simple = '   leading whitespace\n='
        expect = '<h1 id="leading-whitespace">leading whitespace</h1>'
        self.assertEqual(expect, convert(simple))
