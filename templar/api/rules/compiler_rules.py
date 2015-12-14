from templar import markdown
from templar.api.rules import core

class MarkdownToHtmlRule(core.Rule):
    def __init__(self, src=r'\.md', dst=r'\.html'):
        super().__init__(src, dst)

    def apply(self, content):
        # TODO(wualbert): rewrite markdown parser, or use a library.
        return markdown.convert(content)

