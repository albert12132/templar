import re
from random import randint
from hashlib import sha1
import html

TAB_SIZE = 4
SALT = bytes(randint(0, 1000000))
def hash_text(s, label):
    return label + '-' + sha1(SALT + s.encode("utf-8")).hexdigest() + '-' + label

def convert(text):
    text, variables = store_vars(text)
    text, refs = store_references(text)
    text = handle_whitespace(text)
    hashes = {}
    text = hash_blocks(text, hashes)
    text = convert_lists(text, hashes)
    text = hash_blockquote(text, hashes)
    text = hash_codeblocks(text, hashes)
    text = hash_code(text, hashes)
    text = hash_links(text, hashes)
    text = hash_ref_links(text, hashes, refs)
    text = hash_tags(text, hashes)
    text = hr_re.sub(hr_sub, text)
    text = emphasis_re.sub(emphasis_sub, text)
    text = escape_re.sub(escapes_sub, text)
    text = auto_escape_re.sub(auto_escape_sub, text)
    text = atx_header_re.sub(atx_header_sub, text)
    text = setext_header_re.sub(setext_header_sub, text)
    text = paragraph_re.sub(paragraph_sub, text)
    text = unhash(text, hashes)
    text = slug_re.sub(slug_sub, text)
    return text, variables

retab_re = re.compile(r'(.*?)\t', re.M)
def retab_sub(match):
    before = match.group(1)
    return before + (' ' * (TAB_SIZE - len(before) % TAB_SIZE))
whitespace_re = re.compile(r'^\s+$', re.M)
def handle_whitespace(text):
    text = retab_re.sub(retab_sub, text)
    text = whitespace_re.sub('', text).strip()
    return text

vars_re = re.compile('^~\s+(.*?):\s*(.*?)$', re.M)
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

references_re = re.compile(r"""
    \n[ ]{0,3}
    \[([^\n]+?)\]:
    [ \t]+
    (.+?)
    \s
    (?:
        [ \t]*\n?[ \t]*
        (?P<title>["'])(.*?)(?P=title)
    )?
""", re.X | re.S)
def store_references(text):
    refs = {}
    for ref_id, link, _, title in references_re.findall(text):
        ref_id = re.sub(r'<(.*?)>', r'\1', ref_id).lower().strip()
        refs[ref_id] = (link, title)
    text = references_re.sub('', text)
    return text, refs


block_elements = "blockquote|div|form|hr|noscript|ol|p|pre|table"
block_re = re.compile(r"""
    (?:(?<=\n)|(?<=\A))
    <\s*(?P<tag>%s)\s?.*?>
    .*?
    \n<\s*/\s*(?P=tag)\s?.*?>
""" % block_elements, re.S | re.X)
def hash_blocks(text, hashes):
    def sub(match):
        block = match.group(0)
        hashed = hash_text(block, 'block')
        hashes[hashed] = block
        return hashed
    return block_re.sub(sub, text)



def convert_lists(text, hashes):
    for style, marker in (('u', '[+*-]'), ('o', r'\d+\.')):
        list_re = re.compile(r"""
            (
                (?:(?<=\n)|(?<=\A))
                [ ]{0,3}
                %s
                (?!\ %s\ )
                [ ].+?(?=\n\n(?![ ]{4})|\n*\Z)
                (?:
                    (?:
                        [ ]{0,3}
                        %s
                        (?!\ %s\ )
                        [ ].+?(?=\n\n(?![ ]{4})|\n*\Z)
                    )
                   |
                    \n
                )*
            )
        """ % (marker, marker, marker, marker), re.S | re.X)
        for lst in list_re.findall(text):
            items = re.split(r'(?:\n|\A) {0,3}%s ' % marker, lst)[1:]
            whole_list = ''
            for item in items:
                item = re.sub(r'^ {1,4}', '', item, flags=re.M)
                item = convert(item)[0]
                match = re.match('<p>(.*?)</p>', item, flags=re.S)
                if match and match.group(0) == item.strip():
                    item = match.group(1)
                whole_list += '<li>{}</li>\n'.format(item)
            whole_list = '<{0}l>\n{1}\n</{0}l>'.format(
                    style,
                    re.sub('^', '  ', whole_list.strip(), flags=re.M))
            hashed = hash_text(whole_list, 'list')
            hashes[hashed] = whole_list
            start = text.index(lst)
            end = start + len(lst)
            text = text[:start] + '\n' + hashed + '\n\n' + text[end:]
    return text

codeblock_re = re.compile(r"""
    (
        (?:(?<=\n)|(?<=\A))
        [ ]{4}.+?(?:\n|\Z)
        (?:
            \n
           |
            (?:
                [ ]{4}.+?(?:\n|\Z)
            )
        )*
        (?=(?:\n*(?![ ]{4}))|\Z)
    )
""", re.S | re.X)
def hash_codeblocks(text, hashes):
    def codeblock_sub(match):
        block = match.group(1).rstrip('\n')
        block = re.sub(r'(?:(?<=\n)|(?<=\A)) {4}', '', block)
        block = html.escape(block)
        block = '<pre><code>{}</code></pre>'.format(block)
        hashed = hash_text(block, 'pre')
        hashes[hashed] = block
        return '\n' + hashed + '\n\n'
    return codeblock_re.sub(codeblock_sub, text)

