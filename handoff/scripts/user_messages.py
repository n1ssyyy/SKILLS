"""Print every message the user typed in a Claude Code transcript, oldest first, word for word.

Usage: python user_messages.py TRANSCRIPT.jsonl

Includes messages typed while Claude was mid-turn, and slash commands (printed as
"/name args"). Skips tool results, system reminders, messages from other sessions and
compaction summaries. Use it to quote the user exactly in a handoff, even after the
conversation has been compacted.
"""
import json
import re
import sys


def text_blocks(content):
    if isinstance(content, str):
        return [content]
    out = []
    for b in content or []:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "tool_result":
            return []
        if b.get("type") == "text":
            out.append(b.get("text", ""))
        elif b.get("type") == "image":
            out.append("[image]")
    return out


def render(text):
    text = text.strip()
    cmd = re.match(r"<command-name>(/[^<]+)</command-name>", text)
    if cmd:
        args = re.search(r"<command-args>(.*?)</command-args>", text, re.S)
        return f"{cmd.group(1)} {args.group(1).strip() if args else ''}".strip()
    if not text or text.startswith("<"):
        return None
    return text


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(sys.argv[1], encoding="utf-8") as f:
        for line in f:
            if '"user"' not in line and '"queued_command"' not in line:
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            when = (e.get("timestamp") or "")[:19].replace("T", " ")
            if e.get("type") == "attachment":
                a = e.get("attachment") or {}
                if a.get("type") == "queued_command" and (a.get("origin") or {}).get("kind") == "human":
                    msg = render(a.get("prompt") or "")
                    if msg:
                        print(f"[{when}] (sent mid-turn) {msg}\n", flush=True)
                continue
            if e.get("type") != "user" or e.get("isMeta") or e.get("isCompactSummary"):
                continue
            parts = [render(t) for t in text_blocks((e.get("message") or {}).get("content"))]
            parts = [p for p in parts if p]
            if parts:
                print(f"[{when}] " + "\n".join(parts) + "\n", flush=True)


if __name__ == "__main__":
    main()
