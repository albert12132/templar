from tests.test_utils import MarkdownTest, main

class TableTest(MarkdownTest):
    def testBasic(self):
        text = """
        header1 | header2 | header3
        --------|---------|--------
        content1|content2 |content3
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
            <th>header2</th>
            <th>header3</th>
          </tr>
          <tr>
            <td>content1</td>
            <td>content2</td>
            <td>content3</td>
          </tr>
        </table>
        """
        self.assertMarkdown(text, expect)

    def testMinimal(self):
        text = """
        header1|header2|header3
        -|-|-
        content1|content2|content3
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
            <th>header2</th>
            <th>header3</th>
          </tr>
          <tr>
            <td>content1</td>
            <td>content2</td>
            <td>content3</td>
          </tr>
        </table>
        """
        self.assertMarkdown(text, expect)

    def testSpan(self):
        text = """
        **header1**|*header2*|`header3`
        -|-|-
        _content1_|__content2__|***content3***
        """
        expect = """
        <table>
          <tr>
            <th><strong>header1</strong></th>
            <th><em>header2</em></th>
            <th><code>header3</code></th>
          </tr>
          <tr>
            <td><em>content1</em></td>
            <td><strong>content2</strong></td>
            <td><strong><em>content3</em></strong></td>
          </tr>
        </table>
        """
        self.assertMarkdown(text, expect)

    def testLink(self):
        text = """
        header1|header2|header3
        -|-|-
        [content1](link1)|![content2](image1)|[content3][id]

        [id]: link2
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
            <th>header2</th>
            <th>header3</th>
          </tr>
          <tr>
            <td><a href="link1">content1</a></td>
            <td><img src="image1" alt="content2"></td>
            <td><a href="link2">content3</a></td>
          </tr>
        </table>
        """
        self.assertMarkdown(text, expect)

    def testMismatchedColumns(self):
        text = """
        header1|header2|header3
        -|-|-
        content1|
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
            <th>header2</th>
            <th>header3</th>
          </tr>
          <tr>
            <td>content1</td>
          </tr>
        </table>
        """
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = """
        header1|
        -|
        content1|

        header2|
        -|
        content2|
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
          </tr>
          <tr>
            <td>content1</td>
          </tr>
        </table>

        <table>
          <tr>
            <th>header2</th>
          </tr>
          <tr>
            <td>content2</td>
          </tr>
        </table>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testMissingPipe(self):
        text = """
        header1|
        -|
        content1|
        content2
        content3|
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
          </tr>
          <tr>
            <td>content1</td>
          </tr>
        </table>

        <p>content2
        content3|</p>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testTextAlign(self):
        text = """
        header1|header2|header3|header4
        ------:|:------|:-----:|-------
        content1|content2|content3|content4
        """
        expect = """
        <table>
          <tr>
            <th>header1</th>
            <th>header2</th>
            <th>header3</th>
            <th>header4</th>
          </tr>
          <tr>
            <td align="right">content1</td>
            <td align="left">content2</td>
            <td align="center">content3</td>
            <td>content4</td>
          </tr>
        </table>
        """
        self.assertMarkdownIgnoreWS(text, expect)

    def testHtmlTable(self):
        text = """
        <table class="table">
          <tr>
            <th>header1</th>
            <th>header2</th>
          </tr>
          <tr>
            <td>content1</td>
            <td>content2</td>
          </tr>
        </table>
        """
        expect = text
        self.assertMarkdown(text, expect)



if __name__ == '__main__':
    main()
