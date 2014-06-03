from utils import TemplarTest, main
from markdown import convert, Markdown

class SetextH1Test(TemplarTest):
    def setUp(self):
        super().setUp()
        self.simple = "Hello World!\n"

    def testBasic(self):
        self.simple += '=' * len(self.simple)
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(self.simple))

    def testShortUnderline(self):
        self.simple += '='
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(self.simple))

    def testNewlines(self):
        self.simple += '='
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(self.simple))

    def testEmphasis(self):
        italics = "Some *italics*\n="
        expect = '<h1 id="some-italics">Some <em>italics</em></h1>'
        self.assertEqual(expect, convert(italics))

        bold = "Some **bold**\n="
        expect = '<h1 id="some-bold">Some <strong>bold</strong></h1>'
        self.assertEqual(expect, convert(bold))

        italics_bold = "Some ***italics bold***\n="
        expect = '<h1 id="some-italics-bold">Some <strong><em>italics bold</em></strong></h1>'
        self.assertEqual(expect, convert(italics_bold))

        code = "Some `code here`\n="
        expect = '<h1 id="some-code-here">Some <code>code here</code></h1>'
        self.assertEqual(expect, convert(code))

    def testTwoNewlines(self):
        self.simple += '\n='
        notExpect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertNotEqual(notExpect, convert(self.simple))

class SetextH2Test(TemplarTest):
    def setUp(self):
        super().setUp()
        self.simple = "Hello World!\n"

    def testBasic(self):
        self.simple += '-' * len(self.simple)
        expect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertEqual(expect, convert(self.simple))

    def testShortUnderline(self):
        self.simple += '-'
        expect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertEqual(expect, convert(self.simple))

    def testNewlines(self):
        self.simple += '-'
        expect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertEqual(expect, convert('\n' + self.simple + '\n'))

    def testEmphasis(self):
        italics = "Some *italics*\n-"
        expect = '<h2 id="some-italics">Some <em>italics</em></h2>'
        self.assertEqual(expect, convert(italics))

        bold = "Some **bold**\n-"
        expect = '<h2 id="some-bold">Some <strong>bold</strong></h2>'
        self.assertEqual(expect, convert(bold))

        italics_bold = "Some ***italics bold***\n-"
        expect = '<h2 id="some-italics-bold">Some <strong><em>italics bold</em></strong></h2>'
        self.assertEqual(expect, convert(italics_bold))

        code = "Some `code here`\n-"
        expect = '<h2 id="some-code-here">Some <code>code here</code></h2>'
        self.assertEqual(expect, convert(code))

    def testTwoNewlines(self):
        self.simple += '\n-'
        notExpect = '<h2 id="hello-world">Hello World!</h2>'
        self.assertNotEqual(notExpect, convert(self.simple))

class AtxHeaders(TemplarTest):
    def setUp(self):
        super().setUp()

    def testBasic(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertEqual(expect.format(i), convert('#'*i + ' ' + title))

    def testNoLeadingWhitespace(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertEqual(expect.format(i), convert('#'*i + title))

    def testExtraLeadingWhitespace(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertEqual(expect.format(i), convert('#'*i + '    ' + title))

    def testTrailingHashes(self):
        title = "Title Here"
        expect = '<h{0} id="title-here">Title Here</h{0}>'
        for i in range(1, 7):
            self.assertEqual(expect.format(i), convert('#'*i + title + ' ####'))

        for i in range(1, 7):
            self.assertEqual(expect.format(i), convert('#'*i + title + '####'))

class SlugTests(TemplarTest):
    def setUp(self):
        super().setUp()

    def testBasic(self):
        simple = 'Hello World!\n='
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(simple))

        simple = 'With some 1337 hax0r\n='
        expect = '<h1 id="with-some-1337-hax0r">With some 1337 hax0r</h1>'
        self.assertEqual(expect, convert(simple))

    def testPunctuation(self):
        simple = 'He!1. ^0#r$\n='
        expect = '<h1 id="he1-0r">He!1. ^0#r$</h1>'
        self.assertEqual(expect, convert(simple))

    def testWhitespace(self):
        simple = 'Lots       of  whitespace\n='
        expect = '<h1 id="lots-of-whitespace">Lots       of  whitespace</h1>'
        self.assertEqual(expect, convert(simple))

        simple = '   leading whitespace\n='
        expect = '<h1 id="leading-whitespace">leading whitespace</h1>'
        self.assertEqual(expect, convert(simple))



if __name__ == '__main__':
    main()
