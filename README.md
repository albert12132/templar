Templar
=======

Templar is a static templating engine written in Python that is
designed to be lightweight and flexible. Templar supports template
inheritance and modular source files, as well as the ability to define
custom Markdown patterns.

Setup
-----

### Installation

To begin, clone this repo into your working directory (this README
assumes Templar will be installed in `<project>/lib/`):

    cd path/to/project
    git clone https://github.com/albert12132/templar.git lib/templar

Alternatively, add this repo as a git submodule:

    cd path/to/project
    git submodule add https://github.com/albert12132/templar.git lib/templar

### config.py

Choose a directory in which you will be publishing work using Templar
(this can be any directory in your project structure). For example,
suppose we want to publish in a directory called `<project>/blog/src/`.

Create a `config.py` file with the following command:

    python3 templar config blog/src

This will create a file called `config.py` in `<project>/blog/src/`
with the following (paraphrased) contents:

    FILEPATH = ...  # filepath of config.py

    TEMPLATE_DIRS = [
        FILEPATH,
        # list of directories that contain a templates directory
    ]

    VARIABLES = {
        # variables used by templates
    }

    SUBSTITUTIONS = [
        # (regex, sub) pairs
    ]

This basic setup is enough to start using Templar, but you can
customize each of the variables found in `config.py`. `TEMPLATE_DIRS`
is explained next; other customizations are described later.

### `TEMPLATE_DIRS`

Suppose we change `TEMPLATE_DIRS` to the following:

    TEMPLATE_DIRS = [
        FILEPATH,
        os.path.join(FILEPATH, 'example'),
    ]

Continuing from our previous example, `FILEPATH` is
`<project>/blog/src` (since that is where `config.py` is located).
Templar will now look in two directories to find templates:

1. `<project>/blog/src/templates/`
2. `<project>/blog/src/example/templates/`

Templates will be searched in that order.

Notice that each filepath in `TEMPLATE_DIRS` is assumed to have a
`templates` directory -- this is where template files should be placed.

**Note**: The `FILEPATH` variable is not required, though it is
helpful as a reference point for other directories that contain
templates.

Usage
-----

### Basic Templating

Continuing from our example above, suppose we are publishing content
from the filepath `<project>/blog/src`.

First, create a content file anywhere -- for example, we'll create a
Markdown file called `example.md`:

    ~ title: This is a Templar example

    This Markdown file is a *Templar example*.

This file contains standard Markdown, except for the first line `~
title: ...`. This is a *variable* declaration, which have the following
syntax:

    ~ variable name: variable value

Variables can be referenced from within templates (explained later) are
are useful for storing metadata about the content. Some things to note:

* `variable name` can contain any character that is not a newline and
  not a colon (`:`). This means variables can include spaces, hyphens,
  and underscores.
* `variable value` can contain any character that is not a newline.
  This means values can include spaces, hyphens, underscores, and
  colons (the first colon in the line is used as the separator)
* `variable value` will be taken *as is* (meaning it will not be parsed
  for Markdown)
* The variable declaration must be on one line

Once we are done with the content file, let's create a directory called
`templates`:

    mkdir templates

Add a sample template file called `template.html` to the `templates`
directory:

    <html>
      <head>
        <title>{{ title }}</title>
      </head>
      <body>
        <h1>{{ title }}</title>
        <p>Published: <i>{{ datetime.now() }}</i></p>

        {{ :all }}
      </body>
    </html>

This template demonstrates three fundamental features:

* **Variables** (`{{ title }}`): variables can be defined in either the
  content file (as seen above in `example.md`) or in `config.py`
  (explained later). Variables can be reused (e.g. multiple references
  to `title`).
* **Python expressions** (`{{ datetime.now() }}`): any valid Python
  *expression* can be used -- the `str` of the final value will be used
  in place of the `{{ ... }}`. For example, `datetime.now()` will
  evaluate to the current time (`datetime` is imported automatically by
  Templar)

* **Blocks** (`{{ :all }}`): a **block** is a section of the content
  file (see the section on Blocks below). All block expressions in
  templates start with a colon (`:`).

  Templar reserves the special block name `:all` to mean the entire
  content file. In this case, we are replacing `{{ :all }}` with all of
  the contents of our file.

To publish the content, use the following command:

    python3 ../../lib/templar compile template.html -s example.md -m -d result.html

* `../../lib/templar` is used because we are currently in
  `<project>/blog/src`
* `compile` tells Templar to compile a template
* `template.html` is the template that we are using
* `-s example.md` specifies the source content. This option is optional
  (Templar allows templating without use of a source file; this is
  useful if you still want to take advantage of Templar's template
  inheritance)
* `-m` tells Templar to convert the contents of `example.md` from
  Markdown into HTML before templating occurs
* `-d result.html` tells Templar to write the result to a file called
  `result.html`. This option is optional -- if omitted, Templar will
  print the result of templating to standard out.

