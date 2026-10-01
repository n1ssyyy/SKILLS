# Handoff request sent to another session

Fill in the placeholders, then append the full text of checklist.md under "Checklist:". Send it
as one message. The first line is all the user sees in the preview, so keep it as it is.

- {{FROM}}: this session's title.
- {{PATH}}: the handoff file's absolute path.
- {{TRANSCRIPT}}: the target's transcript path, from session_info.py. If none was found, drop
  step 3's command and keep only its first sentence.
- {{SKILL_DIR}}: this skill's folder.
- {{INTERRUPTED}}: use the sentence below if you will stop the target's current turn; otherwise
  delete the line.
  "Your previous turn was stopped so this request could run now. Record exactly where that work
  stood when it stopped."
- {{GOAL_NOTE}}: use the sentence below if the target has an active /goal; otherwise delete the
  line.
  "This session has an active /goal: "<condition word for word>". It will be stopped once the
  handoff is complete. Don't try to meet the goal first. Record it word for word so the next
  session keeps working toward it."

---

Handoff request from the "{{FROM}}" session, sent for the user: write a detailed handoff so a fresh session can take over this work.

Why: the user is moving long-running sessions into fresh ones. Very long contexts make work slow, and details get lost.
{{INTERRUPTED}}

Do this in order:
1. Don't start new work. If a short step is in flight and safe to finish, finish it. Otherwise record exactly where it stands.
2. Save the work the way this project normally does. If its rules say to commit finished chunks, commit them. Don't push, publish or deploy anything you weren't already going to as part of the task. Record exactly what is and isn't saved, committed and pushed.
3. Quote the user exactly. If your context was compacted, recover their messages word for word with:
   python "{{SKILL_DIR}}/scripts/user_messages.py" "{{TRANSCRIPT}}"
4. Write the handoff to exactly this path: {{PATH}}
   Cover everything in the checklist below. Someone with no memory of this conversation must be able to continue properly from it alone. Point to other docs rather than copying them, but make this file the single place to start. It isn't part of the project, so don't commit it.
5. Make the very last line of the file exactly:
   <!-- HANDOFF COMPLETE -->
   Write that line only when the document is finished. It's the signal that the handoff is done.
6. Reply with a short summary and end your turn. Don't start new work after the handoff, and don't run the /handoff skill yourself.
{{GOAL_NOTE}}

Checklist:
