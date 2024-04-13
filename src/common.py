import os
import pathlib

FILES_DIR = pathlib.Path(__file__).parent.parent / "FILES"

ASSETS_PATH = pathlib.Path(__file__).parent.parent / "assets"


class Colors():
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


def cprint(string: str, color: Colors):
    print_this = f'\033[1;3{color}m' + string + '\033[0m'

    if os.getenv("DEBUG", True):
        print(print_this)
    else:
        pass
