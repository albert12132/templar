import templar.utils.core as core
import re

#################
# HTML escaping #
#################

_re_unescape = re.compile(r"\&(#?)(x?)(\w+);")

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

################
# HTML Escapes #
################

_html_escapes = {
    'quot': '"',
    'amp': '&',
    'apos': '',
    'lt': '<',
    'gt': '>',
    'nbsp': '',
    'iexcl': '¡',
    'cent': '¢',
    'pound': '£',
    'curren': '¤',
    'yen': '¥',
    'brvbar': '¦',
    'sect': '§',
    'uml': '¨',
    'copy': '©',
    'ordf': 'ª',
    'laquo': '«',
    'not': '¬',
    'shy': '',
    'reg': '®',
    'macr': '¯',
    'deg': '°',
    'plusmn': '±',
    'sup2': '²',
    'sup3': '³',
    'acute': '´',
    'micro': 'µ',
    'para': '¶',
    'middot': '·',
    'cedil': '¸',
    'sup1': '¹',
    'ordm': 'º',
    'raquo': '»',
    'frac14': '¼',
    'frac12': '½',
    'frac34': '¾',
    'iquest': '¿',
    'Agrave': 'À',
    'Aacute': 'Á',
    'Acirc': 'Â',
    'Atilde': 'Ã',
    'Auml': 'Ä',
    'Aring': 'Å',
    'AElig': 'Æ',
    'Ccedil': 'Ç',
    'Egrave': 'È',
    'Eacute': 'É',
    'Ecirc': 'Ê',
    'Euml': 'Ë',
    'Igrave': 'Ì',
    'Iacute': 'Í',
    'Icirc': 'Î',
    'Iuml': 'Ï',
    'ETH': 'Ð',
    'Ntilde': 'Ñ',
    'Ograve': 'Ò',
    'Oacute': 'Ó',
    'Ocirc': 'Ô',
    'Otilde': 'Õ',
    'Ouml': 'Ö',
    'times': '×',
    'Oslash': 'Ø',
    'Ugrave': 'Ù',
    'Uacute': 'Ú',
    'Ucirc': 'Û',
    'Uuml': 'Ü',
    'Yacute': 'Ý',
    'THORN': 'Þ',
    'szlig': 'ß',
    'agrave': 'à',
    'aacute': 'á',
    'acirc': 'â',
    'atilde': 'ã',
    'auml': 'ä',
    'aring': 'å',
    'aelig': 'æ',
    'ccedil': 'ç',
    'egrave': 'è',
    'eacute': 'é',
    'ecirc': 'ê',
    'euml': 'ë',
    'igrave': 'ì',
    'iacute': 'í',
    'icirc': 'î',
    'iuml': 'ï',
    'eth': 'ð',
    'ntilde': 'ñ',
    'ograve': 'ò',
    'oacute': 'ó',
    'ocirc': 'ô',
    'otilde': 'õ',
    'ouml': 'ö',
    'divide': '÷',
    'oslash': 'ø',
    'ugrave': 'ù',
    'uacute': 'ú',
    'ucirc': 'û',
    'uuml': 'ü',
    'yacute': 'ý',
    'thorn': 'þ',
    'yuml': 'ÿ',
    'OElig': 'Œ',
    'oelig': 'œ',
    'Scaron': 'Š',
    'scaron': 'š',
    'Yuml': 'Ÿ',
    'fnof': 'ƒ',
    'circ': 'ˆ',
    'tilde': '˜',
    'Alpha': 'Α',
    'Beta': 'Β',
    'Gamma': 'Γ',
    'Delta': 'Δ',
    'Epsilon': 'Ε',
    'Zeta': 'Ζ',
    'Eta': 'Η',
    'Theta': 'Θ',
    'Iota': 'Ι',
    'Kappa': 'Κ',
    'Lambda': 'Λ',
    'Mu': 'Μ',
    'Nu': 'Ν',
    'Xi': 'Ξ',
    'Omicron': 'Ο',
    'Pi': 'Π',
    'Rho': 'Ρ',
    'Sigma': 'Σ',
    'Tau': 'Τ',
    'Upsilon': 'Υ',
    'Phi': 'Φ',
    'Chi': 'Χ',
    'Psi': 'Ψ',
    'Omega': 'Ω',
    'alpha': 'α',
    'beta': 'β',
    'gamma': 'γ',
    'delta': 'δ',
    'epsilon': 'ε',
    'zeta': 'ζ',
    'eta': 'η',
    'theta': 'θ',
    'iota': 'ι',
    'kappa': 'κ',
    'lambda': 'λ',
    'mu': 'μ',
    'nu': 'ν',
    'xi': 'ξ',
    'omicron': 'ο',
    'pi': 'π',
    'rho': 'ρ',
    'sigmaf': 'ς',
    'sigma': 'σ',
    'tau': 'τ',
    'upsilon': 'υ',
    'phi': 'φ',
    'chi': 'χ',
    'psi': 'ψ',
    'omega': 'ω',
    'thetasym': 'ϑ',
    'upsih': 'ϒ',
    'piv': 'ϖ',
    'ensp': '',
    'emsp': '',
    'thinsp': '',
    'zwnj': '',
    'zwj': '',
    'lrm': '',
    'rlm': '',
    'ndash': '–',
    'mdash': '—',
    'lsquo': '‘',
    'rsquo': '’',
    'sbquo': '‚',
    'ldquo': '“',
    'rdquo': '”',
    'bdquo': '„',
    'dagger': '†',
    'Dagger': '‡',
    'bull': '•',
    'hellip': '…',
    'permil': '0',
    'prime': '′',
    'Prime': '″',
    'lsaquo': '‹',
    'rsaquo': '›',
    'oline': '‾',
    'frasl': '⁄',
    'euro': '€',
    'image': 'ℑ',
    'weierp': '℘',
    'real': 'ℜ',
    'trade': '™',
    'alefsym': 'ℵ',
    'larr': '←',
    'uarr': '↑',
    'rarr': '→',
    'darr': '↓',
    'harr': '↔',
    'crarr': '↵',
    'lArr': '⇐',
    'uArr': '⇑',
    'rArr': '⇒',
    'dArr': '⇓',
    'hArr': '⇔',
    'forall': '∀',
    'part': '∂',
    'exist': '∃',
    'empty': '∅',
    'nabla': '∇',
    'isin': '∈',
    'notin': '∉',
    'ni': '∋',
    'prod': '∏',
    'sum': '∑',
    'minus': '−',
    'lowast': '∗',
    'radic': '√',
    'prop': '∝',
    'infin': '∞',
    'ang': '∠',
    'and': '∧',
    'or': '∨',
    'cap': '∩',
    'cup': '∪',
    'int': '∫',
    'there4': '∴',
    'sim': '∼',
    'cong': '≅',
    'asymp': '≈',
    'ne': '≠',
    'equiv': '≡',
    'le': '≤',
    'ge': '≥',
    'sub': '⊂',
    'sup': '⊃',
    'nsub': '⊄',
    'sube': '⊆',
    'supe': '⊇',
    'oplus': '⊕',
    'otimes': '⊗',
    'perp': '⊥',
    'sdot': '⋅',
    'vellip': '⋮',
    'lceil': '⌈',
    'rceil': '⌉',
    'lfloor': '⌊',
    'rfloor': '⌋',
    'lang': '〈',
    'rang': '〉',
    'loz': '◊',
    'spades': '♠',
    'clubs': '♣',
    'hearts': '♥',
    'diams': '♦',
}

_html_escapes_reverse = {v: k for k, v in _html_escapes.items()}

