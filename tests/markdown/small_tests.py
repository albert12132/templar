from utils import TemplarTest

class SetextHeaderTest(TemplarTest):
    def h1Test(self):
        simple = "Hello World!"
        simple += '\n' + '-' * len(simple)
        expect = '<h1 id="hello-world">Hello World!</h1>'
        self.assertEqual(expect, simple)

