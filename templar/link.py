import argparse
import os
import re
import sys
import textwrap
from collections import OrderedDict
from templar.markdown import convert
from templar import log

##############
# Public API #
##############

def link(filepath):
    """Link the text based on <include> tags.

    An include tag should have the following syntax:

        <include path/to/file.ext>

    The file can be of any filetype (as long as it is plaintext), and
    <include> tags can have paths to any filetype (even filetypes that
    are different from the original source file). Using the above
    syntax, all of the contents of the included file will be
    substituted for the tag.

    There is an alternate syntax:

        <include path/to/file.ext:blockName>

    The block specified by blockName should be defined using the
    <block> tag in file.ext. Only the contents within blockName will
    be included.

    Note that blockName is a specific use case of a general pattern:

        <include path/to/file.ext:blockRegex>

    where blockRegex is a regular expression that matches block
    names. Each block that is matched by blockRegex acts as if it
    had been written in its own include tag. For example, if the
    regular expression "block\d" matches three blocks "block1",
    "block2", and "block3", then the include tag will be expanded into

        <include path/to/file.ext:block1>
        <include path/to/file.ext:block2>
        <include path/to/file.ext:block3>

    Block names that are matched by the regular expression will be
    included in the order that they were defined in file.ext.

    Note: the regular expression must match the entire block name. For
    example, if blockRegex was "block\d", it would not match a block
    called "block10".

    RETURNS:
    text -- str; the text after resolving all include tags. Any block
            tags that are left over are preserved in text.
    """
    return substitute_links(file_read(filepath), OrderedDict(),
            os.path.dirname(filepath))

def retrieve_blocks(text):
    """Strip block tags from text and return a mapping of block
    names to block contents.

    RETURNS:
    text     -- str; the text with all block tags removed
    mappings -- dict; mapping of block names to block contents
                (strings)
    """
    cache = {}
    return cache_blocks('', text, cache), cache

def substitutions(text, subs, args):
    """Apply regular expression substitutions defined for custom
    patterns.

    PARAMETERS:
    text -- str; original source text
    subs -- list of 2-tuples (regex, sub); regex is either a str or a
            RegexObject, which defines the pattern. sub is a
            substitution function or a string, as used by re.sub

    The (regex, sub) pairs will be applied in the order that they
    appear in subs. This means it is the responsibility of the caller
    of this function to select a proper ordering of substitutions.

    RETURNS:
    text -- str; the text after applying all substitutions in subs
    """
    if not args.conditions:
        args.conditions = []
    for regex, sub, *conditions in subs:
        if all(cond(args) for cond in conditions):
            text = re.sub(regex, sub, text)
    return text

def scrape_headers(text, builder):
    """Scrape headers based on a regular expression and substitution.

    PARAMETERS:
    text      -- str; the source text
    regex     -- str or RegexObject; a regular expression that defines
                 the semantics of a header
    translate -- function; a function that takes in a Match object.
                 The translation function converts the match into
                 a final representation of the header (i.e. the
                 return value will typically be a string, but can
                 be any object).

    regex and translate provide some flexibility in defining what a
    "header" is. For example, a header can be defined as all
    <h[0-6]> tags in an HTML document to create a table of contents.
    Alternatively, a header can be defined as a function signature
    in a Python script.

    RETURNS:
    headers -- list; headers, as converted by the translate function.
               the contents of this list can be any data type; they
               will appear in the order that the original headers
               are placed within text
    """
    return builder(text).result

##########
# Linker #
##########

re_include = re.compile(r"""
(?:(?<=\n)|(?<=\A))
([ \t]*)      # \1 is leading whitespace
<\s*
    include
    \s+
    (.+?)       # \2 is filename
    (?:
        :       # colon as delimiter
        (.+?)   # \3 is block regex
    )?          # optional
\s*>
""", re.X)
def substitute_links(text, cache, base_dir):
    """Substitutes all <include> links in text relative to base_dir,
    using and updating cache as a reference for blocks.

    PARAMETERS:
    text     -- str; text to link
    cache    -- dict; mapping of block names to block contents. Block
                names take the form "filename:blockname"
    base_dir -- str; base directory for resolving relative filepaths

    NOTE:
    The cache parameter is updated in the mutually recursive call.
    It is best to pass in an empty dictionary when calling this
    function for the first time.

    RETURNS:
    linked_text -- str; text with all <include>s resolved
    """
    def link_sub(match):
        filename = match.group(2)
        regex = match.group(3)
        if not file_exists(filename):
            filename = os.path.join(base_dir, filename)
            if not file_exists(filename):
                log.warn("Could not find file " + match.group(2) \
                        + " or " + filename)
                return ''

        text = retrieve_and_link(filename, cache)
        if not regex:
            result = cache[filename + ':all']
        else:
            result = resolve_include_regex(regex, cache, filename)
        return textwrap.indent(result, match.group(1))
    return re_include.sub(link_sub, text)

