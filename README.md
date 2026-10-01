# SKILLS

My custom [Claude Code](https://claude.com/claude-code) skills.

Each folder is a self-contained skill: a `SKILL.md` with YAML frontmatter, plus any
supporting templates or scripts it needs.

## Skills

| Skill | What it does |
|---|---|
| [`handoff`](handoff) | Hand off long-running sessions to fresh ones. Each session writes a detailed handoff doc, `/goal` sessions are stopped afterwards, and you get a paste-ready prompt for every new session. |
| [`master`](master) | Toggle "master mode" for a whole session: Opus plans, reviews and delegates while Sonnet agents do the hands-on coding and shell work, under a hard cap on concurrent agents. |

## Install

Copy (or symlink) a skill folder into your Claude Code skills directory:

```bash
# user-level skills live here
cp -r handoff ~/.claude/skills/handoff
cp -r master  ~/.claude/skills/master
```

On Windows that's `%USERPROFILE%\.claude\skills\`.

Invoke them in a session as `/handoff` and `/master`.
