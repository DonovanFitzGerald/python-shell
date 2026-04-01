import os


def builtin_pwd(args) -> None:
    """
    Print the current working directory.

    Uses os.getcwd() which asks the operating system for the current
    working directory of this process.

    Example usage:
        pysh /home/student $ pwd
        /home/student
    """
    print(os.getcwd())


COMMAND = {
    "name": "pwd",
    "function": builtin_pwd,
    "description": "Print the current working directory.",
    "arguments": [],
    "options": [],
}
