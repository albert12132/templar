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

Source files
------------

Currently, Templar only supports Markdown as its content markup
language. A basic source file can simply contain regular Markdown.
There are also two special tags that can be used: the `<include>` tag
and the `<block>` tag.

### The `include` tag

Sometimes, it is helpful to organize source files in a modular fashion.
For example, let's say we 

Templates
---------
