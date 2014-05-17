import re
from random import randint
from hashlib import sha1
import cgi

TAB_SIZE = 4
SALT = bytes(randint(0, 1000000))
def hash_text(s, label):
    return label + '-' + sha1(SALT + s.encode("utf-8")).hexdigest()

def process(text):
    text = handle_whitespace(text)
    text, variables = store_vars(text)
    hashes = {}
    text = convert_lists(text, hashes)
    text = hash_codeblocks(text, hashes)
    text = blockquote_re.sub(blockquote_sub, text)
    text = hash_code(text, hashes)
    text = hash_links(text, hashes)
    text = hash_tags(text, hashes)
    text = emphasis_re.sub(emphasis_sub, text)
    text = escape_re.sub(escapes_sub, text)
    text = atx_header_re.sub(atx_header_sub, text)
    text = setext_header_re.sub(setext_header_sub, text)
    text = paragraph_re.sub(paragraph_sub, text)
    text = unhash(text, hashes)
    return text

def convert_lists(text, hashes):
    for style, marker in (('u', '[+*-]'), ('o', r'\d+\.')):
        list_re = re.compile(r"""
            (
                (?:
                    (?:\n|\A)
                    %s
                    (?!\ %s\ )
                    [ ]
                    .+?
                    (?=\Z|(?:\n%s\ )|(?=\n\n[^ \n]))
                )+
            )
        """ % (marker, marker, marker), re.S | re.X)
        for lst in list_re.findall(text):
            items = re.split(r'(?:\n|\A)%s ' % marker, lst)[1:]
            whole_list = ''
            for item in items:
                item = re.sub(r'^ {1,4}', '', item, flags=re.M)
                item = convert_lists(item, hashes)
                item = hash_codeblocks(item, hashes)
                item = blockquote_re.sub(blockquote_sub, item)
                # TODO paragraphs
                whole_list += '<li>{}</li>\n'.format(item)
            whole_list = '<{0}l>\n{1}</{0}l>\n\n'.format(style, whole_list)
            hashed = hash_text(whole_list, 'list')
            hashes[hashed] = whole_list
            start = text.index(lst)
            end = start + len(lst)
            text = text[:start] + '\n' + hashed + text[end:]
    return text

codeblock_re = re.compile(r"""
    (
        (?:(?<=\n)|(?<=\A))
        [ ]{4}.+?\n
        (?:
            \n
           |
            (?:
                [ ]{4}.+?\n
            )
        )*
        (?=\n*(?![ ]{4}))
    )
""", re.S | re.X)
def hash_codeblocks(text, hashes):
    def codeblock_sub(match):
        block = match.group(1).rstrip('\n')
        block = re.sub(r'(?:(?<=\n)|(?<=\A)) {4}', '', block)
        block = '<pre><code>{}</code></pre>'.format(block)
        hashed = hash_text(block, 'pre')
        hashes[hashed] = block
        return hashed + '\n\n'
    return codeblock_re.sub(codeblock_sub, text)

blockquote_re = re.compile(r"""
    (
        (?:(?<=\n)|(?<=\A))
        >.*?\n
        (?:[^\n]+?\n)*
        (?:
            (?:
                >.*?\n
                (?:[^\n]+?\n)*
            )
           |
            \n
        )*
        (?=\n*(?!>))
    )
""", re.S | re.X)
def blockquote_sub(match):
    block = match.group(1).rstrip('\n')
    block = re.sub(r'(?:(?<=\n)|(?<=\A))> ?', '', block)
    return '<blockquote>\n{}\n</blockquote>\n\n'.format(block)

code_re = re.compile(r'(?<!\\)(?P<ticks>`+) ?(.*?) ?(?P=ticks)', re.S)
def hash_code(text, hashes):
    def code_sub(match):
        code = '<code>{}</code>'.format(cgi.escape(match.group(1)))
        hashed = hash_text(code, 'code')
        hashes[hashed] = code
        return hashed
    return code_re.sub(code_sub, text)