blockquote_re = re.compile(r"""
    (
        (?:(?<=\n)|(?<=\A))
        >[ ].*?(?=\n\n|\n*\Z)
        (?:
            (?:
                >[ ].*?(?=\n\n|\n*\Z)
            )
           |
            \n
        )*
    )
""", re.S | re.X)
def hash_blockquote(text, hashes):
    def blockquote_sub(match):
        block = match.group(1)
        block = re.sub(r'(?:(?<=\n)|(?<=\A))> ', '', block)
        block = convert(block)[0]
        block = '<blockquote>\n{}\n</blockquote>\n'.format(block)
        hashed = hash_text(block, 'blockquote')
        hashes[hashed] = block
        return hashed + '\n\n'
    return blockquote_re.sub(blockquote_sub, text)

code_re = re.compile(r'(?<!\\)(?P<ticks>`+) ?(.*?) ?(?P=ticks)', re.S)
def hash_code(text, hashes):
    def code_sub(match):
        code = '<code>{}</code>'.format(html.escape(match.group(2)))
        hashed = hash_text(code, 'code')
        hashes[hashed] = code
        return hashed
    return code_re.sub(code_sub, text)

link_re = re.compile(r"""
(?<!\\)
(!?)
\[(.*?)\]
\(
    \s*
    (.*?)
    (\s*(?P<quote>["']).+?(?P=quote))?
    \s*
\)
""", re.X | re.S)
def hash_links(text, hashes):
    def link_sub(match):
        is_img = match.group(1) != ''
        content = match.group(2)
        link = match.group(3)
        title = match.group(4)
        if title:
            title = ' title={0}'.format(title.strip())
        else:
            title = ''
        if is_img:
            result = '<img src="{0}" alt="{1}"{2}>'.format(
                    link, content, title)
        else:
            result = '<a href="{0}"{2}>{1}</a>'.format(link, content,
                    title)
        hashed = hash_text(result, 'link')
        hashes[hashed] = result
        return hashed
    return link_re.sub(link_sub, text)

link_ref_re = re.compile(r"""
(?<!\\)
(!?)
\[(.*?)\]
\[
    (.*?)
\]
""", re.X | re.S)
def hash_ref_links(text, hashes, refs):
    def sub(match):
        is_img = match.group(1) != ''
        content = match.group(2)
        ref = match.group(3).strip().lower()
        if not ref:
            ref = content.strip().lower()
        link, title = refs[ref]
        if title:
            title = ' title="{0}"'.format(title)
        if is_img:
            result = '<img src="{0}" alt="{1}"{2}>'.format(
                    link, content, title)
        else:
            result = '<a href="{0}"{2}>{1}</a>'.format(link, content,
                    title)
        hashed = hash_text(result, 'link')
        hashes[hashed] = result
        return hashed
    return link_ref_re.sub(sub, text)

tag_re = re.compile(r"""<[\w\s:/'"=]+?>""", re.S)
def hash_tags(text, hashes):
    def tag_sub(match):
        hashed = hash_text(match.group(0), 'tag')
        hashes[hashed] = match.group(0)
        return hashed
    return tag_re.sub(tag_sub, text)

hr_re = re.compile(r"\n\n(\*{3,}|-{3,})\n\n", re.S)
def hr_sub(match):
    return '\n\n<hr/>\n\n'

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

auto_escape_re = re.compile(r"&(?!#[xX]?[0-9a-fA-F]+)")
def auto_escape_sub(match):
    return html.escape(match.group(0))

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

atx_header_re = re.compile(r'^(#{1,6})\s*(.*?)\s*#*$', re.M)
def atx_header_sub(match):
    """Substitutes atx headers (headers defined using #'s)."""
    level = len(match.group(1))
    title = match.group(2)
    return '<h{0}>{1}</h{0}>'.format(level, title)

setext_header_re = re.compile(r'(?:(?<=\n)|(?<=\A))(.*?)\n(=+|-+)(?=\n)')
def setext_header_sub(match):
    """Substitutes setext headers (defined with underscores)."""
    title = match.group(1)
    level = 1 if '=' in match.group(2) else 2
    return '<h{0}>{1}</h{0}>'.format(level, title)

avoids = """
    (?:(?P<hash>blockquote|block|tag|pre|list)-[\da-f]+-(?P=hash))|<h(?P<level>[1-6])>.*?</h(?P=level)>
"""
paragraph_re = re.compile(r"""
    (?:(?<=\n\n)|(?<=\A))
    (?!\n)
    (?!%s)
    (.+?)
    (?:(?=\n\n)|(?=\n*\Z))
""" % avoids, re.S | re.X)
def paragraph_sub(match):
    return '<p>{}</p>'.format(match.group(0))

hash_re = re.compile(r"(?P<label>blockquote|block|code|link|tag|list|pre)-[\da-f]+-(?P=label)")
pre_re = re.compile(r"""
    (?P<space>[ ]*)
    <pre>
    .*?
    </pre>
""", re.S | re.X)
def unhash(text, hashes):
    def retrieve_match(match):
        return hashes[match.group(0)]
    while hash_re.search(text):
        text = hash_re.sub(retrieve_match, text)
    text = pre_re.sub(lambda m: re.sub('^' + m.group(1), '', m.group(0), flags=re.M), text)
    return text

slug_re = re.compile(r"<\s*(?P<level>h[0-6])\s*>\s*(.*?)\s*<\s*/\s*(?P=level)\s*>")
def slug_sub(match):
    level = match.group(1)
    title = match.group(2)
    slug = title.lower()
    slug = slug.replace(' ', '-')
    slug = re.sub(r'<.+?>|[^\w-]', '', slug)
    return '<{0} id="{1}">{2}</{0}>'.format(level, slug, title)


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        print(convert(f.read())[0])
        # convert(f.read())[0]
