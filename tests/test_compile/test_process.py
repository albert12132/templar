from tests.test_utils import CompileTest, main

class ExpressionTest(CompileTest):
    def testExpressionVariable(self):
        template = """
        The example is {{ example }}
        """
        attrs = {
            'example': 'stuff',
        }
        expect = """
        The example is stuff
        """
        self.assertProcess(template, attrs, expect)

    def testExpressionBlock(self):
        template = """
        The example is {{ :example }}
        """
        attrs = {
            ':example': 'stuff',
        }
        expect = """
        The example is stuff
        """
        self.assertProcess(template, attrs, expect)

    def testExpressionVariableWithSpaces(self):
        template = """
        The example is {{ an example }}
        """
        attrs = {
            'an example': 'stuff',
        }
        expect = """
        The example is stuff
        """
        self.assertProcess(template, attrs, expect)

    def testExpressionPython(self):
        template = r"""
        The example is {{ example.upper() }}
        {{ '\n'.join(lst) }}
        """
        attrs = {
            'example': 'stuff',
            'lst': ['one', 'two', 'three']
        }
        expect = """
        The example is STUFF
        one
        two
        three
        """
        self.assertProcess(template, attrs, expect)

    def testExpressionNewline(self):
        template = r"""
        The example is {{
        an example }}
        """
        attrs = {
            'an example': 'stuff',
        }
        expect = """
        The example is stuff
        """
        self.assertProcess(template, attrs, expect)

        template = r"""
        The example is {{ an
        example }}
        """
        attrs = {
            'an example': 'stuff',
        }
        expect = """
        The example is stuff
        """
        self.assertProcess(template, attrs, expect)

        template = r"""
        The example is {{ an example
        }}
        """
        attrs = {
            'an example': 'stuff',
        }
        expect = """
        The example is stuff
        """
        self.assertProcess(template, attrs, expect)

class ConditionalTest(CompileTest):
    def testNonemptyCondition(self):
        template = """
        Hello World!
        {% if {{ example }} %}
        This should appear
        {% endif %}
        """
        attrs = {
            'example': 'stuff',
        }
        expect = """
        Hello World!
        This should appear
        """
        self.assertProcess(template, attrs, expect)

    def testEmptyCondition(self):
        template = """
        Hello World!
        {% if {{ example }} %}
        This should not appear
        {% endif %}
        """
        attrs = {
            'example': '',
        }
        expect = """
        Hello World!
        """
        self.assertProcess(template, attrs, expect)

    def testNonexistentCondition(self):
        template = """
        Hello World!
        {% if {{ example }} %}
        This should not appear
        {% endif %}
        """
        attrs = {
        }
        expect = """
        Hello World!
        """
        self.assertProcess(template, attrs, expect)

    def testPythonExpressionCondition(self):
        template = r"""
        Hello World!
        {% if {{ 3 == 4 }} %}
        This should not appear
        {% endif %}
        """
        attrs = {
        }
        expect = """
        Hello World!
        """
        self.assertProcess(template, attrs, expect)

    def testElseClause(self):
        template = r"""
        Hello World!
        {% if {{ 3 == 4 }} %}
        This should not appear
        {% else %}
        This should appear
        {% endif %}
        """
        attrs = {
        }
        expect = """
        Hello World!
        This should appear
        """
        self.assertProcess(template, attrs, expect)

    def testElifClause(self):
        template = r"""
        Hello World!
        {% if {{ 3 == 4 }} %}
        This should not appear
        {% elif {{ 3 == 3 }} %}
        This should appear
        {% endif %}
        """
        attrs = {
        }
        expect = """
        Hello World!
        This should appear
        """
        self.assertProcess(template, attrs, expect)

    def testMultipleElifClauses(self):
        template = r"""
        Hello World!
        {% if {{ 3 == 4 }} %}
        This should not appear
        {% elif {{ foo }} %}
        This should not appear
        {% elif {{ bar bear }} %}
        <h1>This should appear</h1>
        {% endif %}
        """
        attrs = {
            'bar bear': 'something',
        }
        expect = """
        Hello World!
        <h1>This should appear</h1>
        """
        self.assertProcess(template, attrs, expect)

    def testExpressionInConditionalClause(self):
        template = r"""
        Hello World!
        {% if {{ variable }} %}
        This {{ variable }}
        {% endif %}
        """
        attrs = {
            'variable': 'something',
        }
        expect = """
        Hello World!
        This something
        """
        self.assertProcess(template, attrs, expect)

