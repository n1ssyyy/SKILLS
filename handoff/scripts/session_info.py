"""Find each Claude Code session's transcript and report its /goal and context size.

Usage:
  python session_info.py < sessions.json
      sessions.json is a JSON list of the objects list_sessions / get_session return
      (sessionId, title, cwd, lastActivityAt, isRunning). Prints one JSON object per line.
  python session_info.py --transcript PATH
      Report on one transcript directly (use it for the running session:
      ~/.claude/projects/<cwd with every non-alphanumeric char as '-'>/<CLAUDE_SESSION_ID>.jsonl).

Output fields: sessionId, title, cwd, running, transcript, match (title / time / none),
goal (the active /goal condition, or null), context_tokens (size of the latest request).
The active-goal rule mirrors Claude Code's own: the latest goal_status attachment decides,
and a goal that was met, failed or cleared is not active.
"""
import json
import mmap
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"
CLEAR_WORDS = {"clear", "stop", "off", "reset", "none", "cancel"}
GOAL_CMD = b"<command-name>/goal</command-name>"


def project_dir(cwd):
    return PROJECTS / re.sub(r"[^A-Za-z0-9]", "-", cwd)


def epoch(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except (AttributeError, ValueError):
        return None


def line_at(m, i):
    start = m.rfind(b"\n", 0, i) + 1
    end = m.find(b"\n", i)
    end = len(m) if end < 0 else end
    try:
        return json.loads(m[start:end])
    except ValueError:
        return None


def last_matching(m, needle, pred):
    """Position and entry of the last line containing needle whose entry satisfies pred."""
    hi = len(m)
    while True:
        i = m.rfind(needle, 0, hi)
        if i < 0:
            return -1, None
        e = line_at(m, i)
        if e is not None and pred(e):
            return i, e
        hi = i


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def is_goal_status(e):
    return e.get("type") == "attachment" and (e.get("attachment") or {}).get("type") == "goal_status"


def is_goal_command(e):
    return e.get("type") == "user" and text_of((e.get("message") or {}).get("content")).lstrip().startswith(
        "<command-name>/goal</command-name>")


def title_of(m):
    for needle, key in ((b'"type":"custom-title"', "customTitle"), (b'"type":"agent-name"', "agentName")):
        _, e = last_matching(m, needle, lambda e, key=key: bool(e.get(key)))
        if e:
            return e[key]
    return None


def goal_of(m):
    gi, g = last_matching(m, b'"goal_status"', is_goal_status)
    if not g:
        return None
    a = g["attachment"]
    if a.get("met") or a.get("failed"):
        return None
    ci, c = last_matching(m, GOAL_CMD, is_goal_command)
    if c and ci > gi:
        args = re.search(r"<command-args>(.*?)</command-args>", text_of(c["message"]["content"]), re.S)
        if args and args.group(1).strip().lower() in CLEAR_WORDS:
            return None
    cond = a.get("condition")
    return cond if isinstance(cond, str) and cond else None


def context_of(m):
    def has_usage(e):
        return e.get("type") == "assistant" and bool((e.get("message") or {}).get("usage"))
    _, e = last_matching(m, b'"usage"', has_usage)
    if not e:
        return None
    u = e["message"]["usage"]
    return sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


def open_map(path):
    f = open(path, "rb")
    if f.seek(0, 2) == 0:
        f.close()
        return None, None
    return f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)


def report(path):
    f, m = open_map(path)
    if m is None:
        return {"goal": None, "context_tokens": None}
    try:
        return {"goal": goal_of(m), "context_tokens": context_of(m)}
    finally:
        m.close()
        f.close()


def find_transcript(sess):
    title = (sess.get("title") or "").strip().lower()
    last = epoch(sess.get("lastActivityAt") or "")
    dirs = []
    for key in ("cwd", "originCwd"):
        if sess.get(key):
            d = project_dir(sess[key])
            if d.is_dir() and d not in dirs:
                dirs.append(d)
    cands = [p for d in dirs for p in d.glob("*.jsonl")]

    def closeness(p):
        return abs(p.stat().st_mtime - last) if last else -p.stat().st_mtime

    cands.sort(key=closeness)
    for p in cands[:40]:
        f, m = open_map(p)
        if m is None:
            continue
        try:
            t = title_of(m)
        finally:
            m.close()
            f.close()
        if t and t.strip().lower() == title:
            return p, "title"
    if cands and last and closeness(cands[0]) < 15 * 60:
        return cands[0], "time"
    return None, "none"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) == 3 and sys.argv[1] == "--transcript":
        p = Path(sys.argv[2])
        print(json.dumps({"transcript": str(p), **report(p)}, ensure_ascii=False))
        return
    sessions = json.load(sys.stdin)
    if isinstance(sessions, dict):
        sessions = [sessions]
    for s in sessions:
        path, how = find_transcript(s)
        row = {
            "sessionId": s.get("sessionId"),
            "title": s.get("title"),
            "cwd": s.get("cwd"),
            "running": s.get("isRunning"),
            "transcript": str(path) if path else None,
            "match": how,
        }
        row.update(report(path) if path else {"goal": None, "context_tokens": None})
        print(json.dumps(row, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
