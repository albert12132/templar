from utils import MarkdownTest, main

class BlockTagTest(MarkdownTest):
    def testDiv(self):
        text = """
        <div>
          This should be surrounded in div
        </div>
        """
        self.assertMarkdown(text, text)

    def testPreserve(self):
        text = """
        <div>
          *No* _emphasis_ `or code` should be **evaluated**
        </div>
        """
        self.assertMarkdown(text, text)

        text = """
        <div>
          Whitespace is      preserved too
        </div>
        """
        self.assertMarkdown(text, text)

        text = """
        <div>
          No <HTML> escapes &
        </div>
        """
        self.assertMarkdown(text, text)

    def testLeadingSpace(self):
        text = """
        Stuff
          <div>
          *Blah*
          </div>
        """
        expect = """
        <p>Stuff
          <div>
          <em>Blah</em>
          </div></p>
        """
        self.assertMarkdown(text, expect)

    def testPrecedingParagraph(self):
        text = """
        Stuff
        <div>
          Blah
        </div>
        """
        expect = """
        <p>Stuff</p>

        <div>
          Blah
        </div>
        """
        self.assertMarkdown(text, expect)

class TagTest(MarkdownTest):
    def testBasic(self):
        text = """
        This has a <span>here</span>
        """
        expect = """
        <p>This has a <span>here</span></p>
        """
        self.assertMarkdown(text, expect)

    def testPreserveAttributes(self):
        text = """
        This has a <span id="AT&T>here</span>
        """
        expect = """
        <p>This has a <span id="AT&T>here</span></p>
        """
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = """
        This has a <span
        id="AT&T>here</span>
        """
        expect = """
        <p>This has a <span
        id="AT&T>here</span></p>
        """
        self.assertMarkdown(text, expect)


if __name__ == '__main__':
    main()
