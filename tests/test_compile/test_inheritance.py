from tests.test_utils import CompileTest, main

class InheritanceTest(CompileTest):
    def testBasic(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'topic',
        ]
        files = {
            'topic/templates/base.html': """
            Hello world!

            {% block contents %}
            """,
            template_path: """
            <% extends base.html %>

            <% block contents %>
            Stuff here
            <% block contents %>
            """,
        }
        expect = """
        Hello world!

        Stuff here
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testNoInheritance(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'topic',
        ]
        files = {
            template_path: """
            No inheritance here
            """,
        }
        expect = """
        No inheritance here
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testOmitOverride(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'topic',
        ]
        files = {
            'topic/templates/base.html': """
            Hello world!

            {% block contents %}

            {% block no inheritance %}
            """,
            template_path: """
            <% extends base.html %>

            <% block contents %>
            Stuff here
            <% block contents %>
            """,
        }
        expect = """
        Hello world!

        Stuff here
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testInheritanceHierarchy(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'topic',
        ]
        files = {
            'topic/templates/first.html': """
            Hello world!

            <title>{% block title %}</title>

            {% block contents %}
            """,
            'topic/templates/second.html': """
            <% extends first.html %>

            <% block title %>
            A title here
            <% block title %>
            """,
            template_path: """
            <% extends second.html %>

            <% block contents %>
            Stuff here
            <% block contents %>
            """,
        }
        expect = """
        Hello world!

        <title>A title here</title>

        Stuff here
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testNestedOverride(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'topic',
        ]
        files = {
            'topic/templates/first.html': """
            Hello world!

            {% block contents %}
            """,
            'topic/templates/second.html': """
            <% extends first.html %>

            <% block contents %>
            Some stuff here
            {% block stuff %}
            <% block contents %>
            """,
            template_path: """
            <% extends second.html %>

            <% block stuff %>
            More stuff
            <% block stuff %>
            """,
        }
        expect = """
        Hello world!

        Some stuff here
        More stuff
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testSameBlockMultipleTimes(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'topic',
        ]
        files = {
            'topic/templates/base.html': """
            <title>{% block title %}</title>

            <h1>{% block title %}</h1>
            """,
            template_path: """
            <% extends base.html %>

            <% block title %>
            A title here
            <% block title %>
            """,
        }
        expect = """
        <title>A title here</title>

        <h1>A title here</h1>
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testMultipleTemplateDirs(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'first',
            'topic',
        ]
        files = {
            'topic/templates/base.html': """
            Incorrect base

            {% block contents %}
            """,
            'first/templates/base.html': """
            Correct base

            {% block contents %}
            """,
            template_path: """
            <% extends base.html %>

            <% block contents %>
            A title here
            <% block contents %>
            """,
        }
        expect = """
        Correct base

        A title here
        """
        self.assertInheritance(template_path, template_dirs, expect, files)

    def testExplicitTemplateDir(self):
        template_path = 'topic/templates/index.html'
        template_dirs = [
            'first',
            'topic',
        ]
        files = {
            'topic/templates/base.html': """
            Correct base

            {% block contents %}
            """,
            'first/templates/base.html': """
            Incorrect base

            {% block contents %}
            """,
            template_path: """
            <% extends topic:base.html %>

            <% block contents %>
            A title here
            <% block contents %>
            """,
        }
        expect = """
        Correct base

        A title here
        """
        self.assertInheritance(template_path, template_dirs, expect, files)


if __name__ == '__main__':
    main()

