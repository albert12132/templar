"""
Linker utilities.
"""

import os
import re

def get_block_map(source_path):
    """Processes the contents of source_path and returns a dictionary of block names to Blocks."""
    if not os.path.isfile(source_path):
        raise SourceNotFound(source_path)
    with open(source_path, 'r') as f:
        content = f.read()
    block_map = BlockMap(source_path)  # The map will be populated with the following function call.
    link_stack = LinkStack(source_path)
    convert_block_to_string(content, block_map, link_stack, source_path)
    return block_map


class BlockMap(object):
    """A map of block names to block contents (str -> str)."""
    def __init__(self, source):
        # _blocks will be a nested dictionary. Specifically,
        # { filename : { block_name : block_contents } }
        self._blocks = {}
        self._variables = {}
        self.source = source

    def get_block_variables(self):
        """Returns a dictionary mapping block names to block contents, where all block names
        correspond to blocks in the source file only.
        """
        if self.source not in self._blocks:
            raise SourceNotFound(self.source)
        return self._blocks[self.source].copy()

    def get_variables(self):
        return self._variables

    ###########
    # Private #
    ###########

    def add_block(self, filename, block_name, content):
        file_blocks = self._blocks.setdefault(filename, {})
        if block_name in file_blocks:
            raise InvalidBlockName(
                'Found multiple blocks with name "{}" in {}'.format(block_name, filename))
        file_blocks[block_name] = content

    def has_block(self, filename, block_name):
        return filename in self._blocks and block_name in self._blocks[filename]

    def get_block(self, filename, block_name):
        assert self.has_block(filename, block_name)
        return self._blocks[filename][block_name]

    def add_variable(self, variable, value):
        self._variables[variable] = value


###########
# Private #
###########

class LinkStack(object):
    """A stack used for keeping track of link dependencies, detecting cycles if they appear."""
    def __init__(self, filename):
        self._stack = [filename]

    def push(self, filename):
        if filename in self._stack:
            raise CyclicalIncludeError(self._stack, filename)
        self._stack.append(filename)

    def pop(self):
        self._stack.pop()


block_regex = re.compile(r"""
    [^\n]*?               # strip out extra leading characters
    <\s*
        block\s+([\w -]+) # \1 is the block name. Matches alphanumerics, hyphen, and space
    \s*>
    .*?\n                 # strip out extra ending characters
    (.*?)                 # \2 is block contents
    \n?[^\n]*             # strip out extra leading characters
    </\s*                 # forward slash to denote closing tag
        block\s+\1
    \s*>
    [^\n]*                # strip out extra ending characters
""", re.S | re.X)

def convert_block_to_string(content, block_map, link_stack, source_path, block_name='all'):
    """Converts the specified block content into a string.

    Nested blocks are recursively converted into strings and cached in the block_map. Include tags
    are processed as well. The resulting block string is also added to the block_map, along with any
    nested blocks.

    PARAMETERS:
    content     -- str; content to be converted into a Block.
    block_map   -- BlockMap
    link_stack  -- LinkStack
    source_path -- str; the path of the file from which this content came, relative to the current
                   working directory.
    block_name  -- str; the name of the block that contains this content. By default, the name is
                  'all'

    RETURNS:
    str; the result of converting the block content.
    """
    segments = []
    inner_block_name = None
    for i, match in enumerate(block_regex.split(content)):
        if i % 3 == 0 and match != '':
            # Non-block text. Process for links and add to segments. Omit empty matches.
            segments.extend(process_links(match, block_map, link_stack, source_path))
        elif i % 3 == 1:
            # Block name.
            if match == 'all':
                raise InvalidBlockName('"all" is a reserved block name, '
                    'but found block named "all" in ' + source_path)
            inner_block_name = match
        elif i % 3 == 2:
            # Block contents. Recursively convert contents to a Block.
            inner_block = convert_block_to_string(
                match,
                block_map,
                link_stack,
                source_path,
                inner_block_name)
            segments.append(inner_block)

    result = ''.join(segments)
    block_map.add_block(source_path, block_name, result)
    return result