class ForLoopTest(CompileTest):
    def testIterableVariable(self):
        template = """
        Hello World!
        {% for {{ elem }} in {{ lst }} %}
        <h1>{{ elem }}</h1>
        {% endfor %}
        """
        attrs = {
            'lst': ['one', 'two', 'three'],
        }
        expect = """
        Hello World!
        <h1>one</h1>
        <h1>two</h1>
        <h1>three</h1>
        """
        self.assertProcess(template, attrs, expect)

    def testIterableMultipleVariable(self):
        template = """
        Hello World!
        {% for {{ var1 }}, {{ var2 }}, {{ var3 }} in {{ lst }} %}
        <h1>{{ var1 }}, {{ var2 }}, {{ var3 }}</h1>
        {% endfor %}
        """
        attrs = {
            'lst': [
                ('a', 'b', 'c'),        # exactly enough
                ('e', 'f'),             # one value missing
                ('g', 'h', 'i', 'j'),   # extra value
            ],
        }
        expect = """
        Hello World!
        <h1>a, b, c</h1>
        <h1>e, f, </h1>
        <h1>g, h, i</h1>
        """
        self.assertProcess(template, attrs, expect)

    def testIterablePython(self):
        template = """
        Hello World!
        {% for {{ var }} in {{ range(3) }} %}
        <h1>Section {{ var + 1 }}</h1>
        {% endfor %}
        """
        attrs = {
        }
        expect = """
        Hello World!
        <h1>Section 1</h1>
        <h1>Section 2</h1>
        <h1>Section 3</h1>
        """
        self.assertProcess(template, attrs, expect)

    def testGlobalVariable(self):
        template = """
        Hello World!
        {% for {{ var }} in {{ range(3) }} %}
        <h1>Section {{ var }}:</h1>

        {{ topic }}
        {% endfor %}
        """
        attrs = {
            'topic': 'Test',
        }
        expect = """
        Hello World!
        <h1>Section 0:</h1>

        Test
        <h1>Section 1:</h1>

        Test
        <h1>Section 2:</h1>

        Test
        """
        self.assertProcess(template, attrs, expect)

class MacroTest(CompileTest):
    def testBasic(self):
        template = """
        Hello World!
        {% def hello {{ boo }}, {{ here }} %}
        {{ boo }} is {{ here }}
        {% enddef %}

        {% call hello {{ 1 + 3 }}, {{ var1 }} %}
        """
        attrs = {
            'var1': 'hello'
        }
        expect = """
        Hello World!


        4 is hello
        """
        self.assertProcess(template, attrs, expect)

    def testMacroDefinedAfterCall(self):
        template = """
        Hello World!

        {% call hello {{ 1 + 3 }}, {{ var1 }} %}

        {% def hello {{ boo }}, {{ here }} %}
        {{ boo }} is {{ here }}
        {% enddef %}

        """
        attrs = {
            'var1': 'hello'
        }
        expect = """
        Hello World!

        4 is hello
        """
        self.assertProcess(template, attrs, expect)

    def testMacroExtraArguments(self):
        template = """
        Hello World!

        {% call hello {{ 1 + 3 }}, {{ var1 }}, {{ extra }} %}

        {% def hello {{ boo }}, {{ here }} %}
        {{ boo }} is {{ here }}
        {% enddef %}

        """
        attrs = {
            'var1': 'hello',
            'extra': 'boo!',
        }
        expect = """
        Hello World!

        4 is hello
        """
        self.assertProcess(template, attrs, expect)

    def testMacroUnmatchedVariables(self):
        template = """
        Hello World!

        {% call hello {{ 1 + 3 }} %}

        {% def hello {{ boo }}, {{ here }} %}
        {{ boo }} is {{ here }}
        {% enddef %}

        """
        attrs = {
        }
        expect = """
        Hello World!

        4 is
        """
        self.assertProcess(template, attrs, expect)

    def testUndefinedMacro(self):
        template = """
        Hello World!

        {% call hello {{ 1 + 3 }} %}
        """
        attrs = {
        }
        expect = """
        Hello World!

        """
        self.assertProcess(template, attrs, expect)

    def testOneMacroMultipleCalls(self):
        template = """
        Hello World!

        {% call hello {{ 1 + 3 }} %}

        {% call hello {{ 1 + 3 }} %}

        {% def hello {{ boo }} %}
        The number {{ boo }}
        {% enddef %}
        """
        attrs = {
        }
        expect = """
        Hello World!

        The number 4

        The number 4
        """
        self.assertProcess(template, attrs, expect)

class IntegrationTest(CompileTest):
    def testForConditional(self):
        template = """
        {% for {{ var }} in {{ range(4) }} %}
        {% if {{ var % 2 == 0 }} %}
        Even
        {% else %}
        Odd
        {% endif %}
        {% endfor %}
        """
        attrs = {
            'topic': 'Test',
        }
        expect = """
        Even
        Odd
        Even
        Odd
        """
        self.assertProcess(template, attrs, expect)

    def testConditionalFor(self):
        template = """
        {% if {{ 'sol' in topic }} %}
        Loop
        {% for {{ var }} in {{ topic }} %}
        {{ var }}
        {% endfor %}
        {% else %}
        Nothing
        {% endif %}
        """
        attrs = {
            'topic': ['sol', 'stuff', 'here'],
        }
        expect = """
        Loop
        sol
        stuff
        here
        """
        self.assertProcess(template, attrs, expect)

    def testForFor(self):
        template = """
        {% for {{ var1 }} in {{ range(3) }} %}
        {% for {{ var2 }} in {{ range(3) }} %}
        {{ var1 }}, {{ var 2 }}
        {% endfor %}
        {% endfor %}
        """
        attrs = {
        }
        expect = """
        0, 0
        0, 1
        0, 2
        1, 0
        1, 1
        1, 2
        2, 0
        2, 1
        2, 2
        """
        self.assertProcess(template, attrs, expect)

    def testConditionalConditional(self):
        template = """
        {% if {{ 3 == 3 }} %}
        {% if {{ 3 == 4 }} %}
        One
        {% else %}
        Two
        {% endif %}
        {% else %}
        Three
        {% endif %}
        """
        attrs = {
        }
        expect = """
        Two
        """
        self.assertProcess(template, attrs, expect)


if __name__ == '__main__':
    main()

