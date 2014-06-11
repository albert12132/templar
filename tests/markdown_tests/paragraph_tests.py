from utils import MarkdownTest, main

class ParagraphTest(MarkdownTest):
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

class HorizontalRuleTest(MarkdownTest):
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

        <p>&mdash;</p>

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


class MiscellaneousTest(MarkdownTest):
    def testEmDash(self):
        text = """
        This is an example -- of an em dash
        """
        expect = """
        <p>This is an example &mdash; of an em dash</p>
        """
        self.assertMarkdown(text, expect)

    def testEmDashNoWhitespace(self):
        text = """
        This is an example--of an em dash
        """
        expect = """
        <p>This is an example&mdash;of an em dash</p>
        """
        self.assertMarkdown(text, expect)

    def testNotAnEmDash(self):
        text = """
        This is not an em dash
        --
        """
        expect = """
        <h2 id="this-is-not-an-em-dash">This is not an em dash</h2>
        """
        self.assertMarkdown(text, expect)

        text = """
        This is not --- an em dash
        """
        expect = """
        <p>This is not --- an em dash</p>
        """
        self.assertMarkdown(text, expect)

    def testEscapes(self):
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
