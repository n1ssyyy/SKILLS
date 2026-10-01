"""Watch handoff files and print one line per change, for the Monitor tool.

Usage: python watch_handoffs.py NAME=PATH [NAME=PATH ...]

Prints "STARTED <name>" when a file appears, "DONE <name>" when its last line is the
completion marker, and "ALL HANDOFFS DONE" once every file is finished, then exits.
Every 10 minutes it prints which handoffs are still missing. After 28 minutes it prints
"WATCH EXPIRED" and exits, so the caller can re-arm it before Monitor's 30-minute limit.
"""
import os
import sys
import time

MARKER = "<!-- HANDOFF COMPLETE -->"
POLL = 5
NUDGE = 10 * 60
LIMIT = 28 * 60


def finished(path):
    try:
        with open(path, "rb") as f:
            size = f.seek(0, 2)
            f.seek(max(0, size - 512))
            lines = f.read().decode("utf-8", "replace").strip().splitlines()
    except OSError:
        return False
    return bool(lines) and lines[-1].strip() == MARKER


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = dict(arg.split("=", 1) for arg in sys.argv[1:])
    if not files:
        sys.exit("usage: watch_handoffs.py NAME=PATH [NAME=PATH ...]")
    started, done = set(), set()
    t0 = last_nudge = time.time()
    while True:
        for name, path in files.items():
            if name not in started and os.path.exists(path):
                started.add(name)
                print(f"STARTED {name} ({os.path.getsize(path)} bytes)", flush=True)
            if name not in done and finished(path):
                done.add(name)
                print(f"DONE {name} ({os.path.getsize(path)} bytes)", flush=True)
        if len(done) == len(files):
            print("ALL HANDOFFS DONE", flush=True)
            return
        now = time.time()
        waiting = ", ".join(n for n in files if n not in done)
        if now - t0 > LIMIT:
            print(f"WATCH EXPIRED, still waiting on: {waiting}", flush=True)
            return
        if now - last_nudge > NUDGE:
            last_nudge = now
            print(f"STILL WAITING after {int((now - t0) / 60)} min: {waiting}", flush=True)
        time.sleep(POLL)


if __name__ == "__main__":
    main()
