import re
from markdown import convert
import importlib

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
        text, _ = retrieve_and_link(filename + '.md', cache)
        if not block:
            block = 'all'
        return cache[filename + ':' + block]
    return link_sub

def cache_blocks(filename, text, cache):
    filename = filename.replace('.md', '')
    while block_re.search(text):
        for name, contents in block_re.findall(text):
            contents = cache_blocks(filename, contents, cache)
            cache[filename + ':' + name] = contents
        text = block_re.sub(lambda m: m.group(2), text)
    cache[filename + ':all'] = text
    return text

def retrieve_and_link(filename, cache):
    with open(filename, 'r') as f:
        text = f.read()
    text = include_re.sub(make_link_sub(cache), text)
    text = cache_blocks(filename, text, cache)
    return text, cache

def apply_controller(text, controller):
    for regex, sub in controller.regexes:
        text = regex.sub(sub, text)
    return text

def link(filename, controllers):
    text, _ = retrieve_and_link(filename, {})
    cache = {}
    text, variables = convert(text)
    for k, v in variables.items():
        cache[k] = v
    for mod in controllers:
        controller = importlib.import_module(mod)
        text = apply_controller(text, controller)
        for k, v in controller.configs.items():
            cache[k] = v
    return cache_blocks('', text, cache), cache

if __name__ == '__main__':
    import sys
    text, cache = link(sys.argv[1])
    print(text)

