from templar.api.rules import core

import re

class HtmlTableOfContents(core.VariableRule):
    """A rule that constructs a table of contents based on all HTML headers found in the
    content.

    This rule adds a variable called "table_of_contents". By default, this rule only applies
    to destinations with a .html extension.
    """
    header_regex = re.compile(r"""
        <\s*h([1-6])        # \1 is the header level
        (?:
            .*?         # attributes
            id=(['"])   # \2 is the quote
            (.*?)       # \3 is the actual id
            \2          # closing quote
            .*?         # attributes
        )?>
        (.*?)           # \4 is the header title
        <\s*/\s*
            h\1         # closing header tag
        \s*>
    """, re.X)

    def __init__(self, src=None, dst=r'.*\.html'):
        super().__init__(src, dst)


    def extract(self, content):
        matches = re.findall(self.header_regex, content)
        return {'table_of_contents': '\n'.join(self._build_list(matches))}

    def _build_list(self, matches, current_level='1'):
        """Builds an unordered HTML list out of the list of matches, stopping at the first match
        that is smaller than current_level (e.g. h1 < h2).

        This method uses mutual recursion with _build_list_items and expects _build_list_items to
        delete matches as it processes them.

        This method uses string comparison when comparing levels, taking advantage of the fact that
        ordering single-digit ASCII numerical character is the same as ordering single-digit
        integers. By default, the current_level is '1' so that it can process all headers.

        For efficiency reasons, this method doesn't concatenate the lines; callers of this method
        should perform the join after the call.
        """
        lines = ['<ul>']
        while matches and current_level <= matches[0][0]:
            # Build list items and indent each line by two spaces.
            lines.extend('  ' + line for line in self._build_list_items(matches))
        lines.append('</ul>')
        return lines


    def _build_list_items(self, matches):
        """Returns the HTML list items for the next matches that have a larger (or equal) header
        compared to the first header's level.

        This method mutatively removes elements from the front of matches as it processes each
        element. This method assumes matches contains at least one match.

        PARAMETERS:
        matches -- list of tuples; each tuple corresponds to the groups matched by the header_regex.

        RETURNS:
        list of str; the table of contents as a list of lines.
        """
        assert len(matches) > 0, "Should be at least one match, by assumption"

        lines = []
        current_level = matches[0][0]
        while matches and current_level <= matches[0][0]:
            level, _, tag_id, title = matches[0]
            if current_level < level:
                lines.extend(self._build_list(matches, level))
                continue

            if tag_id:
                lines.append('<li><a href="#{0}">{1}</a></li>'.format(tag_id, title))
            else:
                lines.append('<li>{0}</li>'.format(title))
            matches.pop(0)
        return lines

