from .alias import COMMAND as alias_command, alias_commands_dict
from .cat import COMMAND as cat_command
from .cd import COMMAND as cd_command
from .download import COMMAND as download_command
from .echo import COMMAND as echo_command
from .exit import COMMAND as exit_command
from .head import COMMAND as head_command
from .help import COMMAND as help_command
from .procinfo import COMMAND as procinfo_command
from .pwd import COMMAND as pwd_command
from .sysinfo import COMMAND as sysinfo_command
from .wc import COMMAND as wc_command
from .tail import COMMAND as tail_command

"""
Built-in commands for pysh.

Built-in commands are handled directly by the shell, rather than by
running an external program. For example, 'cd' must be a built-in
because changing directory needs to affect the shell process itself.

Each built-in is a function that takes a list of string arguments.
"""


commands_list = [
    pwd_command,
    exit_command,
    cd_command,
    procinfo_command,
    cat_command,
    head_command,
    wc_command,
    sysinfo_command,
    download_command,
    echo_command,
    alias_command,
    help_command,
    tail_command,
]

commands_dict = {command["name"]: command for command in commands_list}

__all__ = ["alias_commands_dict", "commands_dict"]
