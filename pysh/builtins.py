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
import time
import requests
import queue
import threading

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
def builtin_head(args: list[str]) -> None:
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
            for _ in range(numLines):
                print(f.readline())
    else:
        print(f'pysh: "{path}" file not found')


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


# TODO: Part 3:
# - `sysinfo` that provides a real-time view of the system's resource usage, similar to `top` or `htop`. This command should display:
# - Memory usage: total, used, available, and percentage of physical memory in use. Also show swap memory usage.
# - CPU usage: overall CPU usage percentage and per-core breakdown
# - Top processes: display the top 10 processes sorted by memory or CPU usage. Use a `--sort` flag to specify the order (e.g. `sysinfo --sort cpu` or `sysinfo --sort memory`). Default to sorting by memory.
# - Refreshing display: the output should refresh at a configurable interval (default: every 2 seconds).


def builtin_sysinfo(args):
    while True:
        mem = psutil.virtual_memory()
        # mem.total  # Total physical memory (bytes)
        # mem.used  # Used memory (bytes)
        # mem.available  # Available memory (bytes)
        # mem.percent  # Percentage used

        swap = psutil.swap_memory()
        # swap.total  # Total swap (bytes)
        # swap.used  # Used swap (bytes)
        # swap.free  # Free swap (bytes)
        # swap.percent  # Percentage used

        psutil.cpu_percent()  # Overall CPU usage (%)
        psutil.cpu_percent(
            percpu=True
        )  # Per-core usage as a list, e.g. [12.0, 5.3, 8.1, 3.2]

        log = f"""
==================== MEMORY ===================\n
------------------- Virtual -------------------\n
    Total: {mem.total / 1024 / 1024:9.2f} MB
Available: {mem.available / 1024 / 1024:9.2f} MB ... {100 - mem.percent:>5.1f}%
     Used: {mem.used / 1024 / 1024:9.2f} MB ... {mem.percent:>5.1f}%
-------------------- Swap ---------------------\n
    Total: {swap.total / 1024 / 1024:9.2f} MB
Available: {swap.free / 1024 / 1024:9.2f} MB ... {100 - swap.percent:>5.1f}%
     Used: {swap.used / 1024 / 1024:9.2f} MB ... {swap.percent:>5.1f}%
"""
        logLines = log.count("\n") + 1

        sys.stdout.flush()
        print(log)

        time.sleep(1)
        sys.stdout.write(f"\033[{logLines}A")
        sys.stdout.write("\r")
        sys.stdout.write("\033[J")


# TODO: Part 4:
# - `download <file>`: read a text file containing URLs (one per line), add them to the download queue, and immediately begin downloading with 3 worker threads. A sample file `test_urls.txt` is provided for testing.
# - `download <file> -w <number>`: same as above, but with a custom number of worker threads (e.g. `download urls.txt -w 5`)
# - `download --status`: show the current state of the download queue and workers (how many items queued, how many workers active, completed count)
def builtin_download(args: list[str]):
    numWorkers = 3
    for [index, string] in enumerate(args):
        if string == "-w":
            index
            args.pop(index)
            numWorkers = int(args[index])
            args.pop(index)
            break

    download_dir = "downloads"
    if len(args) > 1:
        download_dir = args[1]
    os.makedirs(download_dir, exist_ok=True)

    urls = []
    text_file_path = args[0]
    if os.path.isfile(text_file_path):
        with open(text_file_path, "r") as f:
            for line in f:
                urls.append(line.strip())

    work_queue = queue.Queue()

    def worker(index):
        print(f"Started worker [{index}] ")
        while True:
            item = work_queue.get()  # Blocks until an item is available
            if item is None:
                print(f"Terminating worker [{index}]. (No more work in queue)")
                work_queue.task_done()  # Breaks loop after no more urls are available
                break
            print(f"Processing: {item}")

            try:
                response = requests.get(item)
            except requests.ConnectionError:
                print("Could not connect")
            except requests.Timeout:
                print("Request timed out")

            filename = os.path.split(item)[-1]
            download_path = os.path.join(download_dir, filename)
            with open(download_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded: {filename} to path {download_path}")
            work_queue.task_done()

    threads = []
    for i in range(numWorkers):
        t = threading.Thread(target=worker, args=[i], daemon=True)
        threads.append(t)
        t.start()

    for url in urls:
        work_queue.put(url)

    for _ in range(numWorkers):
        work_queue.put(None)

    work_queue.join()

    for t in threads:
        t.join()


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
        "description": "Display a live view of system resource usage, including memory, swap, and CPU statistics.",
        "arguments": [],
        "options": [],
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
    "alias": {
        "function": builtin_alias,
        "description": "",
        "arguments": [],
        "options": [],
    },
}
