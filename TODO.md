TODO
====

Main
----

* feature: add version checking and warn when running stale version
  (have config.py store a version number; when config.py version number
  is greater than templar version, it is stale)

Markdown
--------

* task: refactor and document

[Markdown Extra]: http://michelf.ca/projects/php-markdown/extra/#markdown-attr

Link
----

* task: refactor and document
* feature: extend conditional compilation to headers and variables
  on command line arguments)

Compile
-------

* task: add tests
* bug: newlines in {{ .. }} expressions cause non-termination
* feature: add conditionals and loops
* bug: path configuration broken for python3.2
