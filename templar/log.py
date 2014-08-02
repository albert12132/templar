from colorama import init, Fore, Back, Style

init()

def info(text, quiet=False):
    if not quiet:
        print(Fore.GREEN + Style.BRIGHT + 'INFO: ' + text \
                + Style.RESET_ALL)

def warn(text, quiet=False):
    if not quiet:
        print(Fore.RED + Style.BRIGHT + 'WARN: '  + text \
                + Style.RESET_ALL)

def log(text, quiet=False):
    if not quiet:
        print(text)
