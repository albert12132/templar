from utils import TemplarTest, main

class BlockquoteTest(TemplarTest):
    def testBasic(self):
        text = """
        Text here

            Codeblock
            contents

        Close
        """
        expect = """
        <p>Text here</p>

        <pre><code>Codeblock
        contents</code></pre>

        <p>Close</p>
        """
        self.assertMarkdown(text, expect)

    def testPreserveWhitespace(self):
        text = """
        Stuff
            def hello():
                return world
        """
        expect = """
        <p>Stuff</p>

        <pre><code>def hello():
            return world</code></pre>
        """
        self.assertMarkdown(text, expect)

        text = """
        Stuff
            hello     daphne
        """
        expect = """
        <p>Stuff</p>

        <pre><code>hello     daphne</code></pre>
        """
        self.assertMarkdown(text, expect)

    def testEscape(self):
        text = """
        Stuff

            Some <example> HTML tags
        """
        expect = """
        <p>Stuff</p>

        <pre><code>Some &lt;example&gt; HTML tags</code></pre>
        """
        self.assertMarkdown(text, expect)

        text = """
        Stuff

            At AT&T Park
        """
        expect = """
        <p>Stuff</p>

        <pre><code>At AT&amp;T Park</code></pre>
        """
        self.assertMarkdown(text, expect)


    def testSeparated(self):
        text = """
        Stuff

            Codeblock here

        Not in codeblock

            Codeblock here
        """
        expect = """
        <p>Stuff</p>

        <pre><code>Codeblock here</code></pre>

        <p>Not in codeblock</p>

        <pre><code>Codeblock here</code></pre>
        """
        self.assertMarkdownIgnoreWS(text, expect)

if __name__ == '__main__':
    main()
