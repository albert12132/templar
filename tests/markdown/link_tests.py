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

if __name__ == '__main__':
    main()
