from utils import MarkdownTest, main

class CodeblockTest(MarkdownTest):
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

    def testNewline(self):
        text = """
        Text here

            def hello(world):
                return world

            print(hello(hi))
        """
        expect = """
        <p>Text here</p>

        <pre><code>def hello(world):
            return world

        print(hello(hi))</code></pre>
        """
        self.assertMarkdown(text, expect)

        text = """
        Text here

            def hello(world):
                return world



            print(hello(hi))
        """
        expect = """
        <p>Text here</p>

        <pre><code>def hello(world):
            return world

        print(hello(hi))</code></pre>
        """
        self.assertMarkdown(text, expect)

    def testNotACodeblock(self):
        text = """
        Stuff

           Only three spaces, not a codeblock
            This should be in codeblock
        """
        expect = """
        <p>Stuff</p>

        <p>Only three spaces, not a codeblock</p>

        <pre><code>This should be in codeblock</code></pre>
        """
        self.assertMarkdownIgnoreWS(text, expect)

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

    def preserveEmphasisDelimiters(self):
        text = """
        Stuff

            Some *em*s
            Some **strong**s
            Some ***strong em***s
            Some _em_s
            Some __strong__s
            Some ___strong em___s
            Some `code`s
        """
        expect = """
        <p>Stuff</p>

        <pre><code>Some *em*s
        Some **strong**s
        Some ***strong em***s
        Some _em_s
        Some __strong__s
        Some ___strong em___s
        Some `code`s</code></pre>
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

    def preserveHeaderMarkers(self):
        text = """
        Stuff

            Setext Header1
            ==============

            Setext Header2
            --------------

            # Atx Header 1
            ## Atx Header 2
            ### Atx Header 3
            #### Atx Header 4
            ##### Atx Header 5
            ###### Atx Header 6
        """
        expect = """
        <p>Stuff</p>

        <pre><code>Setext Header1
        ==============

        Setext Header2
        --------------

        # Atx Header 1
        ## Atx Header 2
        ### Atx Header 3
        #### Atx Header 4
        ##### Atx Header 5
        ###### Atx Header 6</code></pre>
        """
        self.assertMarkdown(text, expect)

    def preserveBlockquote(self):
        text = """
        Stuff

            > blockquote
            > attempt here
        """
        expect = """
        <p>Stuff</p>

        <pre><code>&gt; blockquote
        &gt; attempt here</code></pre>
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
