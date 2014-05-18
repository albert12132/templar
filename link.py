# link markdown
# convert markdown
# apply postprocessing (for special tags)
# create dictionary with variable and block mappings

import re

include_re = re.compile(r'<\s*include\s+(.+?)(?::(.+?))?\s*>')
block_re = re.compile(r"""
    <\s*block\s+(?P<name>.+?)\s*>
    (.*?)
    </\s*block\s+(?P=name)\s*>
""", re.S | re.X)

def make_link_sub(cache):
    def link_sub(match):
        filename = match.group(1)
        block = match.group(2)
        retrieve_and_link(filename + '.md', cache)
        if not block:
            block = 'all'
        return cache[filename + ':' + block]
    return link_sub

def cache_blocks(filename, text, cache):
    filename = filename.replace('.md', '')
    cache[filename + ':all'] = text
    while block_re.search(text):
        for name, contents in block_re.findall(text):
            contents = cache_blocks(filename, contents, cache)
            cache[filename + ':' + name] = contents
        text = block_re.sub(lambda m: m.group(1), text)
    return text

def retrieve_and_link(filename, cache):
    with open(filename, 'r') as f:
        text = f.read()
    text = include_re.sub(make_link_sub(cache), text)
    text = cache_blocks(filename, text, cache)
    return text

if __name__ == '__main__':
    import sys
    print(retrieve_and_link(sys.argv[1], {}))

