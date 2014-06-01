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

    python3 templar example.html -s src/hello_world.md

This will print the compiled result to standard out. To save the result
in a file, specify a destination with the `-d` flag:

    python3 templar example.html -s src/hello_world.md -d hello_world.html

This will save the result in a file called `hello_world.html` in the
`base_path` directory.

For a more extensive example of how to use Templar, see the repository
for my [personal website](https://github.com/albert12132/albertwu.org).
It is often helpful to use a Makefile instead of directly running
Templar every time.

Source files
------------

Currently, Templar only supports Markdown as its content markup
language. A basic source file can simply contain regular Markdown.
There are also two special tags that can be used: the `<block>` tag and
the `<include>` tag.

### `block` tag

The `<block>` tag allows you to name a certain section of Markdown:

    Some Markdown out here

    <block example>
    Example
    -------
    This Markdown is within the block.
    </block example>

The opening `block` tag consists of triangular braces, `< >`, the word
`block`, followed by a space, and then the name of the block. In the
example above, the name of the block is `example`.

The closing `block` tag uses a forward slash and also needs to contain
the name of the block that it closes. This allows you to nest blocks
inside of each other:

    <block outer>

    <block inner>
    This stuff here would be included in both the inner block and the
    outer block
    </block inner>

    But this stuff would only be included in the outer block.
    </block outer>

Block names must be unique within a single file.

### `include` tag

The `<include>` tag allows you to link different Markdown sources
together:

    Topics
    ------
    <include path/to/topics>

    References
    ----------
    <include path/to/references:blockA>

The idea is that sometimes, it is useful to write modular Markdown
sources to make it easier to manage directories. This also makes it
faster to refer to the same Markdown file without duplicating its
contents.

In the example above, the first `include` tag simply uses a filepath.
The filepath should be written *relative to the directory in which you
will run Templar*, not necessarily the directory that houses the
Markdown file. This format will simply copy all of the contents listed
inside of `path/to/topics.md` (notice that the `.md` extension was
omitted in the `include`) into the location of the `include` tag.

The second `include` tag also references a `blockA` inside of the file
`path/to/references.md`. This is useful if you only want to include a
subsection of another Markdown file. The syntax is the following:

    <include path/to/file:block-name>

### Custom patterns

You can define custom patterns in your Markdown, like the following:

    Question 1
    ----------

    A question here.

    <solution>

    This is the solution to the question: `f = lambda x: f(x)`.

    </solution>

You can specify how to convert the `<solution>...</solution>` pattern
by defining a regular expression in `controller.py`, which should be
located *in the directory where you run Templar*. For example,

    solution_re = re.compile(r"<solution>(.*?)</solution>", re.S)
    def solution_sub(match):
        return "<b>Solution</b>: " + match.group(1)

    regexes = [
        (solution_re, solution_sub),
    ]

would replace the `solution` tag with a boldface "Solution: " followed
by the contents within the solution tag. All regular expressions should
be listed inside of the `regexes` list (in `controller.py`), along with
the corresponding substitution function.

**Important note**: the custom patterns are evaluated **after** all
linking (`include` tags) and all Markdown parsing has occurred. Thus,
in the example above, `solution_re` should expect the contents of the
solution tag to look like this:

    <p>this is the solution to the question: <code>f = lambda x:
    f(x)</code>.</p>


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

Acknowledgements
----------------

Templar is an extension of the program that used to generate my
personal website. The idea for linking (the `include` and `block` tags)
was taken from developing the publisher for UC Berkeley's CS 61A labs.

The Markdown parser is a re-implementation of
[markdown2](https://github.com/trentm/python-markdown2), a Python
implementation of the original Perl Markdown parser. The variant of
Markdown that Templar supports is a subset of [Daring Fireball's
Markdown
specification](http://daringfireball.net/projects/markdown/syntax).

Syntax for template inheritance and expression substitution are
inspired by [Django](https://www.djangoproject.com/)'s templating
syntax, as well as [ejs](http://embeddedjs.com/)'s templating syntax.
