~ title: hello there world
~ date: 09/23/1023
~ another-var: this will be a string

Hello World!
============

Second header
-------------

Header with `code`
==================

<include path/to/stuff:blockA>

# Title 1
## Title 2
### Title 3
#### Title 4
##### Title 5
###### Title 6

`normal tick`

``multiple ticks with a ` in here``

`tick with a new
line`

_emph_
__strong__
___emphstrong___

\*Not an emph\*
\_Not an emph\_

\\   backslash
\`   backtick
\*   asterisk
\_   underscore
\{\}  curly braces
\[\]  square brackets
\(\)  parentheses
\#   hash mark
\+   plus sign
\-   minus sign (hyphen)
\.   dot
\!   exclamation mark


`some <code> that should be &escaped`

This is a paragraph with a **strong tag** and an *em tag* in it. It
also has a `code tag`, along with a [link
here](path/to/link_here.html). How do you think ![images](alt_text.png)
would look? How about a ***strong em tag***? Throw <span class='hi'>in
a span element</span> just for kicks.

* List level 1

    this shoudl be on the same line
and so should this
    * List item 2
    * List item 3
* List item 4
    * List item 5

Text text text

* List item 2
    * List item 4
        * List item 1




Stuff here

This should not be in a list

* List level 1
  this is still on the same line
    1. List level 2
       This is still on the same line
        * List level 3
            2. List level 4
* List item 2

take 2

*   List level 1
    this is still on the same line
    1.  List level 2
        This is still on the same line
        *   List level 3
            2.  List level 4
*   List item 2

stff

* stuff
    * stuff
        * stuff
* stuff


Some stuff here

1. Item 1
2. Item 2
    3. Item 3

list ended

* this is a list `with a span

        This is a code block
            whitespace should       be preserved
* list item 2

The code block ended.

> block quote?
> why not?
> this is a type of block quotethis is a type of block quotethis is a
> type of block quote

> why not?
this is a type of block quotethis is a type of block quotethis is a
type

Stuff here should not be in blockquote
> begin blockquote
   here this should be blockquote too



> stuff here



stuff here

<question name='boo'>
This is a custom tag. For example, perhaps we want to design a question
for a class.

    That would be pretty cool
    def hi(sl):
        ***this should not turn into a tag***
        `return`

    def boom('hi')

  This should not be in codeblock
    This should be a new codeblock

The following is another code block:

    def boom(bop):
        print('bim')

        return hi




Stuff here

<solution>
    def cool(hi):
        return cool
</solution>

<block example>
This is an example of a block. Another markdown file can specify this
tag and all contents in this block will be included there. The can do
this by using the

- - - -

stuff

---------

<include path/to/this/cool_file:example>
<include path/to/this/cool_file:example>
</stuff>

syntax.
</block example>

> Blockquote
Blockquote

> Blockquote
Blockquote

This stuff here should not be in blockquote

> blockquote
> 
> Header in blockquote
> --------------------

> > Blockquote in blockquote
> > block quote in block quote

Header
------

---------------


Paragraph there
* hi there
* hi there

A codeblock precedes:
    This is a code block
    This is a code block
Should end here

[link here](this/link/contains "a title")
![link here](this/link/contains "a title")

[Trying out a ref][google]
[apple store][]

This is a path to
~cs61a/lib/stuff here: and there

[google]: www.albertwu.org "title here"
[apple store]: www.albertwu.org

Here is AT&T, but this &#49 should not be escaped

* list
* list

