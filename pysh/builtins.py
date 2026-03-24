"""
Built-in commands for pysh.

Built-in commands are handled directly by the shell, rather than by
running an external program. For example, 'cd' must be a built-in
because changing directory needs to affect the shell process itself.

Each built-in is a function that takes a list of string arguments.
Look at builtin_pwd below as a complete example to follow.
"""

import os
import sys
import psutil


# ---------------------------------------------------------------------------
# Example built-in: pwd
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Example built-in: exit
# ---------------------------------------------------------------------------


def builtin_exit(args) -> None:
    """
    Exit the shell.

    Raises SystemExit which is caught by the main loop in shell.py
    to break out of the loop cleanly.
    """
    sys.exit(0)


# ---------------------------------------------------------------------------
# TODO: Implement the remaining built-in commands below.
#       Each function receives a list of string arguments.
#       Look at builtin_pwd above as an example to follow.
# ---------------------------------------------------------------------------

# TODO: Part 1:
# - `cd <path>`: change the current working directory


def builtin_cd(args: list[str]) -> None:
    """
    Change the current working directory.
    """
    path = args[0]
    os.chdir(path)


# - `help`: display a list of available built-in commands with brief descriptions


# - `procinfo <pid>`: use Python's `os` or `psutil` module to display information about a process: its status, memory usage, CPU time, and parent PID
def builtin_procinfo(args: list[str]) -> None:
    """
    Displays information about a process: its status, memory usage, CPU time, and parent PID
    """
    pid = int(args[0])
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print("No process with that PID")
    except psutil.AccessDenied:
        print("Permission denied")

    print(f"Process ID: {proc.pid}")  # 1234
    print(f"Process name: {proc.name()}")  # 'python3'
    print(f"Process status: {proc.status()}")  # 'running', 'sleeping', etc.
    print(f"Process parent process ID: {proc.ppid()}")  # Parent process ID
    print(f"Process CPU usage: {proc.cpu_percent()}%")  # CPU usage as a percentage
    print(
        f"Process memory: {proc.memory_info().rss / 1024 / 1024}MB"
    )  # Resident memory in bytes

    print(psutil.Process(pid))


# TODO: Part 2:
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


# - `head [-n N] <file>`: display the first _N_ lines of a file (default: 10)
# - `wc <file> [file2 ...]`: count and display the number of lines, words, and characters in one or more files. Display totals when multiple files are given.

# TODO: Part 3:
# - `sysinfo` that provides a real-time view of the system's resource usage, similar to `top` or `htop`. This command should display:
# - Memory usage: total, used, available, and percentage of physical memory in use. Also show swap memory usage.
# - CPU usage: overall CPU usage percentage and per-core breakdown
# - Top processes: display the top 10 processes sorted by memory or CPU usage. Use a `--sort` flag to specify the order (e.g. `sysinfo --sort cpu` or `sysinfo --sort memory`). Default to sorting by memory.
# - Refreshing display: the output should refresh at a configurable interval (default: every 2 seconds).

# TODO: Part 4:
# - `download <file>`: read a text file containing URLs (one per line), add them to the download queue, and immediately begin downloading with 3 worker threads. A sample file `test_urls.txt` is provided for testing.
# - `download <file> -w <number>`: same as above, but with a custom number of worker threads (e.g. `download urls.txt -w 5`)
# - `download --status`: show the current state of the download queue and workers (how many items queued, how many workers active, completed count)
