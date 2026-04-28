import sys
import time
import shutil
import psutil


def mb(bytes_value):
    return bytes_value / (1024 * 1024)


def get_terminal_width():
    return shutil.get_terminal_size(fallback=(80, 24)).columns


def get_terminal_height():
    return shutil.get_terminal_size(fallback=(80, 24)).lines


def build_section_header(title):
    width = get_terminal_width()
    return f"{title:=^{width}}"


def build_memory_log():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    lines = [
        build_section_header(" MEMORY "),
        f"{'--- Virtual ---':^40}",
        f"    Total: {mb(mem.total):9.2f} MB",
        f"Available: {mb(mem.available):9.2f} MB     {100 - mem.percent:>5.1f}% free",
        f"     Used: {mb(mem.used):9.2f} MB     {mem.percent:>5.1f}% used",
        f"{'--- Swap ---':^40}",
        f"    Total: {mb(swap.total):9.2f} MB",
        f"     Used: {mb(swap.used):9.2f} MB     {swap.percent:>5.1f}% used",
    ]
    return lines


def build_cpu_log():
    cpu_total = psutil.cpu_percent(interval=None)
    cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)

    lines = ["", build_section_header(" CPU "), f"Overall Usage: {cpu_total:>5.1f}%"]

    core_str = ""
    for i, val in enumerate(cpu_per_core):
        core_str += f"Core {i:>2}: {val:>5.1f}%  | "
        if (i + 1) % 3 == 0:  # Wrap every 3 cores
            lines.append(core_str.rstrip(" | "))
            core_str = ""
    if core_str:
        lines.append(core_str.rstrip(" | "))

    return lines


def build_process_log(sort_by):
    width = get_terminal_width()
    processes = []

    for proc in psutil.process_iter(
        ["pid", "name", "ppid", "memory_info", "cpu_percent", "status"]
    ):
        try:
            info = proc.info
            rss = info["memory_info"].rss if info["memory_info"] else 0
            cpu = info["cpu_percent"] if info["cpu_percent"] is not None else 0.0
            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"] or "?",
                    "ppid": info["ppid"],
                    "status": info["status"] or "?",
                    "memory_mb": mb(rss),
                    "cpu_percent": cpu,
                }
            )
        except psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess:
            continue

    # Sort logic
    key = "cpu_percent" if sort_by == "cpu" else "memory_mb"
    processes.sort(key=lambda p: p[key], reverse=True)
    top_processes = processes[:10]

    header = (
        f"{'PID':>7}  {'PPID':>7}  {'CPU %':>7}  {'MEM MB':>10}  {'STATUS':<12}  NAME"
    )
    lines = ["", build_section_header(" TOP PROCESSES "), header, "-" * min(width, 80)]

    for proc in top_processes:
        line = (
            f"{proc['pid']:>7}  {proc['ppid']:>7}  {proc['cpu_percent']:>7.1f}  "
            f"{proc['memory_mb']:>10.2f}  {proc['status']:<12.12}  {proc['name']}"
        )
        lines.append(line[:width])

    return lines


def builtin_sysinfo(args: list[str]) -> None:
    sort_by = "memory"
    interval = 2.0
    i = 0
    while i < len(args):
        if args[i] == "--sort" and i + 1 < len(args):
            sort_by = args[i + 1].lower()
            i += 2
        elif args[i] in ("-i", "--interval") and i + 1 < len(args):
            try:
                interval = float(args[i + 1])
            except ValueError:
                print("Error: Interval must be a number")
                return
            i += 2
        else:
            i += 1

    psutil.cpu_percent(interval=None)

    try:
        line_count = 0
        print()
        while True:
            all_lines = []
            all_lines.extend(build_memory_log())
            all_lines.extend(build_cpu_log())
            all_lines.extend(build_process_log(sort_by))

            width = get_terminal_width()
            height = get_terminal_height()
            output = "\n".join([line.ljust(width) for line in all_lines[-height:]])

            sys.stdout.write("\r")
            sys.stdout.write(f"\033[{line_count}F")
            print(output, flush=True, end="")
            line_count = output.count("\n")
            line_count = line_count if height > line_count else height

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nExiting sysinfo...")


COMMAND = {
    "name": "sysinfo",
    "function": builtin_sysinfo,
    "description": "Display a live view of memory, swap, CPU, and top processes.",
    "arguments": [],
    "options": [
        {"flag": "--sort", "value": "cpu|memory", "description": "Sort order."},
        {"flag": "-i", "value": "seconds", "description": "Refresh interval."},
    ],
}
