# New-session prompts

## The prompts file

Start the file with:

    # New-session prompts: <date>

    For each block below, open a new session in the folder shown, set effort to High, and paste
    the prompt. If a block has a /goal line, run it after pasting.

Then add one block per handed-off session, in the order the handoffs finished:

    ## N. <Project>: <what the work is> (replaces "<old session title>")

    **Folder:** `<absolute folder>`
    <Only if it differs from the old session's folder, one sentence on why, for example: "That's
    the game's own repo. The old session ran from ILLEST, which is a different project.">
    **Then run:** `/goal <condition, word for word>`
    <Only when the old session had an active /goal. Otherwise write "No /goal needed.">

    ```
    <the prompt>
    ```

    ---

The folder is where the work actually lives, which isn't always the old session's folder. The
handoff's "Start here" section says which one it is.

## The prompt

Write it in the user's voice ("my", "me"), in this order:

1. "You're taking over <project> from a previous session that ran too long. It wrote a detailed
   handoff before it stopped." If the handoff file sits outside the new folder, say it's there
   only because that's where the old session ran.
2. "Read these in order, fully, before doing anything:" the handoff's absolute path first, then
   the docs the handoff says to read first (request ledgers, CLAUDE.md, plan docs). If the new
   folder differs from the old one, list the memory notes the handoff relies on, with absolute
   paths, and say they won't load automatically.
3. "Where things stand:" 3 to 6 sentences covering the branch and commit, what's finished, what's in
   progress, and anything uncommitted or temporary.
4. "Your first steps:" the handoff's first steps, numbered and concrete, detailed enough to start
   without searching.
5. "Rules:" a short list of the standing rules that are easy to break.
6. One or two sentences on how the user likes to work: autonomy, updates, questions.

Keep the prompt self-contained, but don't copy the whole handoff into it; it points to the
handoff. Never put secrets in a prompt.
