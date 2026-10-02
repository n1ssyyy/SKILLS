# The `.master/` workflow system: file specs

Read this when bootstrapping `.master/` in a project, or when unsure what a file is for. It is
for the master. Workers do not need it.

## Why `.master/` and not `.claude/`

`.claude/` belongs to the Claude Code harness (settings, hooks, launch config). Mixing the master's
planning files into it risks collisions and makes them hard to find. `.master/` is its own folder, at
the project root, readable by any session or any person. Use `.master/` unless the project already
has an equivalent folder that CLAUDE.md points to; then use that one and say so in `README.md`.

## Principles

- **Short and current beats long and stale.** Each file is a working document, not an archive. Trim
  as you go. Newest state wins.
- **The master writes these files.** Workers do not maintain them (see "Agents" below).
- **Do not duplicate what the project already keeps.** If the project has its own request ledger,
  TODO, decisions log or design doc (CLAUDE.md usually says), do not copy it. Make the `.master/`
  file a one-line pointer to the real one, and keep the real one up to date. The project's own file
  wins every conflict.
- **Never put secrets in any of these files.** Say where a secret lives instead.
- Do not commit `.master/` unless the project's rules or the user say to. On creation, tell the user
  once that it can be committed or added to `.gitignore`, and follow their answer.

## Layout

```
.master/
  README.md            index: what each file is, how to use the system, current model + agent cap
  REQUESTS.md          every user request, verbatim, with date, and its status
  PLAN.md              goal, phases, chunks, order, how each is verified
  TODO.md              prioritised backlog of what is not started
  WIP.md               what is in flight right now: chunk, worker, files, state
  FINISHED.md          what landed and how it was verified, newest first
  DECISIONS.md         decisions and why, so they are not re-litigated
  FRONTEND-DESIGN.md   design system, animation/motion system, UI/UX, layouts, components
  BACKEND-DESIGN.md    architecture, data model, APIs, services, security, infra, conventions
  AGENTS.md            rulebook for subagents (read only when needed)
  agents/              optional role files, one per kind of worker (read only when needed)
```

Add other files when the project earns them, for example `TESTING.md`, `ENVIRONMENT.md`,
`GOTCHAS.md`, `GLOSSARY.md`, `API.md`, `SECURITY.md`, `RELEASE.md`. Register every extra file in
`README.md`. Do not create a file nobody will read. Skip `FRONTEND-DESIGN.md` for a project with no
frontend and `BACKEND-DESIGN.md` for one with no backend.

## File by file

### README.md
Index of the folder, one line per file. Then: "Master mode: model `<alias>`, agent cap `<N>`." Then
the relay paragraph (see SKILL.md) so a cold reader understands the system. Update the model and cap
line when they change.

### REQUESTS.md
Every message the user sends that asks for something, **word for word**, never paraphrased. Newest at
the bottom. Each entry: date, the verbatim text, then `status:` one of `open`, `in progress`, `done`,
`dropped`, with a pointer to the `PLAN.md` chunk or `FINISHED.md` entry. Append the moment the request
arrives, before starting work. Before calling any piece of work finished, re-read this file and check
nothing open was missed. A request the user later changes is a new entry that says it supersedes the
old one; do not rewrite history.

### PLAN.md
Goal in a sentence or two. Then phases, and in each phase the chunks: what it is, which files it
touches, whether it can run beside another chunk or must wait, and how it will be verified. Mark
chunks `todo`, `wip`, `done`. Record the order and *why* that order. Rewrite the plan when it changes
and note the change in `DECISIONS.md`.

### TODO.md
What is not started. One line each, ordered by priority, tagged `frontend`, `backend`, `infra`, `docs`
or similar. When a TODO becomes a chunk it moves to `PLAN.md` and `WIP.md`; delete it from here.

### WIP.md
The live board. One row per running or paused chunk: chunk name, worker (name or id), model, files it
owns, state (`running`, `blocked`, `in review`, `fixing`), and the last thing you noticed at a
check-in. Update when a worker launches, when you check in, and when it finishes. Empty means nothing
is running. After a compaction or crash this file is how you find your place.

### FINISHED.md
Newest first. Each entry: date, what landed, where (files, commits), and **how it was verified**
(tests run, browser check, screenshot taken). Move a chunk here only after you have verified it
yourself, not on a worker's say-so.

### DECISIONS.md
Each decision: date, the decision, who made it (user or master), the reason, what was rejected. Check
it before proposing something that may already have been decided.

