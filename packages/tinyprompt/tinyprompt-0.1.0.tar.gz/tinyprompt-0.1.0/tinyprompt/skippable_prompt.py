import sys
import textwrap
from functools import wraps

from .colors import GREEN, RED, YELLOW, color_print


def skippable(name, color=True):
    def inner_decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            color_print("\n\n  Step: {}\n".format(name.upper()), GREEN)
            if func.__doc__:
                color_print(textwrap.indent(func.__doc__, "    "), YELLOW)
            answer = _do_prompt(
                "Run this? ([y]es / [s]kip / [q]uit) ",
                ["y", "yes", "s", "skip", "q", "quit"],
            )
            if answer in ("y", "yes"):
                color_print("running...", YELLOW)
                return func(*args, **kwargs)
            elif answer in ("s", "skip"):
                color_print("skipping...", YELLOW)
                return None
            else:  # quit
                color_print("quitting...", YELLOW)
                sys.exit(1)

        return decorated

    return inner_decorator


def _do_prompt(text, allowed=("y", "n")):
    while True:
        print(text, end="")
        answer = input().lower()
        if answer not in allowed:
            color_print(
                'Could not handle "{}". Please answer one of {}'.format(
                    answer, list(allowed)
                ),
                RED,
            )
        else:
            return answer
