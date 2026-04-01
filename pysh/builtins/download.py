import os
import requests
import queue
import threading

# TODO: Part 4:
# - `download <file>`: read a text file containing URLs (one per line), add them to the download queue, and immediately begin downloading with 3 worker threads. A sample file `test_urls.txt` is provided for testing.
# - `download <file> -w <number>`: same as above, but with a custom number of worker threads (e.g. `download urls.txt -w 5`)
# - `download --status`: show the current state of the download queue and workers (how many items queued, how many workers active, completed count)

download_state = {
    "queue": queue.Queue(),
    "threads": [],
    "active": [],
    "completed": [],
    "failed": [],
    "started": False,
    "download_dir": "downloads",
    "lock": threading.Lock(),
}


def download_worker() -> None:
    current = threading.current_thread()

    while True:
        item = download_state["queue"].get()

        if item is None:
            download_state["queue"].task_done()
            with download_state["lock"]:
                if current in download_state["threads"]:
                    download_state["threads"].remove(current)
            break

        url, download_dir = item

        with download_state["lock"]:
            download_state["active"].append(url)

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            filename = os.path.basename(url) or f"download_{current.ident}"
            download_path = os.path.join(download_dir, filename)

            with open(download_path, "wb") as f:
                f.write(response.content)

            with download_state["lock"]:
                download_state["completed"].append(url)

        except requests.RequestException as e:
            with download_state["lock"]:
                download_state["failed"].append((url, e))

        finally:
            with download_state["lock"]:
                if url in download_state["active"]:
                    download_state["active"].remove(url)
            download_state["queue"].task_done()


def builtin_download(args: list[str]) -> None:
    if not args:
        print("pysh: download: expected a file or --status")
        return

    if args[0] == "--status":
        if len(args) >= 2 and (args[1] == "--verbose" or "-v"):
            with download_state["lock"]:
                queued = max(
                    0, download_state["queue"].qsize() - len(download_state["threads"])
                )
                workers = len(download_state["threads"])
                active = list(download_state["active"])
                completed = list(download_state["completed"])
                failed = list(download_state["failed"])

            print("========== DOWNLOAD STATUS ==========")
            print(f"Queued:    {queued}")
            print(f"Workers:   {workers}")
            print(f"Active:    {len(active)}")
            print(f"Completed: {len(completed)}")
            print(f"Failed:    {len(failed)}")
            print()

            if active:
                print("ACTIVE DOWNLOADS")
                print("----------------")
                for url in active:
                    print(f"- {url}")
                print()

            if completed:
                print("COMPLETED DOWNLOADS")
                print("-------------------")
                for url in completed:
                    print(f"- {url}")
                print()

            if failed:
                print("FAILED DOWNLOADS")
                print("----------------")
                for url, error in failed:
                    print(f"- {url}")
                    print(f"  Error: {error}")
                print()
            return

        with download_state["lock"]:
            active = len(download_state["active"])
            completed = len(download_state["completed"])
            failed = len(download_state["failed"])
            workers = len(download_state["threads"])
            qsize = download_state["queue"].qsize() - workers

        print(f"Queued: {qsize}")
        print(f"Workers: {workers}")
        print(f"Active: {active}")
        print(f"Completed: {completed}")
        print(f"Failed: {failed}")
        return

    num_workers = 3
    download_dir = "downloads"
    text_file_path = None

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "-w":
            if i + 1 >= len(args):
                print("pysh: download: -w requires a number")
                return
            try:
                num_workers = int(args[i + 1])
            except ValueError:
                print("pysh: download: worker count must be an integer")
                return
            i += 2
            continue

        if text_file_path is None:
            text_file_path = arg
        elif download_dir == "downloads":
            download_dir = arg
        else:
            print(f"pysh: download: unexpected argument: {arg}")
            return

        i += 1

    if text_file_path is None:
        print("pysh: download: missing URL file")
        return

    if not os.path.isfile(text_file_path):
        print(f'pysh: download: "{text_file_path}" file not found')
        return

    os.makedirs(download_dir, exist_ok=True)

    new_workers = 0
    while len(download_state["threads"]) < num_workers:
        t = threading.Thread(target=download_worker, daemon=True)
        download_state["threads"].append(t)
        t.start()
        new_workers += 1

    queued_now = 0
    with open(text_file_path, "r") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue
            download_state["queue"].put((url, download_dir))
            queued_now += 1

    for _ in range(new_workers):
        download_state["queue"].put(None)

    print(
        f"Queued {queued_now} download(s) with {len(download_state['threads'])} worker(s)."
    )


COMMAND = {
    "name": "download",
    "function": builtin_download,
    "description": "Download URLs from a text file optionally with a download directory.",
    "arguments": ["text_file", "download_dir"],
    "options": [
        {
            "flag": "-w",
            "value": "number",
            "description": "Number of worker threads to use.",
        }
    ],
}
