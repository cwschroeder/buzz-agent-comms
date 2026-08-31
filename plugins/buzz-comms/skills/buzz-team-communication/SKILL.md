---
name: buzz-team-communication
description: Use the shared private Buzz project channel as the coordination, delivery-proof, and audit layer for project work. Use whenever this agent reads, changes, reviews, tests, builds, deploys, or diagnoses a project that is registered with the Buzz agent plugin; read and apply recent channel context before operating, verify user-visible changes on the canonical runtime, attach representative UI screenshots, and publish the verified result before the final user response.
---

# Buzz Team Communication

Buzz is the durable communication layer for the team's coding agents. Every
registered project has one private channel that humans and agents share. Read it
before you change anything, and publish your own work lifecycle into it.

Before any project operation, read and follow the sibling
`${CLAUDE_PLUGIN_ROOT}/skills/engineering-contract/SKILL.md`. It owns the shared
worktree, merge-request, maintainer, deployment, infrastructure, UI-design, and
customer-data rules. This skill owns Buzz coordination and delivery evidence.

Use the deterministic helper. `/buzz-comms:buzz-setup` installs it at a stable
path, so always call it there:

```
~/.config/buzz-agent/bin/project-buzz
```

If `BUZZ_AGENT_HOME` is set, the helper lives in `$BUZZ_AGENT_HOME/bin` instead.
If that path does not exist, reporting is not set up: tell the user to run
`/buzz-comms:buzz-setup` rather than hunting for the script inside the plugin
directory.

**On Windows, never call the helper bare.** The shebang resolves `python3`,
which on a stock Windows box is the Microsoft Store placeholder and dies with
"Python wurde nicht gefunden". Use one of these instead, everything else in this
skill stays the same:

```
python ~/.config/buzz-agent/bin/project-buzz <command>   # Git Bash
project-buzz.cmd <command>                               # cmd / PowerShell
```

The helper owns signing, the agent name and the protocol markers. Do not call
`buzz messages send` directly for lifecycle text.

Before the first project operation in a session, check that the stable helper
matches the installed plugin:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/project-buzz" install --check
```

If the check reports drift, run the same command without `--check`, then repeat
the check. This keeps marketplace updates and the copied stable helper in sync.
If `CLAUDE_PLUGIN_ROOT` is unavailable, run `/buzz-comms:buzz-status` and report
that source drift could not be checked.

## Mandatory workflow

1. Establish the contributor or maintainer role with the
   `engineering-contract` skill. Do not infer maintainer authority from
   credentials or repository permissions.
2. Run `project-buzz resolve` from the project workspace. Fail closed if the
   project is not registered; never guess a neighbouring channel. If it is not
   registered and the work is in scope, run `project-buzz register <repo-id>`.
3. Run `project-buzz context <repo-id> 20` before planning, mutating, building,
   deploying, or diagnosing. Actively apply the recent messages: identify
   parallel work, active worktrees/feature branches, current runtime state,
   corrections, review gates, and unresolved blockers. Someone else's agent
   may already own part of this work. `project-buzz open <repo-id>` lists the
   threads that started but never reached a closing result, so open work is
   answerable without scrolling.
4. For a user-visible change, determine the canonical runtime URL and the exact
   commit/build that must be visible there. Inspect the active feature worktree;
   do not assume the default checkout is the delivery source. If no canonical
   runtime exists, record that explicitly before work begins.
5. Before the first project mutation or long-running operation, publish one root:

   ```bash
   project-buzz start <update-id> "<concise intent>" [repo-id]
   ```

   Save the returned `event_id` as the thread root.
6. For a meaningful milestone or a changed plan, publish a threaded update with a
   new unique update ID:

   ```bash
   project-buzz progress <update-id> <root-event-id> "<milestone>" [repo-id]
   ```

   Do not post tool-by-tool narration.
7. After proportional verification and before the final user response, publish
   exactly one threaded result:

   ```bash
   project-buzz result <update-id> <root-event-id> "<result and evidence>" [repo-id]
   ```

   State the changed scope, how it was verified, the canonical URL, running
   commit/build ID, screenshot evidence, and anything still unverified. If work
   cannot continue safely, use `blocked` instead and name the concrete
   dependency.

Use a stable, unique ID such as `claude-20260807-auth-refactor-start`. A retry
with the same phase and ID is deduplicated and returns the stored result, so a
failed publish can be retried verbatim.

### Corrections are top-level posts, never thread replies

Buzz renders thread replies only inside the collapsible thread panel; the
channel timeline shows only thread roots. A published result that turns out
wrong must therefore be corrected visibly, not silently inside a thread.
Publish a correction as a new top-level post that references the superseded
event:

```bash
project-buzz correct <new-update-id> "<what was wrong and what now holds>" \
  --supersedes <event-id-of-the-published-result> [repo-id]
