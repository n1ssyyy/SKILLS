# What a handoff must cover

1. **Start here.** What the project is, the repo path or paths, the branch and the head commit.
   If the work lives in a different folder from the session's own, say so, and say which folder
   the next session should open.
2. **What the user asked for.** The original request and every later instruction, quoted word
   for word where it matters, including any /goal condition. If a ledger of the user's requests
   exists (for example OWNER-REQUESTS.md), bring it up to date and point to it.
3. **The full scope as discussed.** Every feature, design choice and requirement the user asked
   for, so nothing that was agreed gets lost.
4. **What's done.** What was built or changed, and where it lives: files, modules, commits,
   branches and PRs. Say how each part was checked.
5. **In progress at handoff.** The exact state of the current item. Uncommitted changes, file by
   file. Running processes (dev servers, background tasks, preview servers), and whether the next
   session has to start or stop them. Temporary edits that must be reverted.
6. **Saved or not.** What is committed, pushed, published or deployed, and what isn't.
7. **Prioritized TODO.** For each item: where it goes, how to approach it, and what "done" looks
   like.
8. **Known issues and open questions.** Bugs, blockers and flaky tests. Questions for the user,
   and whether they were already asked.
9. **Decisions and preferences.** Decisions made and why. What the user liked, rejected, or asked
   you to always or never do.
10. **Standing rules.** Rules from the user, CLAUDE.md and memory that the next session must keep
    following.
11. **Environment.** Commands to build, test and run. Tools and MCP servers used, and their
    quirks. Helper scripts in the old scratchpad that are worth copying, with absolute paths,
    because scratchpads are temporary. If the next session opens in a different folder, the
    memory notes it should read, with absolute paths.
12. **Gotchas.** Approaches that failed and why, and things not to repeat.
13. **First steps for the next session.** The 3 to 5 concrete actions to take first.

Never write secrets (API keys, tokens, passwords) into a handoff. Say where they live instead.
