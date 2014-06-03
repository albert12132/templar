from utils import TemplarTest, main
from markdown import convert, Markdown

class SetextH1Test(TemplarTest):
    def setup(self):
        self.simple = "Hello World!\n"

    def testBasic(self):
        self.simple += '=' * len(simple)
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(simple))

    def testShortUnderline(self):
        self.simple += '\n='
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(simple))

    def testNewlines(self):
        self.simple += '\n='
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert('\n' + simple + '\n'))

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


if __name__ == '__main__':
    main()
