Templar
=======

Templar is a static templating engine that is designed to be
lightweight and flexible. Templar supports template inheritance and
modular source files, as well as the ability to define custom Markdown
patterns.

Basic Usage
-----------

To begin, clone this repo into your working directory or add it as a
git submodule. In the directory directly above Templar, create a Python
file called `config.py` with the following contents:

    import os

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    TEMPLATE_DIRS = [
        BASE_PATH,
        # list of directories that contain a templates directory
    ]

    CONFIGS = {
        # variables used by templates
    }

Each directory listed in `TEMPLATE_DIRS` should contain a directory
called `templates`, each of which houses template files (usually HTML).
The `CONFIGS` variable is a dictionary that maps strings to values --
these strings can be included in templates, and the templating engine
will resolve them when compiling.

**Note**: The `BASE_PATH` variable is not required, though it might be
helpful as a reference point for other directories that contain
templates. For example, if also have some templates in a directory
called `example`, we might add the following to `TEMPLATE_DIRS`:

    TEMPLATE_DIRS = [
        BASE_PATH,
        os.path.join(BASE_PATH, 'example'),
    ]

You can now create a directory called `templates` anywhere you want, as
long as its parent directory is listed in `TEMPLATE_DIRS`. The Markdown
source files (the *content*) can be located anywhere. For example,
let's say our working directory looks like this:

    base_path/
        templar/
        config.py
        templates/
            example.html
        src/
            hello_world.md

To compile `hello_world.md` using the `example.html` template, use the
following command:

    python3 templar/compile.py example.html -s src/hello_world.md

This will print the compiled result to standard out. To save the result
in a file, specify a destination with the `-d` flag:

    python3 templar/compile.py example.html -s src/hello_world.md -d hello_world.html

This will save the result in a file called `hello_world.html` in the
`base_path` directory.

For a more extensive example of how to use Templar, see the repository
for my [personal website](https://github.com/albert12132/albertwu.org).

Templates
---------

Templates are stored in a directory called `templates`, which can be
located anywhere as long as the parent directory is listed in the
`TEMPLATE_DIRS` variable in `config.py`. The most basic "template" is
simply a regular HTML file. In addition, you can add *expressions* in
the templates that the compiler will resolve. For example, the
following template can be used to fill in contact information:

    <ul>
      <li>Name: {{ name }}</li>
      <li>Age: {{ age }}</li>
      <li>Occupation: {{ job }}</li>
    </ul>

Expressions are denoted by two sets of curly braces, such as `{{ name
}}` or `{{ age }}`. The expression within the curly braces can be one
of the following:

* A variable defined within a Markdown source file. These "variable"
  names are more flexible than Python variable names, as they can
  include spaces and hyphens (the only restriction is they cannot
  contain newlines or colons).
* A variable defined within the `CONFIGS` variable of `config.py`.
  Again, these "variable" names can contain any characters besides
  newlines or colons.
* A block defined within a Markdown source file. For example, suppose a
  source file has the following block:

        <block example>

        Some Markdown here.

        </block example>

    The block `example` can then be used in an expression like so:

        <body>
        <p>Some HTML here</p>

        {{ :example }}

    Notice the colon that precedes the block name.
* A Python expression that can be evaluated. For example,

        <p>Date published: {{ datetime.now() }}</p>

    The `__str__` of the final value will be used in place of the
    expression. 

### Template Inheritance

Templar also supports template inheritance. A "child" template can
specify which "parent" template to inherit by including the following
on the *very first line of the child template*:

    <% extends parent.html %>

In the "parent" template, you can define labels that "child" templates
can fill:

    <!-- parent.html -->
    <div id='nav-bar'>
      <h3>Title</h3>

      {% nav-bar %}
    </div>

The `{% nav-bar %}` tag allows child templates to do the following:

    <!-- child.html -->
    <% extends parent.html %>

    <% nav-bar %>
    <h3>Some other stuff</h3>
    <h3>Some more stuff</h3>
    <%/ nav-bar %>

The result of compiling `child.html` will look like this:

    <div id='nav-bar'>
      <h3>Title</h3>

      <h3>Some other stuff</h3>
      <h3>Some more stuff</h3>
    </div>

If a child template choose not to inherit a tag, that tag will simply
be removed from the final document.

Source files
------------

Currently, Templar only supports Markdown as its content markup
language. A basic source file can simply contain regular Markdown.
There are also two special tags that can be used: the `<include>` tag
and the `<block>` tag.

### The `include` tag

The `<include>` tag allows you to 