That's it! There should now be a file in `<project>/blog/src/` called
`result.html` that contains the following:

    <html>
      <head>
        <title>This is a Templar example</title>
      </head>
      <body>
        <h1>This is a Templar example</title>
        <p>Published: <i>2014-06-08</i></p>

        <p>This Markdown file is a <em>Templar example</em>.</p>
      </body>
    </html>

Notice that all `{{ ... }}` expressions have been replaced accordingly
(the `{{ datetime.now() }}` expression will be different depending on
when you publish.

Our final directory structure looks like this:

    <project>/
        lib/
            templar/
        blog/
            src/
                templates/
                    template.html
                example.md
                result.html

Example
-------

For a more extensive example of how to use Templar, see the repository
for my [personal website](https://github.com/albert12132/albertwu.org).
It is often helpful to use a Makefile instead of directly running
Templar every time.

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

* A **variable** defined either within a Markdown source file or
  `config.py`. These "variable" names are more flexible than Python
  variable names, as they can include spaces and hyphens (the only
  restriction is they cannot contain newlines or colons).
* A **Python expression**. Any valid Python *expression* (not
  statements) can be used -- the `str` of the final value will be used
  in place of the `{{ ... }}`:

        <p>Date published: {{ datetime.now() }}</p>

  **Note**: `{{ ... }}` expressions will always be treated as variables
  first; if no such variable exists, before Templar will evaluate the
  expression as a Python expression instead.
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

### Template Inheritance

Templar also supports template inheritance. A "child" template can
specify which "parent" template to inherit by including the following
on the *very first line of the child template*:

    <% extends parent.html %>

In the "parent" template, you can define labels that "child" templates
can fill. Suppose the following content is found in `parent.html`:

    <div id='nav-bar'>
      <h3>Title</h3>

      {% nav-bar %}
    </div>

The `{% nav-bar %}` tag allows child templates to "override" parent
labels. Suppose the following content is found in `child.html`:

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

If a child template chooses not to inherit a tag, that tag will simply
be removed from the final document.

Source files
------------

### Markdown

A basic source file can simply contain regular Markdown. Templar uses a
Markdown converter that follows the [Daring
Fireball](http://daringfireball.net/projects/markdown/syntax)
specification.

In addition, Templar's Markdown parser supports variable definitions:

    ~ variable name: variable value

That is, a tilde (`~`) followed by at least one space, a variable name,
a colon, and a variable value. Variable declarations have the following
rules:

* `variable name` can contain any character that is not a newline and
  not a colon (`:`). This means variables can include spaces, hyphens,
  and underscores.
* `variable value` can contain any character that is not a newline.
  This means values can include spaces, hyphens, underscores, and
  colons (the first colon in the line is used as the separator)
* `variable value` will be taken *as is* (meaning it will not be parsed
  for Markdown)
* The variable declaration must be on one line

You can tell Templar to parse a content file as Markdown with use of
the `-m` flag:

    python3 templar compile template.html -s example.md -m
    python3 templar link example.md -m

### Other filetypes

Templar can also use non-Markdown files as content sources. For
example, we have a template called `homework.py` with the following:

    """Python homework"""

    {{ :all }}

    if __name__ == '__main__':
        main()

and a source file called `hw1.py` with the following:

    def question1(args):
        pass

    def question2(args):
        pass

Then the following command would publish a file called `pub/hw1.py`

    python3 templar compile homework.py -s hw1.py -d pub/hw1.py

Notice we omit the use of `-m`, since we are not publishing Markdown.
The contents of `pub/hw1.py` will look like the following:

    """Python homework"""

    def question1(args):
        pass

    def question2(args):
        pass

    if __name__ == '__main__':
        main()

* * *

There are also two special tags that can be used: the `<block>` tag and
the `<include>` tag. These tags can be used in any kind of source file
(Markdown or not).

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

The `<block>` tag can also be surronded by extra characters on the same
line:

    # <block python>
    def hello(world):
        return hi
    # </block python>

This allows blocks to be defined in source code (e.g. Python scripts)
as comments, so that the source code can be executed.

### `include` tag

The `<include>` tag allows you to link different sources
together. The idea is that sometimes, it is useful to write modular
Markdown sources to make it easier to manage directories. This also
makes it faster to refer to the same Markdown file without duplicating
its contents. Here is an example:

    Topics
    ------
    <include path/to/topics.md>


    Examples
    --------
    <include path/to/example.py>

    References
    ----------
    <include path/to/references:blockA>

In the example above, the first and second `include` tags simply use a
filepath. As in the example, any filetype can be included, irrespective
of the original source filetype (e.g. a Python file can be included in
a Markdown file), as long as the files are plain text.

The filepaths can be written in the following ways
* *relative to the directory in which you will run Templar*: this is
  always assumed by Templar first
* *relative to the current source file*: this is useful if the source
  file is close to other files that it is linking. Templar will assume
  the filepath is relative to the source file only if it cannot find
  the filepath relative to the working directory.

The first two `include` tags will simply copy all of the contents
listed inside of `path/to/topics.md` and `path/to/example.py` into the
locations of the `include` tags.

The third `include` tag also references a `blockA` inside of the file
`path/to/references.md`. This is useful if you only want to include a
subsection of another Markdown file. The syntax is the following:

    <include path/to/file:block-name>

#### Regular expressions

The block name in an `include` tag can also be a regular expression:

    <include path/to/file:block\d+>

Here, the regular expression will be `block\d+`. All blocks in
`path/to/file` whose names match the regular expression will be
included in place of the `include` tag. The blocks will be included in
the order they are defined in `path/to/file` (using their opening
`block` tag to define order).

Suppose the regular expression matches `block42`, `block2`, `block3`,
in that order. The `include` tag will be expanded into the following:

    <include path/to/file:block42>
    <include path/to/file:block2>
    <include path/to/file:block3>

### Custom patterns

You can define custom patterns in your source files, like the
following:

    Question 1
    ----------

    A question here.

    <solution>

    This is the solution to the question: `f = lambda x: f(x)`.

    </solution>

You can specify how to convert the `<solution>...</solution>` pattern
by defining a regular expression in `config.py`. For example,

    solution_re = re.compile(r"<solution>(.*?)</solution>", re.S)
    def solution_sub(match):
        return "<b>Solution</b>: " + match.group(1)

    SUBSTITUTIONS = [
        (solution_re, solution_sub),
    ]

would replace the `solution` tag with a boldface "Solution: " followed
by the contents within the solution tag. All regular expressions should
be listed inside of the `SUBSTITUTIONS` list (in `config.py`), along
with the corresponding substitution function.

**Important note**: the custom patterns are evaluated **after** all
linking (`include` tags) and all Markdown parsing has occurred. Thus,
in the example above, `solution_re` should expect the contents of the
solution tag to look like this:

    <p>this is the solution to the question: <code>f = lambda x:
    f(x)</code>.</p>

Other Features
--------------

### Linking

Templar's primary publishing method is to use templates via the
`compile` subcommand. However, if you do not need to use a template,
and simply want to link a source content file (through use of `include`
tags), you can use the `link` subcommand:

    python3 templar link example.md -m -d result.html

* `example.md` is the source file to link. This is a required argument
* `-m` tells Templar to parse the content as Markdown. You can omit
  this flag to skip Markdown parsing
* `-d result.html` tells Templar to write the result to a file called
  `result.html`. If this argument is omitted, Templar will print the
  result to standard out.

### Table of Contents

Templar has the capability to scrape headers to create a table of
contents. You can specify exactly *what* is defined to be a header in
`config.py`:

    header_regex = r"..."

    def header_translate(match):
        return ...

    def table_of_contents(lst):
        ...

* `header_regex` can either be a string or a `RegexObject`, and tell
Templar how to recognize a "header".
* `header_translate` takes a regular expression match and extracts
  information (e.g. the `id` attribute and title of an HTML `<h1>` tag)
* `table_of_contents` takes a list of expressions returned by
  `header_translate` and compiles the final table of contents.

The table of contents that is returned by `table_of_contents` is
available to templates with the expression

    `{{ table-of-contents }}`

### Header slugs

Templar's Markdown parser adds slugs to headers (`<h[1-6]>`). These
slugs are added as `id` attributes of the headers.

### Multiple `config.py` files

It can be useful to have a hierarchical `config` structure if you have
multiple directories with content, each with their own publishing
configurations. For example, suppose we have the following directory
structure:

    <project>/
        lib/
            templar/
        articles/
            config.py
            blog/
                config.py
            projects/
                config.py

We have a directory for articles that contains some general
configurations (e.g. a table of contents scraper). In the `blog` and
`projects` directories, we have more specific config files (e.g.
substitutions for different types of articles).

If we run Templar from the `blog` directory

    python3 ../../lib/templar compile ...

Templar will use the following method to search for configs:

* Find the lowest common ancestor of `<project>/articles/blog/` and
  `<project>/lib/templar/` (in this case, the ancestor is `<project>/`
* Starting from the ancestor (`<project>/`), Templar will traverse down
  to `<project>/articles/blog/`
* At each intermediate directory, Templar will scan for a `config.py`
  file. If one exists, it will accumulate the contents of that
  `config.py` with all the other configs it has seen before.


Acknowledgements
----------------

Templar is an extension of the program that used to generate my
personal website. The idea for linking (the `include` and `block` tags)
conceived while developing the publisher for UC Berkeley's CS 61A labs.

The Markdown parser is a re-implementation of
[markdown2](https://github.com/trentm/python-markdown2), a Python
implementation of the original Perl Markdown parser. The variant of
Markdown that Templar supports is a subset of [Daring Fireball's
Markdown
specification](http://daringfireball.net/projects/markdown/syntax).

Syntax for template inheritance and expression substitution are
inspired by [Django](https://www.djangoproject.com/)'s templating
syntax, as well as [ejs](http://embeddedjs.com/)'s templating syntax.
