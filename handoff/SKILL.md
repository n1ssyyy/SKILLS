---
name: handoff
description: Hand off long-running sessions to fresh ones. Covers this session, sessions you pick, or every active session. Each session writes a detailed handoff doc, /goal sessions are stopped afterwards, and you get a paste-ready prompt for each new session.
argument-hint: "[this | pick | all | everything]"
disable-model-invocation: true
---

# /handoff

Move work out of long, slow sessions into fresh ones without losing anything. Each session
writes a handoff doc. You then turn each doc into a prompt the user pastes into a new session.

This skill's folder (written as {{SKILL_DIR}} in the templates) is `${CLAUDE_SKILL_DIR}`.
Supporting files:
- `checklist.md`: what every handoff must cover.
- `request-template.md`: the message sent to other sessions.
- `prompt-template.md`: the new-session prompts and the prompts file.
- `scripts/session_info.py`: finds each session's transcript, its active /goal and its context size.
- `scripts/watch_handoffs.py`: prints STARTED, DONE and ALL HANDOFFS DONE as handoff files are
  written. Run it with the Monitor tool.
- `scripts/user_messages.py`: prints every message the user typed in a transcript, word for word.

Run scripts with `python`. On Windows, pass paths in Windows form.

## 1. Choose what to hand off

`$ARGUMENTS` can skip the first question: `this` or `self` means this session; `pick` means pick
sessions; `all` means all active sessions; `everything` means all active sessions plus this one.

Otherwise, gather first, then ask:
- Call `get_session` with `"self"` for this session's title and folder.
- Call `list_sessions` with limit 30, and `ListAgents` for which sessions are busy right now.
- Pipe the list into `scripts/session_info.py`. Save the list to a JSON file in the scratchpad
  and redirect it into the script. The script adds each session's transcript path, active /goal
  and context size.
- "Active" means running now, or active in the last 3 hours. Leave out archived sessions, and
  sessions whose folder doesn't exist on this machine (cloud sessions).

Ask with AskUserQuestion: "What do you want to hand off?", header "Handoff", single select.
- **This session**: "Write a handoff for this conversation and get a prompt to continue it in a
  fresh session."
- **Pick sessions**: "Choose which of your other sessions to hand off."
- **All active sessions**: "Every other session running now or used in the last 3 hours:
  <titles>." If there are none, drop this option and say why in the question.
- **All active + this one**: "The above, plus this session."

## 2. Pick sessions (only for "Pick sessions")

Ask in one AskUserQuestion call with up to 4 multi-select questions of up to 4 sessions each.
Headers are "Sessions 1", "Sessions 2" and so on. List busy sessions first, then the rest by
most recent activity.
- **Label:** the session title, cut to about 40 characters.
- **Description:** status, folder name and last activity. Then context size and /goal if it has
  one. For example: "Running · EXIL · active 4 min ago · 137K tokens · has /goal".

If there are more than 16 sessions, say in the first question that others can be typed into
"Other" by title. If nothing is selected, stop and say so.

## 3. Confirm and set options (whenever other sessions are included)

Make one AskUserQuestion call. Put the full list of target titles in the first question's text.
- Only if any target is busy: "Hand off <N> sessions: <titles>. <K> are mid-task. Interrupt them
  so the handoff runs now?", header "Busy ones".
  - **Interrupt now (Recommended)**: "Stops their current turn. The handoff request runs next
    and records where the work stopped."
  - **Let them finish first**: "The request waits until each one finishes its current turn. A
    session with a /goal may never finish, so it would never hand off."
  - **Cancel handoff**: "Send nothing."
- Always: "After each handoff is written, what should happen to the old session?", header "Old
  ones". If the busy question was skipped, put the list of titles in this question's text and
  add a "Cancel handoff" option.
  - **Leave them open (Recommended)**: "/goal sessions are still stopped so they don't keep
    working."
  - **Archive them**: "Archives each old session once its handoff is done. You can bring one back
    from the Archived list. Pinned sessions stay."

## 4. Send the requests

