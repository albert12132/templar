from tests.test_utils import LinkTest, main
import re

class SubstitutionTest(LinkTest):
    def testSubstititonFunction(self):
        text = """
        <pattern>
        """
        subs = [
            (r"<pattern>", lambda m: 'Hello world!')
        ]
        expect = """
        Hello world!
        """
        self.assertSubstitution(text, expect, subs)

    def testSubstitionString(self):
        text = """
        <pattern>
        """
        subs = [
            (r"<pattern>", 'Hello world!')
        ]
        expect = """
        Hello world!
        """
        self.assertSubstitution(text, expect, subs)

    def testOrdering(self):
        text = """
        <pattern>
        """
        subs = [
            (r"<pattern>", 'Hello world!'),
            (r"<.+>", 'Bye!')
        ]
        expect = """
        Hello world!
        """
        self.assertSubstitution(text, expect, subs)

    def testCounter(self):
        text = """
        <question>
        <question>
        <question>
        """
        count = 0
        def sub(m):
            nonlocal count
            count += 1
            return '<h1>Question {}</h1>'.format(count)
        subs = [
            (r"<question>", sub),
        ]
        expect = """
        <h1>Question 1</h1>
        <h1>Question 2</h1>
        <h1>Question 3</h1>
        """
        self.assertSubstitution(text, expect, subs)

    def testConditions(self):
        text = """
        <solution>
        """
        def sub(m):
            return '<h1>Solution</h1>'
        def cond(args):
            return 'solution' in args.conditions
        subs = [
            (r"<solution>", sub, cond),
        ]
        expect = """
        <h1>Solution</h1>
        """
        self.assertSubstitution(text, expect, subs, args=['solution'])
        self.assertSubstitution(text, text, subs, args=[])

    def testMultipleConditions(self):
        text = """
        <solution>
        <explanation>
        """
        def sub_sol(m):
            return '<h1>Solution</h1>'
        def sub_expl(m):
            return '<h1>Explanation</h1>'
        def cond(args):
            return 'solution' in args.conditions
        subs = [
            (r"<solution>", sub_sol, cond),
            (r"<explanation>", sub_expl, lambda args: not cond(args)),
        ]
        expect = """
        <h1>Solution</h1>
        <explanation>
        """
        self.assertSubstitution(text, expect, subs, args=['solution'])

        expect = """
        <solution>
        <h1>Explanation</h1>
        """
        self.assertSubstitution(text, expect, subs, args=[])

class ScrapeHeadersTest(LinkTest):
    def testBasic(self):
        text = """
        + Header 1
        + Not a header
        + Header 2
        + Header 3
        """
        regex = r"\+ Header (\d+)"
        translate = lambda m: 'Title ' + m.group(1)
        expect = [
            'Title 1',
            'Title 2',
            'Title 3',
        ]
        self.assertHeaders(text, regex, translate, expect)

    def testNoHeaders(self):
        text = """
        No headers
        to be found!
        """
        regex = r"\+ Header (\d+)"
        translate = lambda m: 'Title ' + m.group(1)
        expect = []
        self.assertHeaders(text, regex, translate, expect)

    def testCounter(self):
        text = """
        + Header To be
        + Header Or not to be
        + Header That is the question
        """
        regex = r"\+ Header ([\w ]+)"
        count = 0
        def translate(m):
            nonlocal count
            count += 1
            return "Section {}: {}".format(count, m.group(1))
        expect = [
            'Section 1: To be',
            'Section 2: Or not to be',
            'Section 3: That is the question',
        ]
        self.assertHeaders(text, regex, translate, expect)


if __name__ == '__main__':
    main()

