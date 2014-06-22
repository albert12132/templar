from utils import MarkdownTest, main

class LinkTest(MarkdownTest):
    def testBasic(self):
        text = "[link here](path/to/url)"
        expect = '<p><a href="path/to/url">link here</a></p>'
        self.assertMarkdown(text, expect)

        text = "[link here](http://domainname.com)"
        expect = '<p><a href="http://domainname.com">link here</a></p>'
        self.assertMarkdown(text, expect)

        text = "Inline [links](path/to/url) demo"
        expect = '<p>Inline <a href="path/to/url">links</a> demo</p>'
        self.assertMarkdown(text, expect)

    def testWhitespace(self):
        text = "[  link here   ](path/to/url)"
        expect = '<p><a href="path/to/url">link here</a></p>'
        self.assertMarkdown(text, expect)

        text = "[link here](   path/to/url   )"
        expect = '<p><a href="path/to/url">link here</a></p>'
        self.assertMarkdown(text, expect)

        text = "[link here](path/to/url    'stuff here')"
        expect = '<p><a href="path/to/url" title="stuff here">link here</a></p>'
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = """
        [link
        here](path/to/url)
        """
        expect = """
        <p><a href="path/to/url">link
        here</a></p>
        """
        self.assertMarkdown(text, expect)

    def testTitle(self):
        text = "[link here](path/to/url 'title here')"
        expect = '<p><a href="path/to/url" title="title here">link here</a></p>'
        self.assertMarkdown(text, expect)

        text = '[link here](path/to/url "title here")'
        expect = '<p><a href="path/to/url" title="title here">link here</a></p>'
        self.assertMarkdown(text, expect)

    def testConsecutive(self):
        text = """
        [link here](path/to/url)
        [another link here](path/to/url)
        """
        expect = """
        <p><a href="path/to/url">link here</a>
        <a href="path/to/url">another link here</a></p>
        """
        self.assertMarkdown(text, expect)

class ImageTest(MarkdownTest):
    def testBasic(self):
        text = "![link here](path/to/url)"
        expect = '<p><img src="path/to/url" alt="link here"></p>'
        self.assertMarkdown(text, expect)

        text = "![link here](http://domainname.com)"
        expect = '<p><img src="http://domainname.com" alt="link here"></p>'
        self.assertMarkdown(text, expect)

        text = "Inline ![image](path/to/url) demo"
        expect = '<p>Inline <img src="path/to/url" alt="image"> demo</p>'
        self.assertMarkdown(text, expect)

    def testWhitespace(self):
        text = "![  link here   ](path/to/url)"
        expect = '<p><img src="path/to/url" alt="  link here   "></p>'
        self.assertMarkdown(text, expect)

        text = "![link here](   path/to/url   )"
        expect = '<p><img src="path/to/url" alt="link here"></p>'
        self.assertMarkdown(text, expect)

        text = "![link here](path/to/url    'stuff here')"
        expect = '<p><img src="path/to/url" alt="link here" title="stuff here"></p>'
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = """
        ![link
        here](path/to/url)
        """
        expect = """
        <p><img src="path/to/url" alt="link
        here"></p>
        """
        self.assertMarkdown(text, expect)

    def testTitle(self):
        text = "![link here](path/to/url 'title here')"
        expect = '<p><img src="path/to/url" alt="link here" title="title here"></p>'
        self.assertMarkdown(text, expect)

        text = '![link here](path/to/url "title here")'
        expect = '<p><img src="path/to/url" alt="link here" title="title here"></p>'
        self.assertMarkdown(text, expect)

