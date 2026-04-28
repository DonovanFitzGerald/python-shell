from pysh.colors import GREEN, RED, RESET


def builtin_help(args: list[str]) -> None:
    from pysh.builtins import commands_dict

    command_width = 40
    flag_width = 25

    if args:
        command_name = args[0]
        meta = commands_dict.get(command_name)

        if meta is None:
            print(f"Unknown command: {command_name}")
            return

        arguments = meta.get("arguments", [])
        options = meta.get("options", [])
        description = meta.get("description", "")

        usage = command_name
        if arguments:
            usage += "".join(f" [{arg}]" for arg in arguments)

        print(f"{description}")
        print(f"{'-':-^60}")
        print(f"{usage}")
        print(f"{'-':-^60}")

        if options:
            for option in options:
                flag = option["flag"]
                value = option.get("value")
                flag_description = option.get("description", "")

                flag_text = f"{flag} <{value}>" if value else flag
                print(f"{flag_text:<{flag_width}} - {flag_description}")

        return

    for name, meta in commands_dict.items():
        arguments = meta.get("arguments", [])
        description = meta.get("description", "")

        command_text = name

        print(f"{command_text:<{command_width}} - {description}")


COMMAND = {
    "name": "help",
    "function": builtin_help,
    "description": "Display available commands or detailed help for a specific command.",
    "arguments": ["command"],
    "options": [],
}
