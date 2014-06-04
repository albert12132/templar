from utils import TemplarTest, main
from markdown import convert, Markdown

class EmTest(TemplarTest):
    def setUp(self):
        super().setUp()

    def testBasic(self):
        text = "*This is an em*"
        expect = "<p><em>This is an em</em></p>"
        self.assertEqual(expect, convert(text))

        text = "_This is an em_"
        expect = "<p><em>This is an em</em></p>"
        self.assertEqual(expect, convert(text))

    def testWhitespace(self):
        text = "This is * not an em *"
        expect = "<p>This is * not an em *</p>"
        self.assertEqual(expect, convert(text))

        text = "This is _ not an em _"
        expect = "<p>This is _ not an em _</p>"
        self.assertEqual(expect, convert(text))

    def testNewline(self):
        text = "This *is an\nem* here"
        expect = "<p>This <em>is an\nem</em> here</p>"
        self.assertEqual(expect, convert(text))

    def testMixedDelimiter(self):
        text = "This *is not an em_ here"
        expect = "<p>This *is not an em_ here</p>"
        self.assertEqual(expect, convert(text))

    def testUnderscoreInAsterisk(self):
        text = "This *is an em_ here*"
        expect = "<p>This <em>is an em_ here</em></p>"
        self.assertEqual(expect, convert(text))

class StrongTest(TemplarTest):
    def setUp(self):
        super().setUp()

    def testBasic(self):
        text = "**This is a strong**"
        expect = "<p><strong>This is a strong</strong></p>"
        self.assertEqual(expect, convert(text))

        text = "__This is a strong__"
        expect = "<p><strong>This is a strong</strong></p>"
        self.assertEqual(expect, convert(text))

    # TODO Original Markdown does not specify the following behavior
    # def testWhitespace(self):
    #     text = "This is ** not a strong **"
    #     expect = "<p>This is ** not a strong **</p>"
    #     self.assertEqual(expect, convert(text))

    #     text = "This is __ not a strong __"
    #     expect = "<p>This is __ not a strong __</p>"
    #     self.assertEqual(expect, convert(text))

    def testNewline(self):
        text = "This **is a\nstrong** here"
        expect = "<p>This <strong>is a\nstrong</strong> here</p>"
        self.assertEqual(expect, convert(text))

    # TODO Original Markdown does not specify the following behavior
    # def testMixedDelimiter(self):
    #     text = "This **is not a strong__ here"
    #     expect = "<p>This **is not a strong__ here</p>"
    #     self.assertEqual(expect, convert(text))

    def testUnderscoreInAsterisk(self):
        text = "This **is a strong__ here**"
        expect = "<p>This <strong>is a strong__ here</strong></p>"
        self.assertEqual(expect, convert(text))

    def testAsteriskInStrong(self):
        text = "This **is a strong* here**"
        expect = "<p>This <strong>is a strong* here</strong></p>"
        self.assertEqual(expect, convert(text))

class StrongEmTest(TemplarTest):
    def setUp(self):
        super().setUp()

    def testBasic(self):
        text = "***This is a strong em***"
        expect = "<p><strong><em>This is a strong em</em></strong></p>"
        self.assertEqual(expect, convert(text))

        text = "___This is a strong___"
        expect = "<p><strong><em>This is a strong em</em></strong></p>"
        self.assertEqual(expect, convert(text))

    def testNewline(self):
        text = "This ***is a\nstrong*** here"
        expect = "<p>This <strong><em>is a\nstrong</em></strong> here</p>"
        self.assertEqual(expect, convert(text))

    def testUnderscoreInAsterisk(self):
        text = "This ***is a strong___ here***"
        expect = "<p>This <strong><em>is a strong___ here</em></strong></p>"
        self.assertEqual(expect, convert(text))

    def testAsteriskInStrongEm(self):
        text = "This ***is a strong em* here***"
        expect = "<p>This <strong><em>is a strong em* here</em></strong></p>"
        self.assertEqual(expect, convert(text))

if __name__ == '__main__':
    main()
