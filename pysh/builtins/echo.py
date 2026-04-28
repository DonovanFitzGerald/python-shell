def builtin_echo(args: list[str]) -> None:
    string = " ".join(args)
    print(string)


COMMAND = {
    "name": "echo",
    "function": builtin_echo,
    "description": "Print the content of the arugments",
    "arguments": ["string", "string2 ..."],
    "options": [],
}
