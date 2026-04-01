import sys


def builtin_exit(args) -> None:
    """
    Exit the shell.

    Raises SystemExit which is caught by the main loop in shell.py
    to break out of the loop cleanly.
    """
    sys.exit(0)


COMMAND = {
    "name": "exit",
    "function": builtin_exit,
    "description": "Exit the shell.",
    "arguments": [],
    "options": [],
}
