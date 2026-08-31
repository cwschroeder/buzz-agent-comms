---
name: handoff
description: >-
  Write a handover note before a session ends or its context is compacted, so
  the next session resumes instead of rediscovering. Use when the user invokes
  /buzz-comms:handoff, when the context window is close to compaction, or when
  a session ends with work still open.
---

# Handoff

Write the note yourself, while you still have the whole session in context. An
automatic summary is written by something that never did the work; it keeps the
topics and loses the traps.

## When to write one

- The user asks for a handover.
- The context window is approaching compaction. Write the note first, then keep
  working. After compaction it is too late; the material is gone.
- The session ends with work that is not finished.

A session that ends with nothing open still deserves one line saying so. That
is a valid note, and it saves the next session from looking for unfinished
business that does not exist.

## Where it goes

`~/.agents/handoff/<agent>/YYYY-MM-DD-HHMM-<topic>.md`, where `<agent>` is the
lowercase client name used in Buzz lifecycle messages (`claude`, `codex`,
`pi`, ...). Create the directory if it is missing.

Outside the repository on purpose. The note is session state, not project
knowledge, and it would be noise in every colleague's diff.

## What it is not

Three files already exist and each owns something else. Do not duplicate them:

| Where | What belongs there |
|---|---|
| `docs/LEARNINGS.md` | Durable project knowledge, for everyone, forever. See the `reflect` skill. |
| `tasks/tasks.md` | The task and its status, for everyone. |
| The Buzz channel | The verified result or the concrete blocker, for everyone. |
| The handoff note | What only you know right now: where you stopped, what nearly worked, which wrong turn to skip. |

If an insight belongs in the project memory, put it in `docs/LEARNINGS.md`
instead. The handoff note is read once, by your next session, and then it is
stale.

## What goes in it

Ten to thirty lines, written as prose, not as a filled-in form:

- **Task and state.** What was the goal, what is verifiably finished. Finished
  means checked, not written.
- **Open.** What is missing, and in which order it makes sense to continue.
- **Traps.** What the next session needs in order not to repeat your mistakes:
  paths, assumptions that turned out wrong, quirks of the environment, a test
  that fails for an unrelated reason.
- **Evidence.** The test command, the relevant files, the Buzz thread root if
  there is one.

Be honest about what is unverified. A note that reports something as finished
when it was never checked costs more than no note at all. Never write
credentials, customer data, or private personal detail into it; the same rule
that governs channel messages governs this file.

## Reading one on wake-up

At the start of a session in a project you have worked on before, read your
newest note under `~/.agents/handoff/<agent>/` when it is less than a week old
and matches the current work. It is your own diary, not someone else's mail.
Mention what you took from it, so the user knows what you are building on.
