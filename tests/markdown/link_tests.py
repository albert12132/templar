from utils import TemplarTest, main

class LinkTest(TemplarTest):
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
        expect = '<p><a href="path/to/url">  link here   </a></p>'
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

class ImageTest(TemplarTest):
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

class ReferenceTest(TemplarTest):
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
        A [link text][id12] here, and [second link][id23] here

        [id12]: path/to/resource
        [id23]: path/to/resource
        """
        expect = """
        <p>A <a href="path/to/resource">link text</a> here, and <a href="path/to/resource">second link</a> here</p>
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



if __name__ == '__main__':
    main()
