Templar
=======

Templar is a static templating engine written in Python that is
designed to be lightweight and flexible. Templar supports template
inheritance and modular source files, as well as the ability to define
custom Markdown patterns.

See the [Templar
Wiki](https://github.com/albert12132/templar/wiki/Getting-started)
for help with getting started.

Contributing
------------

1. After cloning the repo, create a virtualenv with Python 3.3 or
   above:
        virtualenv -p python3 .
2. Install requirements:
        pip install -r requirements.txt
3. Create a development version of `templar`:
        python setup.py develop

You can use `nose` to run tests from the root:
    nosetests tests

