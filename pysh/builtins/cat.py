import os

# - `cat <file> [file2 ...]`: read and display the contents of one or more files. Handle missing files with a clear error message.


def builtin_cat(args: list[str]) -> None:
    for arg in args:
        path = arg
        if os.path.isfile(path):
            with open(path, "r") as f:
                contents = f.read()
                print(contents)
        else:
            print(f'pysh: "{path}" file not found')


COMMAND = {
    "name": "cat",
    "function": builtin_cat,
    "description": "Read and display the contents of one or more files.",
    "arguments": ["file", "file2 ..."],
    "options": [],
}
