RED = "0;31"
GREEN = "0;32"
YELLOW = "0;33"
BLUE = "0;34"
GRAY = "0;37"


def _ansicolorize(text, color_code):
    return "\033[{}m{}\033[0m".format(color_code, text)


def color_print(text, color_code):
    if color_code:
        print(_ansicolorize(text, color_code))
    else:
        print(text)
