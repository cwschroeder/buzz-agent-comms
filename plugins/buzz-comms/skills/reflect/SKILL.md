---
name: reflect
description: >-
  Extract durable insights from the current session and append them to the
  project's docs/LEARNINGS.md. Use when the user invokes
  /buzz-comms:reflect, or asks to capture learnings, write down what was
  learned, or update the project memory after a work session.
---

# Reflect

Turn what this session actually established into a dated entry in
`docs/LEARNINGS.md`. Nothing is written before the user confirms the proposed
text.

This skill is the manual trigger for a duty the plugin already carries:
`buzz-team-communication` requires `docs/LEARNINGS.md` to be updated after any
significant work session. Reflect is not a second memory system. It writes to
that one file, in that file's language, under its append-only rule.

## When to run it

The user asks for it. There is no hook, no background mode, and no
configuration file. A good moment is the end of a work session, after the
result has been published and while the reasons for each decision are still in
the conversation.

## What qualifies as a learning

Keep the bar high. `docs/LEARNINGS.md` is read by every future agent on the
project, so every entry costs someone's attention.

Write it down when the session produced:

- **A verified fact** that was not obvious from the code, and that cost effort
  to establish. "The listener reloads its allowlist every two seconds, so a
  restart is unnecessary."
- **A decision with its reason.** The decision alone ages badly; the reason is
  what lets the next agent tell whether it still holds.
- **A trap.** Something that looked right, was wrong, and would catch the next
  person the same way.
- **A correction.** An earlier entry, or an earlier belief, that this session
  disproved.
- **A regression and its cause**, once the cause is actually known.

Leave it out when it is:

- Already in the file. Read the file first, every time.
- Derivable from the code, the commit history, or `AGENTS.md`/`CLAUDE.md`.
  The repository already records those.
- A description of what was done this session. That belongs in the Buzz
  lifecycle result and in `tasks/tasks.md`, not in the project memory.
- A personal preference of one user rather than a fact about the project.
  See "Personal preferences" below.
- A secret, credential, customer name, or private personal detail. These never
  go into a repository file.

An unverified hunch is not a learning. If the session ended with a suspicion,
either verify it or write it down as an open question in `tasks/tasks.md`.

## Append-only

`docs/LEARNINGS.md` keeps its history. This matters when an entry turns out to
be wrong: the wrong entry stays, and the correction is appended below it,
naming what it corrects. A future reader needs to see that the project once
believed the wrong thing, or they will rediscover it.

So there are exactly three moves:

1. **Append a new insight.**
2. **Append a correction** that names the entry it supersedes.
3. **Append a retraction** when an entry no longer holds and nothing replaces
   it.

Never edit an existing entry's meaning, never delete a line, never reorder the
file.

## Format

Match what the file already does. If it has none of this yet, use a dated
section with one bullet per insight and the agent's name:

```markdown
## 2026-03-14 - Short topic

- (claude.petra) One insight, stated so a reader who was not there can act on
  it. Name the file, the command, the measurement.
```

Rules for the text itself:

- One insight per bullet. Two insights in one bullet means the second one gets
  skimmed.
- Write in the language the file already uses. In German, use real umlauts and
  `ß`; ASCII substitutions belong only in paths, commands, and identifiers.
- Be concrete. "The API was slow" is not usable; "`POST /query` without a
  `kinds` filter is rejected with 403 by the relay's p-gate" is.
- No internal reasoning, no narration of the session.
- Run the text through the `no-ai-slop` skill before proposing it, the same as
  a channel message.

A correction names its target so the link is visible:

```markdown
- (claude.petra) Correction to the entry from 2026-03-14 on the p-gate: the
  403 also appears with a `kinds` filter when the filter is empty.
```

## How to run it

1. **Read `docs/LEARNINGS.md`.** If the project has no `docs/` directory yet,
   create the file with a short header explaining what it is. Never create a
   singular `doc/` directory; the plugin's file set uses `docs/` only.
2. **Scan this session** for the qualifying material listed above. Take the
   user's own corrections seriously: a sentence like "no, do it the other way"
   is the strongest signal in the transcript.
3. **Check each candidate against the file** so nothing is written twice, and
   so contradictions surface as corrections instead of duplicates.
4. **Show the user the proposed entries verbatim**, in the exact text that
   would be appended, and say which file they go to. If nothing qualifies, say
   that plainly and stop. An empty session is a normal outcome.
5. **On confirmation, append** and report the file and the number of entries.
   Do not commit; the user decides when and how the change lands.

If the session also produced open work, add or update the row in
`tasks/tasks.md` in the same pass, with status and date.

## Personal preferences

A preference about how the user wants to be worked with is not project memory
and does not belong in a versioned repository file. When the session produced
one, say so and offer to add it to a `CLAUDE.md` instead: the project's file
when it concerns everyone on the project, the user's own personal one when it
concerns only them. Wait for the user to choose the file. Never write to a
`CLAUDE.md` unasked.
