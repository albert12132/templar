from tests.markdown_test.test_utils import MarkdownTest

class EmTest(MarkdownTest):
    def testBasic(self):
        text = "*This is an em*"
        expect = "<p><em>This is an em</em></p>"
        self.assertMarkdown(text, expect)

        text = "_This is an em_"
        expect = "<p><em>This is an em</em></p>"
        self.assertMarkdown(text, expect)

    def testWhitespace(self):
        text = "This is * not an em *"
        expect = "<p>This is * not an em *</p>"
        self.assertMarkdown(text, expect)

        text = "This is _ not an em _"
        expect = "<p>This is _ not an em _</p>"
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = "This *is an\nem* here"
        expect = "<p>This <em>is an\nem</em> here</p>"
        self.assertMarkdown(text, expect)

    def testMixedDelimiter(self):
        text = "This *is not an em_ here"
        expect = "<p>This *is not an em_ here</p>"
        self.assertMarkdown(text, expect)

    def testUnderscoreInAsterisk(self):
        text = "This *is an em_ here*"
        expect = "<p>This <em>is an em_ here</em></p>"
        self.assertMarkdown(text, expect)

class StrongTest(MarkdownTest):
    def testBasic(self):
        text = "**This is a strong**"
        expect = "<p><strong>This is a strong</strong></p>"
        self.assertMarkdown(text, expect)

        text = "__This is a strong__"
        expect = "<p><strong>This is a strong</strong></p>"
        self.assertMarkdown(text, expect)

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
        self.assertMarkdown(text, expect)

    # TODO Original Markdown does not specify the following behavior
    # def testMixedDelimiter(self):
    #     text = "This **is not a strong__ here"
    #     expect = "<p>This **is not a strong__ here</p>"
    #     self.assertEqual(expect, convert(text))

    def testUnderscoreInAsterisk(self):
        text = "This **is a strong__ here**"
        expect = "<p>This <strong>is a strong__ here</strong></p>"
        self.assertMarkdown(text, expect)

    def testAsteriskInStrong(self):
        text = "This **is a strong* here**"
        expect = "<p>This <strong>is a strong* here</strong></p>"
        self.assertMarkdown(text, expect)

class StrongEmTest(MarkdownTest):
    def testBasic(self):
        text = "***This is a strong em***"
        expect = "<p><strong><em>This is a strong em</em></strong></p>"
        self.assertMarkdown(text, expect)

        text = "___This is a strong em___"
        expect = "<p><strong><em>This is a strong em</em></strong></p>"
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = "This ***is a\nstrong*** here"
        expect = "<p>This <strong><em>is a\nstrong</em></strong> here</p>"
        self.assertMarkdown(text, expect)

    def testUnderscoreInAsterisk(self):
        text = "This ***is a strong___ here***"
        expect = "<p>This <strong><em>is a strong___ here</em></strong></p>"
        self.assertMarkdown(text, expect)

    def testAsteriskInStrongEm(self):
        text = "This ***is a strong em* here***"
        expect = "<p>This <strong><em>is a strong em* here</em></strong></p>"
        self.assertMarkdown(text, expect)

class CodeTest(MarkdownTest):
    def testBasic(self):
        text = "This is a `code tag`"
        expect = "<p>This is a <code>code tag</code></p>"
        self.assertMarkdown(text, expect)

    def testNewline(self):
        text = "This `is a\ncode tag` here"
        expect = "<p>This <code>is a\ncode tag</code> here</p>"
        self.assertMarkdown(text, expect)

    def testPreserveAsterisks(self):
        text = "This `should *not* be` emphasized"
        expect = "<p>This <code>should *not* be</code> emphasized</p>"
        self.assertMarkdown(text, expect)

        text = "This `should **not** be` emphasized"
        expect = "<p>This <code>should **not** be</code> emphasized</p>"
        self.assertMarkdown(text, expect)

        text = "This `should *not be` emphasized `*here`"
        expect = "<p>This <code>should *not be</code> emphasized <code>*here</code></p>"
        self.assertMarkdown(text, expect)

    def testEscape(self):
        text = "`AT&T`"
        expect = "<p><code>AT&amp;T</code></p>"
        self.assertMarkdown(text, expect)

        text = "`<example>`"
        expect = "<p><code>&lt;example&gt;</code></p>"
        self.assertMarkdown(text, expect)

        text = '`"double quote"`'
        expect = "<p><code>&quot;double quote&quot;</code></p>"
        self.assertMarkdown(text, expect)

    def testMultipleTicks(self):
        text = "``Two ticks``"
        expect = "<p><code>Two ticks</code></p>"
        self.assertMarkdown(text, expect)

        text = "````Four ticks````"
        expect = "<p><code>Four ticks</code></p>"
        self.assertMarkdown(text, expect)

    def testWhitespace(self):
        text = "` Example text `"
        expect = "<p><code>Example text</code></p>"
        self.assertMarkdown(text, expect)


    def testInternalTicks(self):
        text = "``Two ` surrounding``"
        expect = "<p><code>Two ` surrounding</code></p>"
        self.assertMarkdown(text, expect)

        text = "`` ` ``"
        expect = "<p><code>`</code></p>"
        self.assertMarkdown(text, expect)

        text = "```` ``` ````"
        expect = "<p><code>```</code></p>"
        self.assertMarkdown(text, expect)
