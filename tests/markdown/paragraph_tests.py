from utils import TemplarTest, main

class ParagraphTest(TemplarTest):
    def testBasic(self):
        text = """
        This text should be in a single paragraph
        that contains multiple lines
        such as this one.
        """
        expect = """
        <p>This text should be in a single paragraph
        that contains multiple lines
        such as this one.</p>
        """
        self.assertMarkdown(text, expect)

    def testMultiple(self):
        text = """
        This text should be in a single paragraph
        that contains multiple lines
        such as this one.

        This is another paragraph
        that should be separate from the first one
        """
        expect = """
        <p>This text should be in a single paragraph
        that contains multiple lines
        such as this one.</p>

        <p>This is another paragraph
        that should be separate from the first one</p>
        """
        self.assertMarkdown(text, expect)

    def testNoLeadingWhitespace(self):
        text = """
        Stuff

           This text has three leading spaces
        so it is still a paragraph
        """
        expect = """
        <p>Stuff</p>

        <p>This text has three leading spaces
        so it is still a paragraph</p>
        """
        self.assertMarkdown(text, expect)

class HorizontalRuleTest(TemplarTest):
    def testBasic(self):
        text = """
        paragraph here

        ---

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        paragraph here

        ***

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

    def testSpaces(self):
        text = """
        paragraph here

        - - -

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        paragraph here

        * * *

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

    def testExtra(self):
        text = """
        paragraph here

        -------------

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        paragraph here

        **************

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

    def testInvalidHorizontalRule(self):
        text = """
        paragraph here

        --

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <p>--</p>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        paragraph here

        **

        Horizontal rule above
        """
        expect = """
        <p>paragraph here</p>

        <hr/>

        <p>Horizontal rule above</p>
        """
        self.assertMarkdownNotEqual(text, expect)

class EscapeTest(TemplarTest):
    def testBasic(self):
        self.assertMarkdown(r'\\', r"<p>\</p>")
        self.assertMarkdown(r'\`', r"<p>`</p>")
        self.assertMarkdown(r'\*', r"<p>*</p>")
        self.assertMarkdown(r'\_', r"<p>_</p>")
        self.assertMarkdown(r'\{\}', r"<p>{}</p>")
        self.assertMarkdown(r'\[\]', r"<p>[]</p>")
        self.assertMarkdown(r'\(\)', r"<p>()</p>")
        self.assertMarkdown(r'\#', r"<p>#</p>")
        self.assertMarkdown(r'\+', r"<p>+</p>")
        self.assertMarkdown(r'\-', r"<p>-</p>")
        self.assertMarkdown(r'\.', r"<p>.</p>")
        self.assertMarkdown(r'\!', r"<p>!</p>")

if __name__ == '__main__':
    main()
