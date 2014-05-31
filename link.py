import argparse
import os
import re
from markdown import Markdown
import importlib
try:
    import controller
except ImportError:
    controller = None

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
        text, _ = retrieve_and_link(filename, cache)
        if not block:
            block = 'all'
        return cache[filename + ':' + block]
    return link_sub

def cache_blocks(filename, text, cache):
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
    cache_blocks(filename, text, cache)
    return text, cache

def apply_controller(text):
    for regex, sub in controller.regexes:
        text = regex.sub(sub, text)
    return text

header_re = re.compile(r"""
<\s*h([1-6])(?:.*?id=(['"])(.*?)\2.*?)?>
(.*?)
<\s*/\s*h\1\s*>
""", re.X)
def scrape_toc(text):
    return [(h[0], h[2], h[3]) for h in header_re.findall(text)]

def link(filename):
    text, _ = retrieve_and_link(filename, {})
    cache = {}
    converted = Markdown(text)
    for k, v in converted.variables.items():
        cache[k] = v
    if controller:
        text = apply_controller(converted.text)
        for k, v in controller.configs.items():
            cache[k] = v
        toc = scrape_toc(converted.text)
        cache['table-of-contents'] = controller.toc(toc)
    return cache_blocks('', converted.text, cache), cache

##########################
# Command-line Interface #
##########################

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help="Link contents of file")
    parser.add_argument('-d', '--destination', type=str,
                        help="Store result in destination file")
    parser.add_argument('-c', '--cache', action='store_true',
                        help="Show cache keys")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print('File ' + args.file + ' does not exist.')
        exit(1)
    elif not os.path.isfile(args.file):
        print(args.file + ' is not a valid file')
        exit(1)
    result, cache = link(args.file)
    if args.destination:
        with open(args.destination, 'w') as f:
            f.write(result)
        print('Result can be found in ' + args.destination)
    else:
        print('--- BEGIN RESULT ---')
        print(result)
        print('--- END RESULT ---')
    if args.cache:
        print('--- Cache keys ---')
        for k in sorted(cache):
            print(k)

if __name__ == '__main__':
    main()