### FRONTEND-DESIGN.md
The single source of truth for how the interface looks and behaves. Sections:
- **Design system:** tokens (color, type scale, spacing, radius, elevation, z-index), component
  inventory and their variants, naming, and any rules that are enforced by tests or lint.
- **Animation and motion system:** durations, easing, what is allowed to move and what the movement
  communicates, reduced-motion behaviour, anything that must never flash or loop.
- **UI/UX:** principles, interaction patterns, states every component must have (empty, loading,
  error, disabled, focus), accessibility requirements, copy and tone.
- **Layouts:** page and shell structure, grid, breakpoints, responsive behaviour, dark mode / theming.
- **Stack notes:** framework, styling approach, file layout, where components live.
- **Open design questions** and **known deviations**.
If the project already has a design doc (`DESIGN.md` etc.), link to it from here and add only what it
lacks. This is the document the browser review in the master workflow is judged against.

### BACKEND-DESIGN.md
Same idea for the server side. Sections:
- **Architecture:** services, boundaries, how they talk, what runs where.
- **Data model:** entities, relationships, migrations approach, indexes worth knowing about.
- **APIs and protocols:** endpoints or message types, auth, versioning, error shape, rate limits.
- **Security:** threat notes, secrets handling (where they live, never the values), validation rules.
- **Conventions:** language and framework idioms, error handling, logging, testing approach, how to
  run the build, tests and dev server.
- **Infra and ops:** environments, deploys, config, observability.
- **Open questions** and **known debt**.

### AGENTS.md
The subagent rulebook. Short. It tells a worker: your brief is your source of truth; do not read
anything in `.master/` unless the brief names it or you are blocked without it; do not edit files in
`.master/`; the brevity rules; the report format; the project hard rules that are easy to break. Keep
it under about 40 lines, because a worker that opens it pays for every line.

### agents/
Optional. One short `.md` per worker role when the project has repeating kinds of work, for example
`frontend.md`, `backend.md`, `tests.md`, `refactor.md`, `docs.md`. Each holds only what is specific to
that role: files it usually touches, patterns to imitate, traps, the exact verify commands. Under about
30 lines each. Create one only when the same guidance would otherwise be pasted into several briefs.

## When subagents may open these files

**Only when absolutely necessary.** Every file a worker reads costs tokens, and the master already
reads them. The default is: the master puts what the worker needs into the brief, and the worker never
opens `.master/` at all. A worker may open one file when the brief names it, or when it cannot proceed
without a fact only that file holds. It reads that file and nothing else from the folder. It never
writes to `.master/`; it reports to the master and the master updates the files.

When a brief does name a file, name the exact file and the exact section, not the folder.

## Bootstrapping

1. If `.master/` exists, read `README.md`, `REQUESTS.md`, `PLAN.md`, `WIP.md` and `TODO.md` before
   anything else, and read the design files for whatever is about to change. Do not recreate files.
2. If it does not exist, create the folder and the files above. Seed them from what is real: the
   user's first request into `REQUESTS.md`, the project's CLAUDE.md and docs and the actual code into
   `FRONTEND-DESIGN.md` / `BACKEND-DESIGN.md` (read the code; do not invent a design system the
   project does not have, write what exists and mark gaps as open questions), and a first `PLAN.md`.
   Leave a file that has nothing to say yet as a header with a one-line "nothing yet".
3. A worker may do the legwork of surveying a large codebase to fill the design files, but the master
   reviews and owns what is written.
4. Tell the user in a line or two what was created and where.

## Starter skeletons

Use these headers. Fill only what is real.

```
# REQUESTS
<!-- Verbatim. Newest last. -->
## 2026-01-01
> <exact words>
status: open | in progress | done | dropped  -> PLAN: <chunk> / FINISHED: <entry>
```

```
# PLAN
Goal: ...
## Phase 1: <name>
- [todo] <chunk> | files: ... | parallel: yes/no | verify: ...
Order and why: ...
```

```
# WIP
| chunk | worker | model | owns files | state | last check-in |
|---|---|---|---|---|---|
```

```
# FINISHED
## 2026-01-01  <what landed>
where: ... | verified: ... | request: ...
```

```
# AGENTS (rulebook for subagents)
Your brief is your source of truth. Do not open files in .master/ unless the brief names one or you
cannot proceed without it. Never edit .master/.
Work silently, think and code, no narration. Final report: files changed, commands run with
pass/fail, anything unsure. A few lines.
Project hard rules: <the ones easy to break>
```
