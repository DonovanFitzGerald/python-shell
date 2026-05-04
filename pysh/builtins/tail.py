import os

# - `head [-n N] <file>`: display the first _N_ lines of a file (default: 10)


def builtin_tail(args: list[str]) -> None:
    """
    Displays the first _N_ lines of a file
    """
    numLines = 10
    for [index, string] in enumerate(args):
        if string == "-n":
            index
            args.pop(index)
            numLines = int(args[index])
            args.pop(index)
            break

    path = args[0]
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()[-numLines:]
            for line in lines:
                print(line)
    else:
        print(f'pysh: "{path}" file not found')


COMMAND = {
    "name": "tail",
    "function": builtin_tail,
    "description": "Display the last lines of a file. Defaults to 10 lines.",
    "arguments": ["file"],
    "options": [
        {
            "flag": "-n",
            "value": "number",
            "description": "Number of lines to display.",
        }
    ],
}
