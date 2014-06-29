import re

class TableOfContents:
    def __init__(self, text):
        self._text = text

    @property
    def pattern(self):
        raise NotImplementedError

    def translate(self, match):
        raise NotImplementedError

    def build(self, lst):
        raise NotImplementedError

    @property
    def result(self):
        lst = [self.translate(match)
               for match in re.finditer(self.pattern, self._text)]
        self._result = self.build(lst)
        return self._result

    def __repr__(self):
        return self._result