class ReferenceTest(MarkdownTest):
    def testRemoval(self):
        text = "[id]: path/to/resource"
        expect = ''
        self.assertMarkdown(text, expect)

    def testBasic(self):
        text = """
        A [link text][id] here

        [id]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        [id]: path/to/resource

        A [link text][id] here
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

    def testIdCaseInsensitive(self):
        text = """
        A [link text][Id] here

        [id]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        A [link text][id] here

        [ID]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

    def testIdWhitespace(self):
        text = """
        A [link text][id  whitespace is ok] here

        [id  whitespace is ok]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

    def testIdNumbers(self):
        text = """
        A [link text][id12] here

        [id12]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

    def testTitle(self):
        text = """
        A [link text][id] here

        [id]: path/to/resource "Optional title"
        """
        expect = """
        <p>A <a href="path/to/resource" title="Optional title">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

        text = """
        A [link text][id] here

        [id]: path/to/resource 'Optional title'
        """
        expect = """
        <p>A <a href="path/to/resource" title="Optional title">link text</a> here</p>
        """
        self.assertMarkdown(text, expect)

    def testIdImplicit(self):
        text = """
        A [id][] here

        [id]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">id</a> here</p>
        """
        self.assertMarkdown(text, expect)

    def testImage(self):
        text = """
        A ![link here][id] here

        [id]: path/to/resource
        """
        expect = """
        <p>A <img src="path/to/resource" alt="link here"> here</p>
        """
        self.assertMarkdown(text, expect)

    def testConsecutiveReferences(self):
        text = """
        A [link here][id] here, [second link][id1]

        [id]: path/to/resource
        [id1]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link here</a> here, <a href="path/to/resource">second link</a></p>
        """
        self.assertMarkdown(text, expect)

    def testConsecutiveLinks(self):
        text = """
        [link here][]
        [another link here](path/to/url)

        [link here]: another/path
        """
        expect = """
        <p><a href="another/path">link here</a>
        <a href="path/to/url">another link here</a></p>
        """
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = """
        [link
        here][]

        [link here]: path/to/url
        """
        expect = """
        <p><a href="path/to/url">link
        here</a></p>
        """
        self.assertMarkdown(text, expect)

        text = """
        [link here][ref
        id]

        [ref id]: path/to/url
        """
        expect = """
        <p><a href="path/to/url">link here</a></p>
        """
        self.assertMarkdown(text, expect)

class FootnoteTest(MarkdownTest):
    def testBasic(self):
        text = """
        Text here.[^id]

        [^id]: some text here
        """
        expect = """
        <p>Text here.<sup><a href="#fnref-1">1</a></sup></p>

        <div id="footnotes">
          <ol>
            <li id="fnref-1"><p>some text here</p></li>
          </ol>
        </div>
        """
        self.assertMarkdown(text, expect)

    def testMultipleReferences(self):
        text = """
        Text here.[^id]
        Another [^id] reference.

        [^id]: some text here
        """
        expect = """
        <p>Text here.<sup><a href="#fnref-1">1</a></sup>
        Another <sup><a href="#fnref-1">1</a></sup> reference.</p>

        <div id="footnotes">
          <ol>
            <li id="fnref-1"><p>some text here</p></li>
          </ol>
        </div>
        """
        self.assertMarkdown(text, expect)

    def testMultipleFootnotes(self):
        text = """
        Text here.[^id]
        Another [^blah] reference.

        [^id]: some text here
        [^blah]: some text here
        """
        expect = """
        <p>Text here.<sup><a href="#fnref-1">1</a></sup>
        Another <sup><a href="#fnref-2">2</a></sup> reference.</p>

        <div id="footnotes">
          <ol>
            <li id="fnref-1"><p>some text here</p></li>
            <li id="fnref-2"><p>some text here</p></li>
          </ol>
        </div>
        """
        self.assertMarkdown(text, expect)

    def testNoBackreference(self):
        text = """
        Text here.[^id]
        """
        expect = """
        <p>Text here.</p>
        """
        self.assertMarkdown(text, expect)

    def testList(self):
        text = """
        * Text here.[^id]

        [^id]: some text here
        """
        expect = """
        <ul>
          <li>Text here.<sup><a href="#fnref-1">1</a></sup></li>
        </ul>

        <div id="footnotes">
          <ol>
            <li id="fnref-1"><p>some text here</p></li>
          </ol>
        </div>
        """
        self.assertMarkdown(text, expect)

    def testBlockquote(self):
        text = """
        > Text here.[^id]

        [^id]: some text here
        """
        expect = """
        <blockquote><p>Text here.<sup><a href="#fnref-1">1</a></sup></p></blockquote>

        <div id="footnotes">
          <ol>
            <li id="fnref-1"><p>some text here</p></li>
          </ol>
        </div>
        """
        self.assertMarkdown(text, expect)


if __name__ == '__main__':
    main()
