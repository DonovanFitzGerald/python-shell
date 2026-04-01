import psutil

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
