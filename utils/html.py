
##################
# Header Regexes #
##################

header_regex = re.compile(r"""
    <\s*
    h([1-6])        # \1 is the header level
    (?:
        .*?         # attributes
        id=(['"])   # \2 is the quote
        (.*?)       # \3 is the actual id
        \2          # closing quote
        .*?         # attributes
    )?>
    (.*?)           # \4 is the header title
    <\s*/\s*
    h\1             # closing header tag
    \s*>
""", re.X)
def header_translate(match):
    return match.group(1), match.group(3), match.group(4)
