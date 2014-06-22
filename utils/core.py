import re

class TableOfContents:
    def __init__(self, text):
        lst = [self.translate(match)
               for match in re.finditer(self.pattern, text)]
        self._result = self.build(lst)

    @property
    def pattern(self):
        raise NotImplementedError

    def translate(self, match):
        raise NotImplementedError

    def build(self, lst):
        raise NotImplementedError

    @property
    def result(self):
        return self._result

    def __repr__(self):
        return self._result

