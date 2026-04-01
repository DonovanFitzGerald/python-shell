import os

# TODO: Part 1:
# - `cd <path>`: change the current working directory


def builtin_cd(args: list[str]) -> None:
    """
    Change the current working directory.
    """
    path = args[0]
    os.chdir(path)


COMMAND = {
    "name": "cd",
    "function": builtin_cd,
    "description": "Change the current working directory.",
    "arguments": ["path"],
    "options": [],
}
