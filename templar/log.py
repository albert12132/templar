from colorama import init, Fore, Back, Style

init()

def info(text, quiet=False):
    if not quiet:
        print(Fore.GREEN + Style.BRIGHT + 'INFO: ' + str(text) \
                + Style.RESET_ALL)

def warn(text, quiet=False):
    if not quiet:
        print(Fore.RED + Style.BRIGHT + 'WARN: '  + str(text) \
                + Style.RESET_ALL)

def log(text, quiet=False):
    if not quiet:
        print(text)