link_re = re.compile(r'(?<!\\)(!?)\[(.*?)\]\((.*?)\)', re.S)
def hash_links(text, hashes):
    def link_sub(match):
        is_img = match.group(1) != ''
        content = match.group(2)
        link = match.group(3)
        if is_img:
            result = '<img src="{0}" alt="{1}">'.format(link, content)
        else:
            result = '<a href="{0}">{1}</a>'.format(link, content)
        hashed = hash_text(result, 'link')
        hashes[hashed] = result
        return hashed
    return link_re.sub(link_sub, text)

tag_re = re.compile(r"""<[\w\s:/'"=]+?>""", re.S)
def hash_tags(text, hashes):
    def tag_sub(match):
        hashed = hash_text(match.group(0), 'tag')
        hashes[hashed] = match.group(0)
        return '\n' + hashed + '\n'
    return tag_re.sub(tag_sub, text)

emphasis_markers = r'\*{1,3}|_{1,3}'
emphasis_re = re.compile(
        r'(?<!\\)(?P<emph>%s)(?!\s+)(.*?)(?P=emph)' % emphasis_markers,
        re.S)
def emphasis_sub(match):
    """Substitutes <strong>, <em>, and <strong><em> tags."""
    level = len(match.group(1))
    content = match.group(2)
    if level == 3:
        return '<strong><em>{0}</em></strong>'.format(content)
    elif level == 2:
        return '<strong>{0}</strong>'.format(content)
    elif level == 1:
        return '<em>{0}</em>'.format(content)

escape_re = re.compile(r"""\\(
    \*  |
    `   |
    _   |
    \{  |
    \}  |
    \[  |
    \]  |
    \(  |
    \)  |
    #   |
    \+  |
    -   |
    \.  |
    !
)""", re.X)
def escapes_sub(match):
    return match.group(1)

atx_header_re = re.compile(r'^(#{1,6})\s*(.*)$', re.M)
def atx_header_sub(match):
    """Substitutes atx headers (headers defined using #'s)."""
    level = len(match.group(1))
    title = match.group(2)
    return '<h{0}>{1}</h{0}>'.format(level, title)

setext_header_re = re.compile(r'(?<=\n)(.*?)\n(=+|-+)')
def setext_header_sub(match):
    """Substitutes setext headers (defined with underscores)."""
    title = match.group(1)
    level = 1 if '=' in match.group(2) else 2
    return '<h{0}>{1}</h{0}>'.format(level, title)

avoids = """
    (?:(?:tag|pre|list)-[\da-f]+)|<h(?P<level>[1-6])>.*?</h(?P=level)>
"""
paragraph_re = re.compile(r"""
    (?<=\n\n)
    (?!\n)
    (?!%s)
    (.+?)
    (?=\n\n)
""" % avoids, re.S | re.X)
def paragraph_sub(match):
    return '<p>{}</p>'.format(match.group(0))

hash_re = re.compile("(?:link|tag|list|pre)-[\da-f]+")
def unhash(text, hashes):
    def retrieve_match(match):
        return hashes[match.group(0)]
    while hash_re.search(text):
        text = hash_re.sub(retrieve_match, text)
    return text


retab_re = re.compile(r'(.*?)\t', re.M)
def retab_sub(match):
    before = match.group(1)
    return before + (' ' * (TAB_SIZE - len(before) % TAB_SIZE))
whitespace_re = re.compile(r'^\s+$', re.M)
def handle_whitespace(text):
    text = retab_re.sub(retab_sub, text)
    text = whitespace_re.sub('', text)
    return text

vars_re = re.compile('^~\s*(.*?):\s*(.*)$', re.M)
def store_vars(text):
    """Extracts variables that can be used in templating engines.

    Each variable is defined on a single line in the following way:

        ~ var: text

    The ~ must be at the start of a newline. var can be any sequence of
    characters that does not contain a ":". Likewise, text can be any
    sequence of characters.

    RETURNS:
    dict; variable to value mappings
    """
    variables = {var: value for var, value in vars_re.findall(text)}
    text = vars_re.sub('', text)
    return text, variables





if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        print(process(f.read()))
