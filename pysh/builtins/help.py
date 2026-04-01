def builtin_help(args: list[str]) -> None:
    from pysh.builtins import commands_dict

    command_width = 30
    option_padding = 5

    for name, meta in commands_dict.items():
        arguments = meta.get("arguments", [])
        description = meta.get("description", "")
        options = meta.get("options", [])

        command_text = name
        if arguments:
            command_text += "".join(f" [{arg}]" for arg in arguments)

        print(f"{command_text:<{command_width}} - {description}")

        for option in options:
            flag = option["flag"]
            value = option.get("value")
            flag_description = option.get("description", "")

            option_text = f"{flag} <{value}>" if value else flag
            print(
                f"{'':{option_padding}}{option_text:<{command_width - option_padding}} - {flag_description}"
            )

        print()


COMMAND = {
    "name": "help",
    "function": builtin_help,
    "description": "Display the list of available built-in commands and their descriptions.",
    "arguments": [],
    "options": [],
}
