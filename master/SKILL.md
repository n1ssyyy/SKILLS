---
name: master
description: Toggle master mode for the whole session. While on, Opus plans, thinks and reviews, and Sonnet 5.5 agents write the code and run the shell commands. Asks how many agents to use (1, 2, 4, 8 or custom) as a hard cap. Use /master enable, /master disable, or /master alone to toggle.
---

# /master: a session mode, not a task

`/master` switches the session into (or out of) a working mode. While the mode is on, **every
request the user sends for the rest of the session** is handled with the workflow below. The user
does not need to repeat `/master` or attach a task to it.

## Step 0: Work out what the user asked for

Look at the arguments after `/master` and at whether master mode is currently on. It is on if it was
enabled earlier in this conversation and not disabled since. Otherwise it is off.

| Input | Mode is off | Mode is on |
|---|---|---|
| `enable`, `on` | Turn on (Step 1) | Say it is already on and keep the current agent cap. Offer nothing else. |
| `disable`, `off` | Say it is already off | Turn off (see "Turning off") |
| nothing | Turn on (Step 1) | Ask with `AskUserQuestion`: header `Master mode`, question `Master mode is on. Disable it?`, options `Disable` and `Keep on`. Act on the answer. |
| a number (`4`) | Turn on with that cap, skip the panel | Change the cap to it, confirm in one line |
| anything else | Turn on (Step 1), then treat the text as the first task | Treat it as a normal request under the workflow |

## Step 1: Turn on and ask for the agent cap

Call `AskUserQuestion` with one question:

- header: `Agents`
- question: `How many Sonnet agents may I use while master mode is on?`
- multiSelect: false
- options: `1 agent`, `2 agents`, `4 agents`, `8 agents`. Each description says it is a hard cap. The
  panel adds "Other" automatically for a custom number.

The answer is a **hard cap on agents running at the same time** for the whole session. Never exceed
it. Fewer is fine when the work does not split. Keep the cap until the user changes it (`/master 2`,
or just asking) or turns the mode off.

Then confirm in one line: master mode on, cap N. If a task came with the command, start on it. If not,
wait for the user's next message.

## Turning off

Confirm in one line that master mode is off. From then on, work normally: no forced delegation, no
cap. Do not keep following the workflow below. `/master` again turns it back on and asks for the cap
again.

## The workflow (applies to every request while the mode is on)

You are the master. You think, plan, delegate, review and verify. Sonnet 5.5 agents do the hands-on
work: writing code, editing files, running builds, tests and shell commands.

A request that is only a question, a discussion or a quick lookup of one fact can be answered
directly. Anything that means changing files or running commands goes through workers.

### Plan (you, Opus)

- Read what you need to plan: the project's CLAUDE.md, the ledgers and handoff files it points to,
  the relevant code, recent git log. Use read-only search to build a real picture.
- Write a short plan: goal, the chunks of work, which are independent, the order, and how each chunk
  will be verified.
- Split work so parallel agents touch **disjoint files**. Anything that shares files or depends on an
  earlier result runs after it, not beside it. With a cap of 1, everything is sequential.
- Do not write the implementation yourself. Your own edits are limited to tiny glue you cannot
  sensibly delegate, and planning notes.

### Delegate with the Agent tool

Every worker is spawned with `subagent_type: "general-purpose"` and `model: "sonnet"`. Never leave
the model unset, or the worker inherits Opus.

A good brief gives the agent everything to succeed **without giving it ready-made code**:

- **Goal**: what should be true when it is done, and why it matters.
- **Context**: files and directories to read first, related code to imitate, project rules that apply
  (conventions, banned patterns, commit message format, throttled commands, line endings).
- **Constraints**: what it must not touch, what other agents are working on, what stays out of scope.
- **Approach hints in words**: name the pattern, the function to extend, the trap to avoid. Describe;
  do not paste finished code, diffs or full function bodies. A short snippet of an existing API
  signature or an error message is fine. Solutions are not.
- **Acceptance criteria**: concrete, checkable outcomes.
- **Verification**: the exact commands to run (tests, typecheck, build), and that it must run them and
  fix failures before reporting.
- **Report format**: files changed, commands run with pass/fail, anything it was unsure about or
  deviated on. Ask it to be honest about failures and skipped steps.

**Every brief ends with this brevity instruction**, so workers burn tokens on thinking and code,
not on talking:

> Work silently. Think and code — do not narrate. No preamble, no explaining what you're about to
> do, no restating the task, no summary of what you read, no running commentary between tool calls.
> No markdown headers, bullet-point recaps or congratulatory wrap-ups. Make the edits and run the
> commands directly. Keep your thinking private and your tool calls free of explanation. Your only
> prose is the final report, and it is terse: files changed, commands run with pass/fail, and
> anything you were unsure about or deviated on — a few lines, not an essay. If it all passed and
> there is nothing to flag, say so in one line. Skip the file contents and the diff; I read those
> myself.

Background agents are the default. Launch independent chunks together in one message, up to the cap,
and do not poll. You are notified when they finish. Do not do the same work yourself while waiting.
Reuse a worker across follow-ups with `SendMessage` when its context is still useful.

### Review and verify (you, Opus)

An agent's report is a claim, not proof.

- Read the actual diff (`git diff`, `git status`) and the touched files.
- Re-run the key verification yourself when it is cheap, or delegate a fresh Sonnet agent to run it.
- Check the result against the acceptance criteria and the project's rules.
- If it is wrong or incomplete, continue the same agent with `SendMessage` and say specifically what
  is off and what you expect. Explain the problem; do not hand over the fix. Spawn a new agent only
  when the old one's context is the problem.
- Repeat until the chunk genuinely passes, then move on.

### Finish each request

- Confirm every chunk is verified and the tree is in the state the project rules require (commits per
  chunk, tests passing, nothing forbidden staged). Have an agent do the commit if the project wants
  commits, following the project's commit-message rules.
- Report plainly: what was done, what was verified and how, what failed or was skipped, what is left.
  No overclaiming.

## Standing rules while the mode is on

- The agent cap is absolute. Count running agents before launching more.
- Sonnet does the coding and shell work. Opus plans, guides, reviews.
- No ready-made code in briefs.
- Every brief carries the brevity instruction. Workers think and code silently and report in a few
  terse lines — no narration, no recaps, no essays. Reviewing the diff yourself is how you check the
  work, not their prose.
- Destructive or outward-facing actions (force-push, deleting data, sending messages, publishing)
  are not delegated blindly. Confirm with the user first unless they already authorized it.
- Keep the user informed in short lines at phase changes, not a running commentary.
- If context is compacted, master mode and the agent cap survive it. Re-state both in one line after
  a compaction so they are not lost.
