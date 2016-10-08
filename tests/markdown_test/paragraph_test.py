from tests.markdown_test.test_utils import MarkdownTest

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

    def testLineBreak(self):
        text = """
        Stuff This text is text with a line break  
        so it is still a paragraph  

        Another line break!
        """
        expect = """
        <p>Stuff This text is text with a line break
        <br/>
        so it is still a paragraph
        <br/>

        Another line break!</p>
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

class MiscellaneousTest(MarkdownTest):
    def testDoubleDashInLinkIsPreserved(self):
        text = """
        This is [a link](http://example.com/id--tag)
        """
        expect = """
        <p>This is <a href="http://example.com/id--tag">a link</a></p>
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

    def testHtmlEscapes(self):
        self.assertMarkdown("&", "<p>&amp;</p>")
        self.assertMarkdown("&reg;", "<p>&reg;</p>")

    def testComment(self):
        text = """
        <!-- HTML comment -->
        """
        expect = """
        <!-- HTML comment -->
        """
        self.assertMarkdown(text, expect)

        text = """
        Some stuff <!-- this is a comment --> here
        """
        expect = """
        <p>Some stuff <!-- this is a comment --> here</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        Some stuff <!--
        this is
        a comment --> here
        """
        expect = """
        <p>Some stuff <!--
        this is
        a comment --> here</p>
        """
        self.assertMarkdown(text, expect)

    def testPandocComment(self):
        text = """
        <!--- pandoc comment -->
        Some stuff here
        """
        expect = """
        <p>Some stuff here</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        <!---
        pandoc comment -->
        Some stuff here
        """
        expect = """
        <p>Some stuff here</p>
        """
        self.assertMarkdown(text, expect)