For each target session:
1. **Handoff path:** `<session folder>\HANDOFF-<slug>-<YYYY-MM-DD>.md`. The slug is the title in
   lowercase, with every non-alphanumeric run turned into `-`, cut to about 40 characters at a
   word boundary. If the file exists, add `-2`, `-3` and so on.
2. **Message:** `request-template.md` with its placeholders filled in, followed by the full text
   of `checklist.md`.
3. **Send:** use `SendMessage` with `to` set to the session's `local_...` id, and
   `notify_when_idle: true`.
4. **Interrupt:** if the user chose to interrupt and the session is busy, call `stop_session`
   *after* sending. The queued request then runs next. Without this, a busy session never
   shows the request.

Then start one watcher for all targets with the Monitor tool (`timeout_ms` 1800000):
`python "${CLAUDE_SKILL_DIR}/scripts/watch_handoffs.py" "<slug>=<path>" ...`
If it prints `WATCH EXPIRED`, re-arm it with only the unfinished ones.

Tell the user in two or three lines: which sessions got the request, that it appears at the
bottom of each chat, and that you'll gather the handoffs as they finish.

If a target shows no STARTED within about 3 minutes, check its last few events with
`list_events` (limit 6).
- **The request isn't there:** the session is holding it for approval, because it runs in a
  different permission mode. Tell the user to approve it in that session.
- **The session asked a question, or declined:** tell the user what it said.

An idle notice without a DONE means the same thing, so check it the same way.

## 5. As each handoff finishes (DONE)

1. **If the session has an active /goal:** call `stop_session` right away. The goal would
   otherwise start it working again when its turn ends. After ALL HANDOFFS DONE, check
   `ListAgents` once more, and stop any /goal session that is running again.
2. **If the user chose to archive:** once the session is idle, call `archive_session` with the
   reason "Handed off to a new session". If it's refused (pinned, or open on screen), tell the
   user.
3. **Write its prompt:** read the handoff fully, then add its block to the prompts file following
   `prompt-template.md`. The prompts file is
   `%USERPROFILE%\.claude\handoffs\prompts-<YYYY-MM-DD-HHMM>.md`; create the folder if needed.
   Give the user one short line per finished handoff.

## 6. This session (for "This session" and "All active + this one")

When other sessions are included too, send their requests and start the watcher first. Then
write this one while they work.
1. **Transcript:** this session's transcript is
   `%USERPROFILE%\.claude\projects\<folder with every non-alphanumeric character as ->\${CLAUDE_SESSION_ID}.jsonl`.
   Run `session_info.py --transcript <path>` to get this session's /goal.
2. **The user's words:** run `scripts/user_messages.py` on the transcript. It recovers every
   user message word for word, even from before a compaction.
3. **The handoff:** write it to `<this folder>\HANDOFF-<slug>-<YYYY-MM-DD>.md`. Cover everything
   in `checklist.md`, and end with the line `<!-- HANDOFF COMPLETE -->`.
4. **The prompt:** add this session's block to the prompts file, and also show its prompt in chat
   as a code block so it's easy to copy.
5. **If this session has an active /goal:** tell the user it will keep working after this reply,
   and that they can press Stop or run `/goal clear` here.

## 7. Wrap up

When everything is finished:
- Send the prompts file with `SendUserFile` (`display: "attach"`).
- Summarize in a few lines: which handoffs were written, which sessions were stopped or archived,
  and for each new session, the folder to open and any `/goal` line to run.
- Check once with ToolSearch for a tool that starts sessions (`start_session`).
  - **If one exists:** ask whether to start the new sessions for the user, each with its folder,
    effort high and its prompt. The /goal line still has to be run by the user.
  - **If none exists:** say the user opens each new session themselves, sets effort to High and
    pastes its prompt.

## Rules

- Never put secrets (API keys, tokens, passwords) in a request, handoff or prompt.
- Don't stop a session before its handoff is DONE. The only exception is the interrupt in step 4,
  which the user chose.
- Use session titles, not ids, in everything the user reads.
- Don't answer on another session's behalf, and don't approve anything in it.
- Keep updates short. The prompts file carries the detail.