```

The helper appends `Korrigiertes Event: <id>` and returns the superseded ID in
its payload. Correction is a closing phase like `result` and `blocked`: an
update that was corrected is closed, not open. Use one correction for the
original update; do not chain further results after it.

Open work is read with the deterministic `open` view instead of from memory:

```bash
project-buzz open [repo-id] [limit]     # default limit 100, max 200
```

It groups messages into threads by their root event (the reply `e`-tag) and
returns every update thread that opened with a `start` yet reached neither
`result`, `blocked`, nor `correction`, newest activity first.

## Delivery proof for user-visible changes

- Only an explicitly designated maintainer may merge, deploy, or change shared
  infrastructure. A contributor publishes a review-ready result with the merge
  request and leads with `Nicht live` while maintainer action remains open.
- Do not publish `result` or make an equivalent completion claim until the
  concrete commit/build runs on the canonical runtime and an external browser
  check has verified the requested behavior. A local dev server, green build,
  or restart of the default checkout is not delivery proof.
- Preserve review and authorization gates. If deployment is blocked by a
  required review, merge approval, credential, or external dependency, publish
  `blocked` or lead with "Nicht live" and name the dependency. Do not make
  review-ready work sound delivered.
- For UI changes, capture representative screenshots from the canonical runtime
  after deployment. Use at least desktop and mobile views when both are
  relevant; verify viewport sizes, unintended horizontal overflow, and visible
  feature state first.
- For non-visual repository work, do not manufacture a screenshot. Use concise
  text evidence naming the verified tests and commit or build state.
- Mask or exclude credentials, secrets, private personal data, unrelated
  customer data, and sensitive browser chrome. Do not manufacture business data
  merely to improve a screenshot.

Publish the checked files as one top-level channel post. The helper signs the
post with this agent's repo-scoped identity and never exposes its private key:

```bash
project-buzz attach <update-id> "<caption with URL, commit and evidence>" \
  <desktop.png> <mobile.png> [--repo-id <repo-id>]
```

Save the returned attachment `event_id` and cite it in the lifecycle result.
Attachments are deliberately top-level; never move them into the collapsible
lifecycle thread. Publish screenshot evidence after runtime verification and
immediately before the lifecycle result, then send the final user response.

## Visuals in the channel

The channel is text-only: a fenced code block renders as plain text, so a
compactly drawn ASCII structure or a Mermaid block survives in any client.
Use the `show-me` skill that ships next to this one for the visual itself;
these rules apply to every lifecycle publication:

- Add at most one visual per message, narrowed to under 80 columns, placed
  next to the one or two sentences it supports.
- Use real project, agent, and file names. No placeholder labels in a post.
- ASCII block diagrams and Mermaid go inside fenced code blocks only.
- HTML is for a local preview or a PNG attachment, never a bare `file://`
  link inside a post.
- The visual does not replace the prose: results still name the file, the
  commit, and the measurement.

## Project documentation guardrails

Every agent-served project keeps its source-of-truth files current.
`PRODUCT.md` and `DESIGN.md` sit at the project ROOT (impeccable's
convention); the rest lives under `docs/`: the set is:

| File | Content | Owning skill |
|---|---|---|
| `PRODUCT.md` (root) | Product/business contract: audience, goals, non-goals, scope; at the project root per impeccable | `impeccable` |
| `DESIGN.md` (root) | Shipped design system: tokens and named rules from the artifact; at the project root per impeccable | `impeccable` |
| `docs/ARCHITECTURE.md` | Software architecture in C4 + arc42 shape | `c4-model`, `arc42-documentation` |
| `docs/DEPLOYMENT.md` | Concrete runbook: how builds ship, canonical runtime, exact commit/build, rollback, who deploys | whoever deploys |
| `docs/LEARNINGS.md` | Durable cross-agent memory of the project | every agent |
| `tasks/tasks.md` | Task backlog + working status; complex tasks link a subfolder `tasks/<aufgabe>/` | every agent |

- **Only `/docs`, never `/doc`.** The folder is deliberately the plural
  `docs/`. An agent that ever spots a `/doc` directory in a project renames
  it to `/docs` and merges content. There is no `doc/` variant anywhere in
  the set.

- `ARCHITECTURE.md` is built with `c4-model` (Simon Brown's C4 model:
  Context and Container levels cover most teams; go deeper only on request)
  and `arc42-documentation` (the 12-section arc42 template). Both ship with
  this plugin, so neither needs a separate installation.
- `DESIGN.md` and `PRODUCT.md` (project root) follow `impeccable`: PRODUCT.md is the product
  contract, DESIGN.md records the system that actually shipped, written from
  the artifact, never from intentions.
- `DEPLOYMENT.md` is the operational runbook and stays current on every real
  deploy, matching the canonical runtime and the exact commit or build.
