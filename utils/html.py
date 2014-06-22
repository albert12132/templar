import utils.core as core
import re

#################
# HTML escaping #
#################

_re_unescape = re.compile(r"\&(#?)(x?)(\w+);")

_html_escapes = {
}

_html_escapes_reverse = {v: k for k, v in _html_escapes.items()}

def _unescape_sub(match):
    is_code = match.group(1) != ''
    is_hex = match.group(2) != ''
    entity = match.group(3)
    if not is_code:
        return _html_escapes[entity]
    elif is_hex:
        return chr(int(entity, 16))
    return chr(int(entity))

def unescape(text):
    """Unescapes hex, decimal, and entity escapes in HTML."""
    return _re_unescape.sub(_unescape_sub, text)

def hex_escape(text):
    """Entirely hex escape all characters contained within text.
    The text will be unescaped first"""
    text = unescape(text)
    return ''.join('&#{};'.format(hex(ord(c))[1:]) for c in text)

def decimal_escape(text):
    """Entirely decimal escape all characters contained within text.
    The text will be unescaped first"""
    text = unescape(text)
    return ''.join('&#{};'.format(ord(c)) for c in text)

def entity_escape(text):
    """Escape HTML entities."""
    return ''.join(_html_escapes_reverse.get(c, c) for c in text)


#############################
# Table of Contents Parsers #
#############################

class HeaderParser(core.TableOfContents):
    REGEX = re.compile(r"""
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

    @property
    def pattern(self):
        return self.REGEX

    def translate(self, match):
        return match.group(1), match.group(3), match.group(4)

    def build(self, lst):
        if not lst:
            return ''
        return self._help_build(lst[0][0], lst)

    def _help_build(self, cur, lst):
        if not lst:
            return ''
        text = []
        while lst and lst[0][0] >= cur:
            level, tag, title = lst[0]
            if cur == level:
                text.append('<li><a href="#{0}">{1}</a></li>'.format(
                    tag, title))
                lst.pop(0)
            else:
                text.append(self._help_build(level, lst))
        if text:
            return '<ul>\n  ' + '\n  '.join(text) + '\n</ul>\n'

