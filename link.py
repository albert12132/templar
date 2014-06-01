import argparse
import os
import re

# TODO
try:
    import controller
except ImportError:
    controller = None

##############
# Public API #
##############

def link(text):
    """Link the text based on <include> tags.

    An include tag should have the following syntax:

        <include path/to/file.ext>

    The file can be of any filetype, and include tags can have paths
    to any filetype (even filetypes that are different from the
    original source file). Using the above syntax, all of the contents
    of the included file will be substituted for the tag.

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

    Note: the regular expression must match the entire block name. For
    example, if blockRegex was "block\d", it would not match a block
    called "block10".

    RETURNS:
    text -- str; the text after resolving all include tags. Any block
            tags that are left over are preserved in text.
    """
    return substitute_links(text, {})

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

def substitutions(text, subs):
    """Apply regular expression substitutions defined for custom
    patterns.

    PARAMETERS:
    text -- str; original source text
    subs -- list of 2-tuples (regex, sub); regex is either a str or a
            RegexObject, which defines the pattern. sub is a
            substitution function, as used by re.sub

    The (regex, sub) pairs will be applied in the order that they
    appear in subs. This means it is the responsibility of the caller
    of this function to select a proper ordering of substitutions.

    RETURNS:
    text -- str; the text after applying all substitutions in subs
    """
    for regex, sub in subs:
        text = re.sub(regex, sub, text)
    return text

def scrape_headers(text, regex, translate):
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
    return [translate(match) for match in re.findall(regex, text)]

##########
# Linker #
##########

re_include = re.compile(r"""
    <\s*
        include
        \s+
        (.+?)       # \1 is filename
        (?:
            :       # colon as delimiter
            (.+?)   # \2 is block regex
        )?          # optional
    \s*>
""", re.X)
def substitute_links(text, cache, base_dir):
    """Create a function that acts as a substitution function for the
    include-tag regex.
    """
    def link_sub(match):
        filename = match.group(1)
        regex = match.group(2)
        if not os.path.exists(filename):
            filename = os.path.join(base_dir, filename)
        text = retrieve_and_link(filename, cache)
        if not regex:
            return cache[filename + ':all']
        return '\n'.join([cache[block] for block in cache
                          if re.match('^' + regex + '$',
                                      block.split(':')[-1])])
    return re_include.sub(link_sub, text)

def retrieve_and_link(filename, cache):
    with open(filename, 'r') as f:
        text = f.read()
    text = substitute_links(text, cache, os.path.dirname(filename))
    cache_blocks(filename, text, cache)
    return text

re_block = re.compile(r"""
    [^\n]*
    <\s*
        block
        \s+
        (.+?)       # \1 is block name
    \s*>
    [^\n]*\n
    (.*?)           # \2 is block contents
    \n[^\n]*
    </\s*        # forward slash to denote closing tag
        block
        \s+
        \1
    \s*>
    [^\n]*
""", re.S | re.X)

def cache_blocks(filename, text, cache):
    while re_block.search(text):
        for name, contents in re_block.findall(text):
            contents = cache_blocks(filename, contents, cache)
            cache[filename + ':' + name] = contents
        text = re_block.sub(lambda m: m.group(2), text)
    cache[filename + ':all'] = text
    return text


##########################
# Command-line Interface #
##########################

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help="Link contents of file")
    parser.add_argument('-d', '--destination', type=str,
                        help="Store result in destination file")
    parser.add_argument('-c', '--cache', action='store_true',
                        help="Show cache keys")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print('File ' + args.file + ' does not exist.')
        exit(1)
    elif not os.path.isfile(args.file):
        print(args.file + ' is not a valid file')
        exit(1)
    with open(args.file, 'r') as f:
        result = link(f.read())
    if args.cache:
        result, cache = retrieve_blocks(result)
        print('--- Cache keys ---')
        for k in sorted(cache):
            print(k)
    if args.destination:
        with open(args.destination, 'w') as f:
            f.write(result)
        print('Result can be found in ' + args.destination)
    else:
        print('--- BEGIN RESULT ---')
        print(result)
        print('--- END RESULT ---')

if __name__ == '__main__':
    main()

