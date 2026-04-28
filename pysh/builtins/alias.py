alias_commands_dict: dict[str, str] = {}


def builtin_alias(args: list[str]) -> None:
    if not args:
        for name, command in alias_commands_dict.items():
            print(f'{name} = "{command}"')
        return

    definition = " ".join(args)

    name, command = definition.split("=", 1)
    name = name.strip()
    command = command.strip()

    if (command.startswith('"') and command.endswith('"')) or (
        command.startswith("'") and command.endswith("'")
    ):
        command = command[1:-1]

    alias_commands_dict[name] = command


COMMAND = {
    "name": "alias",
    "function": builtin_alias,
    "description": "Define or list command aliases.",
    "arguments": [],
    "options": [],
}