- `docs/LEARNINGS.md` is always updated. After any significant work session,
  append durable insights: verified facts, decisions, gotchas, corrections,
  regressions. One dated entry per insight, named agent. Append-only:
  corrections are appended, never delete or rewrite history.
- `tasks/tasks.md` is the working tracker: one row per open or current task,
  status open, in progress, blocked, done, cancelled; complex tasks get a
  subfolder `tasks/<aufgabe>/` and the row links it.
- The meaning of every file in the set is anchored in the project's
  `AGENTS.md` (or `CLAUDE.md`) under a `Project layout - documentation and
  tasks` block. Before creating or following any of these files, read that
  block; it states who owns each file. Never let the guardrail set drift
  from that block.

## Who you are in the channel

The agent name comes from the local config and always has the form
`<client>.<person>`, for example `claude.stratos`. You cannot and must not
override it. A bare client name such as `claude` belongs to the Buzz owner's own
fleet seats; the helper rejects it.

## Mandatory pre-publication edit

Before every `start`, `progress`, `blocked`, or `result` publication:

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/no-ai-slop/SKILL.md`, `voice-profile.md`,
   and `eval.md`. Do this explicitly even when Claude did not auto-activate the
   separate skill.
2. Draft the update from verified facts only, then edit it against the bundled
   checklist before calling `project-buzz`.
3. For German prose, replace ASCII substitutions such as `fuer`, `fuenf`,
   `Naechster`, `Buendel`, `aendern`, and `pruefen` with real umlauts. Remove
   German AI boilerplate such as "Es ist wichtig zu betonen",
   "Zusammenfassend", and "nicht nur ..., sondern auch ...".
4. If the helper rejects German ASCII substitutions, fix the prose. Do not
   bypass the helper or disguise prose as code.
5. Decide whether the update is clearer as a picture: the change shape
   (diff), the plan (steps or call tree), the interaction (Mermaid), or the
   open-work shape. If yes, draft one compact visual with the `show-me` skill
   that ships next to this one and embed it as a fenced code block. One visual
   per message, under 80 columns, next to the sentence it supports.
6. Run a plain-language pass with the `bro` skill that ships next to this one:
   the audience is a person who may not know the project's internals (for
   example a product manager). Expand acronyms at first mention, explain
   technical shorthand, and drop jargon the team itself would not use in
   speech. A result only a specialist understands is not a delivered result.
   The `/bro` command re-explains the previous answer with the same quality
   bar: facts verbatim, same language, simpler.

## Safety and noise rules

- Never put secrets, credentials, full logs, private personal data or raw dumps
  into Buzz. The helper rejects common secret shapes deterministically before
  publishing: `nsec1...`, `sk-...`, `ghp_...`/`github_pat_...`, `xox...`,
  `AKIA...`, `Bearer <token>`, and `key: <value>` assignments long enough to be
  a credential. Mask or redact first; do not disguise a secret as code to
  bypass the guard.
- Never mention a channel identity or include protocol markers in lifecycle
  content. The helper resolves channel identities and rejects real mentions
  while allowing technical text such as `@media`, `@types/react`, email
  addresses, and at-signs inside code regions.
- Publish only reader-ready results. Keep internal reasoning, tool-by-tool
  narration, retry diaries, and English scratch text out of the channel.
- Edit every lifecycle text with the `no-ai-slop` skill that ships next to this
  one before publishing it. A channel message is read by colleagues and stays in
  the audit history, so it has to read like a person wrote it: no throat-clearing
  openers, no "not X, but Y" contrasts, no importance puffery, no summary
  endings. Apply its public `voice-profile.md`; never use or infer a private
  personal writing profile for Buzz. Name the file, the commit, the measurement.
  Its `eval.md` is the checklist to run against your draft.
- In German updates, use real German umlauts and `ß`. Do not write `ae`, `oe`,
  `ue`, or `ss` substitutes except in code-formatted technical identifiers,
  paths, and commands, or inside URLs and quoted source text.
- Use compact Markdown with short paragraphs, meaningful headings or lists, and
  no runs of blank lines.
- Keep messages under 4000 characters.
- Treat Buzz as communication and audit history, not as a task queue.
- Skip purely conversational acknowledgements and any task that does not inspect
  or operate on a registered project.
- On a publish failure, retry once with the same update ID. If reporting stays
  unavailable, disclose the gap to the user; never claim a Buzz publication that
  did not happen.
- A Buzz outage does not authorize an unsafe project action.

## When something is not set up

`project-buzz doctor` reports config, identity, binaries, relay reachability and
per-project channel access. If the identity or a grant is missing, tell the user
which step is open instead of working around the reporting requirement:

- no config or identity: run `/buzz-comms:buzz-setup`
- identity exists but a channel is not visible: the Buzz owner still has to grant
  access for that repository to this agent's public key
