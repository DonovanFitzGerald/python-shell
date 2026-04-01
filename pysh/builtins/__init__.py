from .pwd import builtin_pwd
from .exit import builtin_exit
from .cd import builtin_cd
from .procinfo import builtin_procinfo
from .cat import builtin_cat
from .head import builtin_head
from .wc import builtin_wc
from .sysinfo import builtin_sysinfo
from .download import builtin_download
from .alias import builtin_alias
from .alias_store import alias_commands_dict


"""
Built-in commands for pysh.

Built-in commands are handled directly by the shell, rather than by
running an external program. For example, 'cd' must be a built-in
because changing directory needs to affect the shell process itself.

Each built-in is a function that takes a list of string arguments.
Look at builtin_pwd below as a complete example to follow.
"""


def builtin_help(args: list[str]) -> None:
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


alias_commands_dict = {}


commands_dict = {
    "pwd": {
        "function": builtin_pwd,
        "description": "Print the current working directory.",
        "original_name": "pwd",
        "arguments": [],
        "options": [],
    },
    "exit": {
        "function": builtin_exit,
        "description": "Exit the shell.",
        "arguments": [],
        "options": [],
    },
    "cd": {
        "function": builtin_cd,
        "description": "Change the current working directory.",
        "arguments": ["path"],
        "options": [],
    },
    "procinfo": {
        "function": builtin_procinfo,
        "description": "Display information about a process by PID, including status, memory usage, CPU usage, and parent PID.",
        "arguments": ["pid"],
        "options": [],
    },
    "cat": {
        "function": builtin_cat,
        "description": "Read and display the contents of one or more files.",
        "arguments": ["file", "file2 ..."],
        "options": [],
    },
    "head": {
        "function": builtin_head,
        "description": "Display the first lines of a file. Defaults to 10 lines.",
        "arguments": ["file"],
        "options": [
            {
                "flag": "-n",
                "value": "number",
                "description": "Number of lines to display.",
            }
        ],
    },
    "wc": {
        "function": builtin_wc,
        "description": "Count lines, words, and characters in one or more files.",
        "arguments": ["file", "file2 ..."],
        "options": [],
    },
    "sysinfo": {
        "function": builtin_sysinfo,
        "description": "Display a live view of memory, swap, CPU, and top processes.",
        "arguments": [],
        "options": [
            {
                "flag": "--sort",
                "value": "cpu|memory",
                "description": "Sort top processes by CPU or memory usage.",
            },
            {
                "flag": "-i",
                "value": "seconds",
                "description": "Refresh interval in seconds. Default is 2.",
            },
        ],
    },
    "download": {
        "function": builtin_download,
        "description": 'Download URLs from a text file optionally with a download directory ( defaults to "/downloads").',
        "arguments": ["text_file", "download_dir"],
        "options": [
            {
                "flag": "-w",
                "value": "number",
                "description": "Number of worker threads to use.",
            },
        ],
    },
    "help": {
        "function": builtin_help,
        "description": "Display the list of available built-in commands and their descriptions.",
        "arguments": [],
        "options": [],
    },
}

commands_dict = {command["name"]: command for command in commands_list}