def retrieve_and_link(filename, cache):
    """Retrieves the contents found in filename and recursively
    resolves links in those contents, updating cache with blocks found
    in the contents.

    PARAMETERS:
    filename -- str; name of file to retrieve
    cache    -- dict; mapping of block names to block contents. Block
                names take the form "filename:blockname"

    RETURNS:
    contents -- str; linked results of file contents
    """
    text = file_read(filename)
    text = substitute_links(text, cache, os.path.dirname(filename))
    cache_blocks(filename, text, cache)
    return text

def resolve_include_regex(regex, cache, filename):
    """Resolves an <include> that contains a regular expression.

    PARAMETERS:
    regex    -- str or RegexObject; regular expression for block names.
                regex must match the entire block name
    cache    -- dict; mapping of block names to block contents. Block
                names take the form "filename:blockname"
    filename -- str; file in which to look for blocks

    NOTE:
    The order in which this function matches blocks depends entirely
    on the __iter__ function of the cache. Built-in dictionaries have
    an arbitrary ordering. For ordering, use of an OrderedDict is
    suggested.

    RETURNS:
    text -- str; all <include>s linked together, with only a newline
            separating them
    """
    contents = []
    for block in cache:
        if ':' not in block:
            continue
        block_file, block_name = block.split(':', 1)
        if re.match('^' + regex + '$', block_name) and \
                filename == block_file and\
                block_name != 'all':
            contents.append(cache[block])
    if regex == 'all' and not contents:
        contents.append(cache[filename + ':all'])
    return '\n'.join(contents)


re_block = re.compile(r"""
[^\n]*      # strip out extra leading characters
<\s*
    block
    \s+
    (.+?)   # \1 is block name
\s*>
[^\n]*\n    # strip out extra ending characters
(.*?)       # \2 is block contents
\n[^\n]*    # strip out extra leading characters
</\s*       # forward slash to denote closing tag
    block
    \s+
    \1
\s*>
[^\n]*      # strip out extra ending characters
""", re.S | re.X)
# TODO refactor
re_open_block = re.compile(r"""
[^\n]*
<\s*
    block
    \s+
    (.+?)       # \1 is block name
\s*>
(\n|\Z)
""", re.S | re.X)
re_close_block = re.compile(r"""
(\n|\A)
[^\n]*
<\s* / \s*
    block
    \s+
    (.+?)       # \1 is block name
\s*>
""", re.S | re.X)

def cache_blocks(filename, text, cache):
    while re_block.search(text):
        for name, contents in re_block.findall(text):
            contents = cache_blocks(filename, contents, cache)
            cache[filename + ':' + name] = contents
        text = re_block.sub(lambda m: m.group(2), text)
    # TODO refactor
    text = re_open_block.sub('', text)
    text = re_close_block.sub('', text)
    cache[filename + ':all'] = text
    return text

##################
# File Utilities #
##################

def file_exists(filename):
    """Checks if a file exists relative to os.getcwd().

    NOTE:
    This function exists to make test injection easier.

    RETURNS:
    bool; True if filename exists
    """
    return os.path.exists(filename)

def file_read(filename):
    """Reads contents of a specified file.

    NOTE:
    This function exists to make test injection easier.

    RETURNS:
    text -- str; contents of file
    """
    with open(filename, 'r') as f:
        return f.read()

def file_write(filename, text):
    """Writes text to a specified file.

    NOTE:
    This function exists to make test injection easier.
    """
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(text)


##########################
# Command-line Interface #
##########################

def cmd_options(parser):
    parser.add_argument('source', type=str,
                        help="Link contents of source file")
    parser.add_argument('-d', '--destination', type=str,
                        help="Store result in destination file")
    parser.add_argument('-m', '--markdown', action='store_true',
                        help="Use Markdown conversion")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Suppresses extraneous output")
    parser.add_argument('-c', '--conditions', action='append',
                        help="Specify conditions for substitutions")

def main(args, configs):
    if not os.path.exists(args.source):
        log.warn('File ' + args.source + ' does not exist.')
        exit(1)
    elif not os.path.isfile(args.source):
        log.warn(args.source + ' is not a valid file')
        exit(1)
    result = link(args.source)
    if args.markdown:
        result = convert(result)
    result = substitutions(result,
                           configs.get('SUBSTITUTIONS', []),
                           args)
    result, cache = retrieve_blocks(result)
    if args.destination:
        file_write(args.destination, result)
        log.info('Result can be found in ' + args.destination)
    else:
        log.log('--- BEGIN RESULT ---', args.quiet)
        log.log(result)
        log.log('--- END RESULT ---', args.quiet)

if __name__ == '__main__':
    log.log('Usage: python3 __main__.py link ...')

