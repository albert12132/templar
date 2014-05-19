import re
import controller
from markdown import convert

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
    text = apply_controller(text)
    return text

def retrieve_and_link(filename, cache):
    with open(filename, 'r') as f:
        text = f.read()
    text = include_re.sub(make_link_sub(cache), text)
    text = cache_blocks(filename, text, cache)
    return text, cache

def apply_controller(text):
    for regex, sub in controller.regexes:
        text = regex.sub(sub, text)
    return text

def link(filename):
    text, cache = retrieve_and_link(filename, {})
    text, variables = convert(text)
    for k, v in variables.items():
        cache[k] = v
    return text, cache

if __name__ == '__main__':
    import sys
    text, cache = link(sys.argv[1])
    print(text)
    print(cache)


