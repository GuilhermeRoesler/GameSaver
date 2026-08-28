from colorama import Fore, Style, init
init()

COLORS = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "CYAN": Fore.CYAN,
        "MAGENTA": Fore.MAGENTA,
        "WHITE": Fore.WHITE,
        "BLACK": Fore.BLACK,
    }

def printc(color, content) -> None:
    color_code = COLORS.get(color.upper(), Fore.WHITE)
    print(f"{color_code}{content}{Style.RESET_ALL}")

def colored(color: str, content: str) -> str:
    color_code = COLORS.get(color.upper(), Fore.WHITE)
    return f"{color_code}{content}{Style.RESET_ALL}"

def colored_multi(colors: list, contents: list) -> str:
    if len(colors) != len(contents):
        raise ValueError('The color and content arrays must be the same size.')
    
    result = ''
    for color, content in zip(colors, contents):
        result += colored(color, content)
    
    return result