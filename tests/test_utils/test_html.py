import re
from tests.test_utils import LinkTest, main
import templar.utils.html as html

class EscapeTest(LinkTest):
    def testHexUnescape(self):
        text = "&#x27;&#x68;&#x65;&#x6c;&#x6c;&#x6f;&#x20;&#x77;&#x6f;&#x72;&#x6c;&#x64;&#x27;&#x21;&#x20;&#x54;&#x68;&#x69;&#x73;&#x20;&#x69;&#x73;&#x20;&#x61;&#x20;&#x22;&#x74;&#x65;&#x73;&#x74;&#x22;&#x2e;"
        expect = """'hello world'! This is a "test"."""
        self.assertEqual(html.unescape(text), expect)

    def testDecimalUnescape(self):
        text = ''.join('&#{};'.format(ord(c))
                       for c in """'hello world'! This is a "test".""")
        expect = """'hello world'! This is a "test"."""
        self.assertEqual(html.unescape(text), expect)

    def testHexEscape(self):
        text = """
        'hello world'! This is a "test".
        """
        self.assertEqual(html.unescape(html.hex_escape(text)), text)

    def testDecimalEscape(self):
        text = """
        'hello world'! This is a "test".
        """
        self.assertEqual(html.unescape(html.decimal_escape(text)), text)

class HeaderTest(LinkTest):
    def testBasic(self):
        text = """
        <h1 id="header1">Title</h1>
        <h2 id='header2'>Second header</h2>
        <h1 class="stuff" id='header3'>Boom!</h1>
        """
        expect = """
        <ul>
          <li><a href="#header1">Title</a></li>
          <li><a href="#header2">Second header</a></li>
          <li><a href="#header3">Boom!</a></li>
        </ul>
        """
        self.assertEqual(self.ignoreWhitespace(
                             html.HeaderParser(text).result),
                         expect)

    def testBasic(self):
        text = """
        <h1 id="header1">Title</h1>
        <h2 id='header2'>Second header</h2>
        <h1 class="stuff" id='header3'>Boom!</h1>
        """
        expect = """
        <ul>
          <li><a href="#header1">Title</a></li>
          <ul>
            <li><a href="#header2">Second header</a></li>
          </ul>
          <li><a href="#header3">Boom!</a></li>
        </ul>
        """
        self.assertEqual(self.ignoreWhitespace(
                             html.HeaderParser(text).result),
                         self.ignoreWhitespace(expect))


if __name__ == '__main__':
    main()

