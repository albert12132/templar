"""
Linker utilities.
"""

from templar.exceptions import TemplarError

import os
import re

def link(source_path):
    """Links the content found at source_path and represents a Block that represents the content."""
    if not os.path.isfile(source_path):
        raise SourceNotFound(source_path)
    with open(source_path, 'r') as f:
        content = f.read()
    block_map = BlockMap()  # The map will be populated with the following function call.
    all_block = convert_lines_to_block(
            content.splitlines(), block_map, LinkStack(source_path), source_path)
    return all_block, block_map.get_variables()


def get_block_dict(top_level_block):
    """Returns a dictionary of block names (str) to block contents (str) for all child blocks, as
    well as the original block itself.

    The block_dict argument is only used for recursive calls and should not 
    """
    block_stack = [top_level_block]
    block_dict = {}
    while block_stack:
        block = block_stack.pop()
        block_dict[block.name] = str(block)
        for segment in block.segments:
            if isinstance(segment, Block):
                block_stack.append(segment)
    return block_dict


class Block(object):
    def __init__(self, source_path, name, segments):
        self.source_path = source_path
        self.name = name
        self.segments = segments
        self._str = None  # Cache the str representation of this block.

    def apply_rule(self, rule):
        self._str = None  # Clear str cache.
        for i, segment in enumerate(self.segments):
            assert isinstance(segment, str) or isinstance(segment, Block)
            if isinstance(segment, str):
                self.segments[i] = rule.apply(segment)
            else:
                segment.apply_rule(rule)  # Recursively apply rule onto nested blocks.

    def __str__(self):
        if self._str is None:
            self._str = '\n'.join(str(segment) for segment in self.segments)
        return self._str


###########
# Private #
###########

class BlockMap(object):
    """A map of block names to block contents (str -> str)."""
    def __init__(self):
        # _blocks will be a nested dictionary. Specifically,
        # { filename : { block_name : block_contents } }
        self._blocks = {}
        self._variables = {}

    def get_variables(self):
        return self._variables

    def add_block(self, block):
        file_blocks = self._blocks.setdefault(block.source_path, {})
        if block.name in file_blocks:
            raise InvalidBlockName(
                'Found multiple blocks with name "{}" in {}'.format(block.name, block.source_path))
        file_blocks[block.name] = block

    def has_block(self, filename, block_name):
        return filename in self._blocks and block_name in self._blocks[filename]

    def get_block(self, filename, block_name):
        assert self.has_block(filename, block_name)
        return self._blocks[filename][block_name]

    def add_variable(self, variable, value):
        self._variables[variable] = value


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


ALL_BLOCK_NAME = 'all'

BLOCK_OPEN_REGEX = re.compile("""
^.*?<\s*block\s+
([\w -]+)           # \1 is the block name
\s*>.*$
""", re.X)

BLOCK_CLOSE_REGEX = re.compile("""
^.*?<\s*/\s*block\s+
([\w -]+)           # \1 is the block name
\s*>.*$
""", re.X)

INCLUDE_REGEX = re.compile(r"""
^([ \t]*)       # \1 is leading whitespace
<\s*include\s+
    (.+?)       # \2 is filename
    (:.+?)?     # \3 is (optional) block name with leading colon
\s*>.*$
""", re.X)

VARIABLE_REGEX = re.compile(r"""
^~\s*        # Begins with ~
(.+?)        # \1 is variable name
\s*:\s*      # Colon delimiter
(.+?)        # \2 is value
\s*(?:\n|\Z) # Remove trailing newline.
""", re.X)


