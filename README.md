# SKILLS

My custom [Claude Code](https://claude.com/claude-code) skills.

Each folder is a self-contained skill: a `SKILL.md` with YAML frontmatter, plus any
supporting templates or scripts it needs.

## Skills

| Skill | What it does |
|---|---|
| [`handoff`](handoff) | Hand off long-running sessions to fresh ones. Each session writes a detailed handoff doc, `/goal` sessions are stopped afterwards, and you get a paste-ready prompt for every new session. |
| [`master`](master) | A session mode where Opus plans, reviews and verifies while subagents do the hands-on coding and shell work. Keeps a `.master/` folder of working files for the project. |

## `/master`

Turn it on with `/master`. It asks two things, then stays on for the whole session:

- **Agent cap:** 1, 2, 4, 8 or a custom number. A hard limit on subagents running at the same time.
- **Worker model:** picked from the models available in that session (the Agent tool's `model`
  options), so the list stays current. Change either later with `/master 2` or `/master haiku`.

While it is on:

- **Workers are terse.** Every brief ends with a brevity instruction: think and code silently, no
  narration, report in a few lines.
- **The master checks in on running workers** and corrects them early instead of fire-and-forget.
- **The master verifies everything itself.** Frontend changes are reviewed in a real browser (the
  built-in Claude browser by default, Chrome when a logged-in session is needed): layout, responsive,
  dark mode, interactions, console and network, and a screenshot.
- **No AI attribution.** Commits and PRs, including ones workers make, carry no `Co-Authored-By`
  trailer, no "Generated with" line and no mention of an assistant.

### The `.master/` workflow system

In each project the master keeps a `.master/` folder at the repo root. It is the master's working
memory, so the work survives compaction, crashes and handoffs.

| File | Holds |
|---|---|
| `README.md` | Index, current model and agent cap, how the system works |
| `REQUESTS.md` | Every user request, verbatim, with status |
| `PLAN.md` | Goal, phases, chunks, order, how each is verified |
| `TODO.md` | Prioritised backlog |
| `WIP.md` | What is running right now, and by which worker |
| `FINISHED.md` | What landed and how it was verified |
| `DECISIONS.md` | Decisions and why |
| `FRONTEND-DESIGN.md` | Design system, animation and motion system, UI/UX, layouts |
| `BACKEND-DESIGN.md` | Architecture, data model, APIs, security, conventions |
| `AGENTS.md`, `agents/` | Rules for subagents, which read them only when absolutely necessary |

More files can be added when a project needs them. If a project already keeps its own ledger or design
doc, `.master/` points to it instead of duplicating it. Only the master writes these files. The file
specs and starter skeletons are in [`master/workflow-files.md`](master/workflow-files.md).

Every handoff, new-session prompt and final summary the master writes explains this system: what
`.master/` is, how it is used, and how to create it if it is missing.

## Install

Copy (or symlink) a skill folder into your Claude Code skills directory:

```bash
# user-level skills live here
cp -r handoff ~/.claude/skills/handoff
cp -r master  ~/.claude/skills/master
```

On Windows that's `%USERPROFILE%\.claude\skills\`.

Invoke them in a session as `/handoff` and `/master`.