include_regex = re.compile(r"""
    ^([ \t]*)        # \1 is leading whitespace
    <\s*include\s+
        (.+?)       # \2 is filename
        (:.+?)?     # \3 is (optional) block name with leading colon
    \s*>.*$
""", re.M | re.X)

variable_regex = re.compile(r"""
    ^~\s*        # Begins with ~
    (.+?)        # \1 is variable name
    \s*:\s*      # Colon delimiter
    (.+?)        # \2 is value
    \s*(?:\n|\Z) # Remove trailing newline.
""", re.X | re.M)

def process_links(content, block_map, link_stack, source_path):
    """Process a string of content for include tags.

    This function assumes there are no blocks in the content. The content is split into segments,
    with include tags being replaced by Block objects.

    PARAMETERS:
    content     -- str; content to be converted into a Block.
    block_map   -- BlockMap
    link_stack  -- LinkStack
    source_path -- str; the filepath of the file from which this content came.

    RETURNS:
    list of str; segments that the comprise the content.
    """
    segments = []
    leading_whitespace = None
    include_path = None
    for i, match in enumerate(include_regex.split(content)):
        if i % 4 == 0 and match != '':
            # Regular text. Omit empty matches. Process for variables.
            for variable, value in variable_regex.findall(content):
                block_map.add_variable(variable, value)
            stripped_of_variables = variable_regex.sub('', match)
            segments.append(stripped_of_variables)
        elif i % 4 == 1:
            # Leading whitespace
            leading_whitespace = match
        elif i % 4 == 2:
            # Include path.
            include_path = match
        elif i % 4 == 3:
            # Optional block name. If match is None, block name was ommitted (default to 'all').
            block_name = match.lstrip(':') if match is not None else 'all'
            block = retrieve_block_from_map(
                    source_path,
                    include_path.strip(),
                    block_name.strip(),
                    leading_whitespace,
                    block_map,
                    link_stack)
            segments.append(block)
    return segments


def retrieve_block_from_map(
        source_path,
        include_path,
        block_name,
        leading_whitespace,
        block_map,
        link_stack):
    """Given a source directory, the path specified in an include tag, and the block name, retrieve
    the corresponding Block from the block_map (adding it to the map if necessary).

    The paths in include tags are interpreted as follows:

    1. relative to the directory of source_path.
    2. relative to the current working directory.

    If the included block is not found in either location, an exception is raised. If a cycle is
    detected, an exception is raised.
    """
    # Check if the included file exists.
    relative_to_source = os.path.join(os.path.dirname(source_path), include_path)
    if os.path.isfile(relative_to_source):
        filename = relative_to_source
    elif os.path.isfile(include_path):
        filename = include_path
    else:
        raise IncludeNonExistentBlock(
            source_path + ' tried to include a non-existent file: ' + include_path)

    # Add included file to stack, checking for cycles in the process.
    link_stack.push(filename)

    # Process the block's file if it hasn't been processed before.
    if not block_map.has_block(filename, block_name):
        with open(filename, 'r') as f:
            content = f.read()
        convert_block_to_string(content, block_map, link_stack, filename)

    # If the block is not in the map even after converting, then the block doesn't exist.
    if not block_map.has_block(filename, block_name):
        raise IncludeNonExistentBlock(
            source_path + ' tried to include a non-existent block: ' + filename + ':' + block_name)

    link_stack.pop()
    return indent(block_map.get_block(filename, block_name), leading_whitespace)


def indent(content, whitespace):
    lines = content.splitlines()
    indented_lines = map(lambda line: whitespace + line, lines)
    return '\n'.join(indented_lines)


##############
# Exceptions #
##############

class InvalidBlockName(Exception):
    pass

class IncludeNonExistentBlock(Exception):
    pass

class CyclicalIncludeError(Exception):
    def __init__(self, link_stack, last_file):
        super().__init__(' -> '.join(link_stack + [last_file]))

class SourceNotFound(Exception):
    def __init__(self, source_path):
        super().__init__('Could not find source file: ' + source_path)
