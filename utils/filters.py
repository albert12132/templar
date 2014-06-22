import re

def has_source(filepattern):
    """Returns a filter that returns true if the source has a filename
    that matches the file pattern.
    """
    def filter(info):
        return re.search(filepattern, info.source) is not None
    return filter

def has_destination(filepattern):
    """Returns a filter that returns true if the source has a filename
    that matches the file pattern.
    """
    def filter(info):
        return re.search(filepattern, info.destination) is not None
    return filter

def is_markdown():
    """Returns a filter that returns true if the source file is a
    Markdown file.
    """
    return has_source(r'.*\.md$')

def is_python():
    """Returns a filter that returns true if the source file is a
    Python file.
    """
    return has_source(r'.*\.py$')

def has_arguments(*args):
    """Returns a filter that returns true if all of the arguments
    are passed as command line options to Templar.
    """
    def filter(info):
        return all(a in info.conditions for a in args)
    return filter

