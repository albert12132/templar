from utils import TemplarTest, main

class ListTest(TemplarTest):
    def testBasic(self):
        text = """
        * item 1
        * item 2
        * item 3
        """
        expect = """
        <ul>
          <li>item 1</li>
          <li>item 2</li>
          <li>item 3</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

        text = """
        1. item 1
        2. item 2
        3. item 3
        """
        expect = """
        <ol>
          <li>item 1</li>
          <li>item 2</li>
          <li>item 3</li>
        </ol>
        """
        self.assertMarkdown(text, expect)

        text = """
        * Some text here that is
          aligned nicely to the side
        * Some text here that is
          aligned nicely to the side
        """
        expect = """
        <ul>
          <li>Some text here that is
          aligned nicely to the side</li>
          <li>Some text here that is
          aligned nicely to the side</li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testNewline(self):
        text = """
        * item 1

        * item 2
        """
        expect = """
        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testNestedList(self):
        text = """
        * item 1
            * item 2
                * item 3
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <ul>
            <li><p>item 2</p>

            <ul>
              <li>item 3</li>
            </ul></li>
          </ul></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testNestedListWithMultipleItems(self):
        text = """
        * item 1
            * item 1
            * item 2
            * item 3
        * item 2
            * item 1
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <ul>
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
          </ul></li>
          <li><p>item 2</p>

          <ul>
            <li>item 1</li>
          </ul></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testNoWrap(self):
        text = """
        * item 1
        this should be in same
        list
        """
        expect = """
        <ul>
          <li>item 1
          this should be in same
          list</li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testParagraphs(self):
        text = """
        * item 1

            This should be in same list item,
            different paragraph
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <p>This should be in same list item,
          different paragraph</p></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        * item 1

            This should be in same list item,
            different paragraph



            Yet another paragraph
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <p>This should be in same list item,
          different paragraph</p>

          <p>Yet another paragraph</p></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testSeparated(self):
        text = """
        * item 1
        * item 2

        Not in list
        * item 1
        * item 2
        """
        expect = """
        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>

        <p>Not in list</p>

        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testNotAList(self):
        text = """
        * * Not a list
        """
        expect = """
        <p>* * Not a list</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        \* Not a list
        """
        expect = """
        <p>* Not a list</p>
        """
        self.assertMarkdown(text, expect)

    def testInterchangedListType(self):
        text = """
        * item 1
        * item 2
        1. item 1
        2. item 2
        """
        expect = """
        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>

        <ol>
          <li>item 1</li>
          <li>item 2</li>
        </ol>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        1. item 1
        2. item 2
        * item 1
        * item 2
        """
        expect = """
        <ol>
          <li>item 1</li>
          <li>item 2</li>
        </ol>

        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        1. item 1
        * item 1
        2. item 2
        * item 2
        """
        expect = """
        <ol>
          <li>item 1</li>
        </ol>

        <ul>
          <li>item 1</li>
        </ul>

        <ol>
          <li>item 2</li>
        </ol>

        <ul>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testNestedInterchangedListType(self):
        text = """
        * item 1
            1. item 1
            2. item 2
        * item 2
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <ol>
            <li>item 1</li>
            <li>item 2</li>
          </ol></li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        * level 1
            1. level 2
                * level 3
                    2. level 4
        """
        expect = """
        <ul>
          <li><p>level 1</p>

          <ol>
            <li><p>level 2</p>

            <ul>
              <li><p>level 3</p>

              <ol>
                <li>level 4</li>
              </ol></li>
            </ul></li>
          </ol></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testLeadingEmphasis(self):
        text = """
        * *This is a* list
        """
        expect = """
        <ul>
          <li><em>This is a</em> list</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

        text = """
        * **This is** a * list
        """
        expect = """
        <ul>
          <li><strong>This is</strong> a * list</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testPrecedingParagraph(self):
        text = """
        Preceding Paragraph here
        * item 1
        * item 2
        """
        expect = """
        <p>Preceding Paragraph here</p>

        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testPrecedingCodeblock(self):
        text = """
        Stuff
            Code block
            here
        * item 1
        * item 2
        """
        expect = """
        <p>Stuff</p>

        <pre><code>Code block
        here</code></pre>

        <ul>
          <li>item 1</li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

class ListItemTest(TemplarTest):
    def testCodeblock(self):
        text = """
        * item 1
                Codeblock contents
        """
        expect = """
        <ul>
          <li><p>item 1</p>

        <pre><code>Codeblock contents</code></pre></li>
        </ul>
        """
        self.assertMarkdown(text, expect)

        text = """
        * item 1

                def hello(world):
                    return hi

        """
        expect = """
        <ul>
          <li><p>item 1</p>

        <pre><code>def hello(world):
            return hi</code></pre></li>
        </ul>
        """
        self.assertMarkdown(text, expect)

        text = """
        * item 1

                def hello(world):
                    return hi

        * item 2
        """
        expect = """
        <ul>
          <li><p>item 1</p>

        <pre><code>def hello(world):
            return hi</code></pre></li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testNotCodeblock(self):
        text = """
        * item 1

            def hello(world):
                return hi

        * item 2
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <p>def hello(world):
              return hi</p></li>
          <li>item 2</li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testBlockquote(self):
        text = """
        * item 1
            > blockquote in list
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <blockquote>
          <p>blockquote in list</p>
          </blockquote></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        * item 1

            > Multiline
            > blockquote
            with no wrap here

        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <blockquote>
          <p>Multiline
          blockquote
          with no wrap here</p></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

        text = """
        * item 1

            > Multiline
            > blockquote

            > with a
            > split in the middle

        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <blockquote>
          <p>Multiline
          blockquote</p>

          <p>with a
          split in the middle</p></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testCodeblockLooksLikeList(self):
        text = """
        * item 1
                * This is a codeblock
                  because it is indented
                * 8 spaces
        """
        expect = """
        <ul>
          <li><p>item 1</p>

        <pre><code>* this is a codeblock
          because it is indented
        * 8 spaces</code></pre></li>
        </ul>
        """
        self.assertMarkdown(text, expect)

        text = """
        * item 1
                1. This is a codeblock
                   because it is indented
                2. 8 spaces
        """
        expect = """
        <ul>
          <li><p>item 1</p>

        <pre><code>1. this is a codeblock
           because it is indented
        2. 8 spaces</code></pre></li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testCodeblockLooksLikeBlockquote(self):
        text = """
        * item 1
                > This is a codeblock
                > Because it is indented
                > 8 spaces
        """
        expect = """
        <ul>
          <li><p>item 1</p>

        <pre><code>&gt; This is a codeblock
        &gt; Because it is indented
        &gt; 8 spaces</code></pre></li>
        </ul>
        """
        self.assertMarkdown(text, expect)

    def testCodeblockInNestedList(self):
        text = """
        * item 1
            * item 1
                    This is a codeblock
            * item 2
                This is not a codeblock
        * item 2
                This is a codeblock
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <ul>
            <li><p>item 1</p>

        <pre><code>This is a codeblock</code></pre></li>
            <li>item 2
                This is not a codeblock</li>
          </ul></li>
          <li><p>item 2</p>

        <pre><code>This is a codeblock</code></pre></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testBlockquoteInNestedList(self):
        text = """
        * item 1
            * item 1
                > This is a blockquote
        """
        expect = """
        <ul>
          <li><p>item 1</p>

          <ul>
            <li><p>item 1</p>

            <blockquote>
            <p>This is a blockquote</p>
            </blockquote></li>
          </ul></li>
        </ul>
        """
        self.assertMarkdownIgnoreWS(text, expect)

if __name__ == '__main__':
    main()
