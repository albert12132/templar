from tests.markdown_test.test_utils import MarkdownTest

class BlockquoteTest(MarkdownTest):
    def testBasic(self):
        text = "> Block quote basic"
        expect = """
        <blockquote><p>Block quote basic</p></blockquote>
        """
        self.assertMarkdown(text, expect)

    def testMultiline(self):
        text = """
        > Block quote
        > here and there
        > and everywhere
        """
        expect = """
        <blockquote><p>Block quote
        here and there
        and everywhere</p></blockquote>
        """
        self.assertMarkdown(text, expect)

    def testMultilineNotPretty(self):
        text = """
        > Block quote
        here and there
        and everywhere
        """
        expect = """
        <blockquote><p>Block quote
        here and there
        and everywhere</p></blockquote>
        """
        self.assertMarkdown(text, expect)

    def testMultipleParagraphs(self):
        text = """
        > Block quote
        > here and there
        > and everywhere
        >
        > Another paragraph
        > here
        """
        expect = """
        <blockquote><p>Block quote
        here and there
        and everywhere</p>

        <p>Another paragraph
        here</p></blockquote>
        """
        self.assertMarkdown(text, expect)

        text = """
        > Block quote
        > here and there
        > and everywhere

        > Another paragraph
        > here
        """
        expect = """
        <blockquote><p>Block quote
        here and there
        and everywhere</p>

        <p>Another paragraph
        here</p></blockquote>
        """
        self.assertMarkdown(text, expect)

        text = """
        > Block quote
        here and there
        and everywhere

        > Another paragraph
        here
        """
        expect = """
        <blockquote><p>Block quote
        here and there
        and everywhere</p>

        <p>Another paragraph
        here</p></blockquote>
        """
        self.assertMarkdown(text, expect)

    def testSetextHeaders(self):
        text = """
        > Setext header
        > =============
        """
        expect = """
        <blockquote>
        <h1 id="setext-header">Setext header</h1>
        </blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        > Setext header
        > -------------
        """
        expect = """
        <blockquote>
        <h2 id="setext-header">Setext header</h2>
        </blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testAtxHeaders(self):
        text = """
        > ### Atx header
        """
        expect = """
        <blockquote>
        <h3 id="atx-header">Atx header</h3>
        </blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testCodeblock(self):
        text = """
        > Some text
        >     Code block here
        > Closing text
        """
        expect = """
        <blockquote>
        <p>Some text</p>

        <pre><code>Code block here</code></pre>

        <p>Closing text</p>
        </blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        > Some text
        >     Code block here
        >     Second line
        > Closing text
        """
        expect = """
        <blockquote>
        <p>Some text</p>

        <pre><code>Code block here
        Second line</code></pre>

        <p>Closing text</p>
        </blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testNestedBlockquote(self):
        text = """
        > Some text
        > > Nested blockquote
        """
        expect = """
        <blockquote><p>Some text</p>

        <blockquote><p>Nested blockquote</p></blockquote></blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        > Some text
        > > Header in Nested
        > > ================
        """
        expect = """
        <blockquote>
        <p>Some text</p>

        <blockquote>
        <h1 id="header-in-nested">Header in Nested</h1>
        </blockquote>
        </blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testList(self):
        text = """
        > Some text
        > * Item 1
        > * Item 2
        """
        expect = """
        <blockquote><p>Some text</p>

        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
        </ul></blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        > Some text
        > 1. Item 1
        > 2. Item 2
        """
        expect = """
        <blockquote><p>Some text</p>

        <ol>
          <li>Item 1</li>
          <li>Item 2</li>
        </ol></blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testSeparated(self):
        text = """
        > Some text
        > here

        Not in blockquote

        > Some more text
        """
        expect = """
        <blockquote><p>Some text
        here</p>
        </blockquote>

        <p>Not in blockquote</p>

        <blockquote><p>Some more text</p></blockquote>
        """
        self.assertMarkdownIgnoreWS(text, expect)

