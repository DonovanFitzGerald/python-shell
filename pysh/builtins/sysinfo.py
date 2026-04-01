import os
import subprocess
import time
import psutil


# TODO: Part 3:
# - `sysinfo` that provides a real-time view of the system's resource usage, similar to `top` or `htop`. This command should display:
# - Memory usage: total, used, available, and percentage of physical memory in use. Also show swap memory usage.
# - CPU usage: overall CPU usage percentage and per-core breakdown
# - Top processes: display the top 10 processes sorted by memory or CPU usage. Use a `--sort` flag to specify the order (e.g. `sysinfo --sort cpu` or `sysinfo --sort memory`). Default to sorting by memory.
# - Refreshing display: the output should refresh at a configurable interval (default: every 2 seconds).


def builtin_sysinfo(args: list[str]) -> None:
    sort_by = "memory"
    interval = 2.0

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--sort":
            if i + 1 >= len(args):
                print("pysh: sysinfo: --sort requires 'cpu' or 'memory'")
                return

            value = args[i + 1].lower()
            if value not in ("cpu", "memory"):
                print("pysh: sysinfo: --sort must be 'cpu' or 'memory'")
                return

            sort_by = value
            i += 2
            continue

        if arg in ("-i", "--interval"):
            if i + 1 >= len(args):
                print("pysh: sysinfo: interval flag requires a number")
                return

            try:
                interval = float(args[i + 1])
            except ValueError:
                print("pysh: sysinfo: interval must be a number")
                return

            if interval <= 0:
                print("pysh: sysinfo: interval must be greater than 0")
                return

            i += 2
            continue

        print(f"pysh: sysinfo: unexpected argument: {arg}")
        return

    def mb(value):
        return value / 1024 / 1024

    def clear_terminal() -> None:
        subprocess.run(
            ["cls"] if os.name == "nt" else ["clear"],
            shell=(os.name == "nt"),
            check=False,
        )

    psutil.cpu_percent(interval=None)
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    try:
        while True:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            cpu_total = psutil.cpu_percent(interval=None)
            cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)

            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "ppid", "memory_info", "cpu_percent", "status"]
            ):
                try:
                    info = proc.info
                    rss = info["memory_info"].rss if info["memory_info"] else 0
                    cpu = (
                        info["cpu_percent"] if info["cpu_percent"] is not None else 0.0
                    )

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
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            if sort_by == "cpu":
                processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
            else:
                processes.sort(key=lambda p: p["memory_mb"], reverse=True)

            top_processes = processes[:10]

            core_lines = [
                "===================== CPU =====================",
                f"Overall: {cpu_total:>5.1f}%",
            ]
            for index, value in enumerate(cpu_per_core):
                core_lines.append(f"Core {index:>2}: {value:>5.1f}%")

            process_lines = [
                "================= TOP PROCESSES =================",
                f"{'PID':>7}  {'PPID':>7}  {'CPU %':>7}  {'MEM MB':>10}  {'STATUS':<12}  NAME",
                "-" * 70,
            ]
            for proc in top_processes:
                process_lines.append(
                    f"{proc['pid']:>7}  "
                    f"{proc['ppid']:>7}  "
                    f"{proc['cpu_percent']:>7.1f}  "
                    f"{proc['memory_mb']:>10.2f}  "
                    f"{proc['status']:<12.12}  "
                    f"{proc['name']}"
                )

            log_lines = [
                "==================== MEMORY ====================",
                "------------------- Virtual -------------------",
                f"    Total: {mb(mem.total):9.2f} MB",
                f"Available: {mb(mem.available):9.2f} MB     {100 - mem.percent:>5.1f}%",
                f"     Used: {mb(mem.used):9.2f} MB     {mem.percent:>5.1f}%",
                "-------------------- Swap ---------------------",
                f"    Total: {mb(swap.total):9.2f} MB",
                f"Available: {mb(swap.free):9.2f} MB     {100 - swap.percent:>5.1f}%",
                f"     Used: {mb(swap.used):9.2f} MB     {swap.percent:>5.1f}%",
                "",
                *core_lines,
                "",
                *process_lines,
            ]

            log = "\n".join(log_lines)

            clear_terminal()
            print(log, flush=True)

            time.sleep(interval)

    except KeyboardInterrupt:
        print()

    def mb(value: int | float) -> float:
        return value / 1024 / 1024

    psutil.cpu_percent(interval=None)
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    time.sleep(0.15)

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    cpu_total = psutil.cpu_percent(interval=None)
    cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)

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

    if sort_by == "cpu":
        processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
    else:
        processes.sort(key=lambda p: p["memory_mb"], reverse=True)

    top_processes = processes[:10]

    core_lines = []
    core_lines.append("===================== CPU =====================")
    core_lines.append(f"Overall: {cpu_total:>5.1f}%")
    for index, value in enumerate(cpu_per_core):
        core_lines.append(f"Core {index:>2}: {value:>5.1f}%")

    process_lines = []
    process_lines.append("================= TOP PROCESSES =================")
    process_lines.append(
        f"{'PID':>7}  {'PPID':>7}  {'CPU %':>7}  {'MEM MB':>10}  {'STATUS':<12}  NAME"
    )
    process_lines.append("-" * 76)

    for proc in top_processes:
        process_lines.append(
            f"{proc['pid']:>7}  {proc['ppid']:>7}  {proc['cpu_percent']:>7.1f}  "
            f"{proc['memory_mb']:>10.2f}  {proc['status']:<12.12}  {proc['name']}"
        )

    log_lines = [
        "==================== MEMORY ====================",
        "------------------- Virtual -------------------",
        f"    Total: {mb(mem.total):9.2f} MB",
        f"Available: {mb(mem.available):9.2f} MB     {100 - mem.percent:>5.1f}%",
        f"     Used: {mb(mem.used):9.2f} MB     {mem.percent:>5.1f}%",
        "-------------------- Swap ---------------------",
        f"    Total: {mb(swap.total):9.2f} MB",
        f"Available: {mb(swap.free):9.2f} MB     {100 - swap.percent:>5.1f}%",
        f"     Used: {mb(swap.used):9.2f} MB     {swap.percent:>5.1f}%",
        "",
        *core_lines,
        *process_lines,
    ]

    print("\n".join(log_lines))


COMMAND = {
    "name": "sysinfo",
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
}
