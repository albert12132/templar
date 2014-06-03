from utils import TemplarTest, main
from markdown import convert, Markdown

class SetextHeaderTest(TemplarTest):
    def test_h1(self):
        simple = "Hello World!"
        simple += '\n' + '=' * len(simple)
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, convert(simple))

if __name__ == '__main__':
    main()
