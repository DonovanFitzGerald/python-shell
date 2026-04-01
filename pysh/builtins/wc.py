import os

# - `wc <file> [file2 ...]`: count and display the number of lines, words, and characters in one or more files. Display totals when multiple files are given.


def builtin_wc(args: list[str]) -> None:
    """
    Counts and displays the number of lines, words, and characters in one or more files. Display totals when multiple files are given
    """
    line_count = 0
    word_count = 0
    char_count = 0
    for arg in args:
        path = arg
        if os.path.isfile(path):
            with open(path, "r") as f:
                lines = f.readlines()
                line_count += len(lines)
                word_count += sum(len(line.split()) for line in lines)
                char_count += sum(len(line) for line in lines)
        else:
            print(f'pysh: "{path}" file not found')
    print(f"Lines: {line_count}")
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")


COMMAND = {
    "name": "wc",
    "function": builtin_wc,
    "description": "Count lines, words, and characters in one or more files.",
    "arguments": ["file", "file2 ..."],
    "options": [],
}