def convert_lines_to_block(lines, block_map, link_stack, source_path, block_name=ALL_BLOCK_NAME):
    """Converts the specified block content lines (list of strings) into a Block object.

    Nested blocks are recursively converted into strings and cached in the block_map. Include tags
    are processed as well. The resulting block string is also added to the block_map, along with any
    nested blocks.

    PARAMETERS:
    lines       -- str; content lines to be converted into a Block.
    block_map   -- BlockMap
    link_stack  -- LinkStack
    source_path -- str; the path of the file from which this content came, relative to the current
                   working directory.
    block_name  -- str; the name of the block that contains this content. By default, the name is
                  'all'

    RETURNS:
    Block; the result of converting the block content.
    """
    found_closing_block = False
    segments = []
    while lines:
        line = lines.pop(0)

        # Check if the line is a closing tag. This should only occur if we encounter the closing
        # block tag that matches the block_name parameter.
        close_tag_match = BLOCK_CLOSE_REGEX.match(line)
        if close_tag_match:
            if close_tag_match.group(1) != block_name:
                raise InvalidBlockName('Expected closing block ' + block_name + \
                    'but found block named "' + block_tag_match.group(1) + '" in ' + source_path)
            # If the block name is valid, we are done processing this block.
            found_closing_block = True
            break

        # Otherwise, check if the line is a nested block.
        open_tag_match = BLOCK_OPEN_REGEX.match(line)
        if open_tag_match:
            # Make sure the block name is not the reserved ALL_BLOCK_NAME.
            inner_block_name = open_tag_match.group(1)
            if inner_block_name == ALL_BLOCK_NAME:
                raise InvalidBlockName(
                    '"{0}" is a reserved block name, but found block named "{0}" in {1}'.format(
                        ALL_BLOCK_NAME, source_path))

            # Recursively convert nested block contents to a Block.
            inner_block = convert_lines_to_block(
                lines,
                block_map,
                link_stack,
                source_path,
                inner_block_name)
            segments.append(inner_block)
            continue

        # Otherwise, check if the line is a variable. The line should be omitted.
        variable_match = VARIABLE_REGEX.match(line)
        if variable_match:
            process_variable(variable_match, block_map)
            continue

        # Otherwise, check if the line is an include tag.
        include_match = INCLUDE_REGEX.match(line)
        if include_match:
            included_content = process_links(include_match, block_map, link_stack, source_path)
            # Omit empty content.
            if included_content != '':
                append_text_to_segments(segments, included_content)
        else:
            append_text_to_segments(segments, line)

    if block_name != ALL_BLOCK_NAME and not found_closing_block:
        raise InvalidBlockName(
                'Expected closing block called "{0}" in {1}'.format(block_name, source_path))

    block = Block(source_path, block_name, segments)
    block_map.add_block(block)
    return block


def append_text_to_segments(segments, text):
    if segments and not isinstance(segments[-1], Block):
        segments[-1] = segments[-1] + '\n' + text
    else:
        segments.append(text)


def process_variable(variable_match, block_map):
    variable = variable_match.group(1)
    value = variable_match.group(2)
    block_map.add_variable(variable, value)


def process_links(include_match, block_map, link_stack, source_path):
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
    leading_whitespace = include_match.group(1)
    include_path = include_match.group(2)

    # Optional block name. If match is None, block name was ommitted (default to 'all').
    block_name = include_match.group(3)
    if block_name is not None:
        block_name = block_name.lstrip(':')
    else:
        block_name = ALL_BLOCK_NAME

    return retrieve_block_from_map(
            source_path,
            include_path.strip(),
            block_name.strip(),
            leading_whitespace,
            block_map,
            link_stack)


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
        convert_lines_to_block(content.splitlines(), block_map, link_stack, filename)

    # If the block is not in the map even after converting, then the block doesn't exist.
    if not block_map.has_block(filename, block_name):
        raise IncludeNonExistentBlock(
            source_path + ' tried to include a non-existent block: ' + filename + ':' + block_name)

    link_stack.pop()
    # Convert the Block to a string and indent.
    return indent(str(block_map.get_block(filename, block_name)), leading_whitespace)


def indent(content, whitespace):
    lines = content.splitlines()
    indented_lines = map(lambda line: whitespace + line, lines)
    return '\n'.join(indented_lines)


##############
# Exceptions #
##############

class InvalidBlockName(TemplarError):
    pass

class IncludeNonExistentBlock(TemplarError):
    pass

class CyclicalIncludeError(TemplarError):
    def __init__(self, link_stack, last_file):
        super().__init__(' -> '.join(link_stack + [last_file]))

class SourceNotFound(TemplarError):
    def __init__(self, source_path):
        super().__init__('Could not find source file: ' + source_path)

