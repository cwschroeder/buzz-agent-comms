# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Claude Code **plugin marketplace** (`buzz-agent-comms`) containing one plugin
(`buzz-comms`). The plugin applies a shared engineering contract and lets a
colleague's coding agent report into the same private Buzz project channels as
the Buzz owner's own agents: one project, one channel, one shared history,
regardless of whose machine the agent runs on.

There is no compiler and no build step. The deliverable is a Python helper
(standard library only) plus markdown that instructs the agent.

Public distribution mirror: `https://github.com/cwschroeder/buzz-agent-comms`.

Development does not happen on that GitHub mirror. The Burglengenfeld
development office uses its internal GitLab project. Approved external
developers use the private repository on Buzz's integrated Git server with
NIP-98 authentication and NIP-34 issues, patches and merge requests. The
maintainer mirrors released versions to GitHub for Marketplace installation and
updates.

This repository is public. Never add real relay URLs, channel UUIDs, public or
private identity material, auth tags, customer names, proprietary project data,
internal hostnames, or local operator paths. Use synthetic examples only.

## Workflow: direkt auf main

Dieses Repository nimmt den Opt-out aus dem `engineering-contract`, Abschnitt
"Repositories that opt out". Änderungen gehen ohne Worktree und ohne Merge
Request direkt auf `main`.

Der Grund: das Plugin trägt die Regeln für alle anderen Projekte. Eine
Regelkorrektur, die einen Tag im Review liegt, ist einen Tag lang eine falsche
Regel bei jedem Kollegen. Die Umlaufzeit wiegt hier schwerer als das
Vier-Augen-Prinzip.

Was trotzdem gilt:

- Die Testsuite läuft vollständig und grün, bevor gepusht wird.
- Commits sind einzeln, signiert (`git commit -s`) und auf eine Änderung
  begrenzt.
- Versionssprünge treffen alle drei Stellen.
- Der öffentliche Marketplace ist ein eigener Schritt mit eigener Prüfung, kein
  Nebeneffekt des Pushs. Er wird nur auf ausdrückliche Ansage nachgeführt.
- Wer nicht Maintainer dieses Repos ist, arbeitet weiter über Branch und Merge
  Request.

## Repository layout

```
.claude-plugin/marketplace.json          # marketplace manifest, lists the plugin
plugins/buzz-comms/
├── .claude-plugin/plugin.json           # plugin manifest (name, version, author)
├── skills/engineering-contract/
│   └── SKILL.md                         # worktrees, roles, UI and customer-data policy
├── skills/buzz-team-communication/
│   └── SKILL.md                         # the behavioural contract for the agent
├── skills/no-ai-slop/                   # vendored, MIT, Peter Yang, edits every
│   ├── SKILL.md                         #   lifecycle text before it is published
│   ├── eval.md                          #   the post-edit checklist
│   └── LICENSE                          #   keep this file with any copy
├── skills/show-me/                      # compact visuals for channel posts
│   └── SKILL.md                         #   comparisons and rendered media
├── skills/bro/                          # vendored MIT luchasarie/bro-skill
│   ├── SKILL.md                         #   /bro: plain-language re-explainer
│   └── LICENSE                          #   keep this file with any copy
├── skills/ponytail-review/              # bounded over-engineering review
│   ├── SKILL.md                         #   one-shot and read-only
│   └── LICENSE                          #   MIT, DietrichGebert/ponytail
├── skills/reflect/                      # session learnings into the project
│   └── SKILL.md                         #   memory, append-only, on request
├── skills/handoff/                      # handover note before the context
│   └── SKILL.md                         #   is compacted or the session ends
├── skills/c4-model/                     # vendored MIT, Cherif Toujeni
│   ├── SKILL.md                         #   C4 levels, modes, examples
│   ├── LICENSE                          #   keep this file with any copy
│   └── *.md                             #   mode and reference companions
├── skills/arc42-documentation/          # vendored MIT, Melodic Software
│   ├── SKILL.md                         #   the 12 arc42 sections
│   └── LICENSE                          #   keep this file with any copy
├── commands/
│   ├── buzz-setup.md                    # /buzz-comms:buzz-setup: guided onboarding
│   ├── buzz-status.md                   # /buzz-comms:buzz-status: read-only diagnostics
│   ├── bro.md                           # /bro: plain-language re-explainer
│   ├── ponytail-review.md               # explicit simplification review
│   ├── reflect.md                       # /buzz-comms:reflect: session learnings
│   └── handoff.md                       # /buzz-comms:handoff: handover note
├── scripts/project-buzz                 # the deterministic helper (Python 3.8+)
└── tests/test_project_buzz.py           # unittest suite, runs without a relay
README.md                                # operator and colleague documentation (German)
```

## Commands

```bash
# Run the test suite (no relay needed, uses a fake buzz binary)
python -m unittest discover -s plugins/buzz-comms/tests

# Run a single test class or case
python -m unittest discover -s plugins/buzz-comms/tests -k MarkerFormat
python -m unittest discover -s plugins/buzz-comms/tests -k test_bare_client_name_is_rejected

# Syntax check the helper
python -m py_compile plugins/buzz-comms/scripts/project-buzz
```

The expected test count is documented by the current test run. On Windows, two
pure POSIX cases are skipped: permission bits on the identity file and absence
of the `.cmd` launcher.

Use `python`, not `python3`, when running anything on Windows. See
"Windows specifics" below.

## Architecture

Three policy surfaces and one mechanics layer have separate responsibilities:

- **`skills/engineering-contract/SKILL.md`** holds the shared development
  contract: worktrees, contributor merge requests, maintainer-only merges and
  deployments, infrastructure ownership, cohesive simplicity, Impeccable UI
  work, and local AI for customer data. The optional `ponytail-review` skill
  inspects a requested diff for avoidable complexity without editing it or
  replacing normal review gates.
- **`skills/buzz-team-communication/SKILL.md` and the commands** hold the Buzz
  policy: when the agent must read the
  channel, what counts as delivery proof, what must never be published. This
  prose is the contract, so treat wording changes as behaviour changes. Two
  advisory skills shape every publication: `no-ai-slop` edits the prose, and
  `show-me` selects comparisons, screenshots or rendered diagrams when they help
  the reader. Preserve useful lists and tables in the plain-language edit.
  `bro` rides along as a vendored general quality-of-life skill: `/bro`
  re-explains the previous answer in plain language, it has no lifecycle role.
  `reflect` serves the `docs/LEARNINGS.md` duty that
  `buzz-team-communication` already states: `/buzz-comms:reflect` proposes
  dated entries for the session and appends them once the user confirms. It
  ships without a hook and without a configuration file on purpose. `Stop`
  fires after every assistant turn rather than at the end of a session, and
  `SessionEnd` cannot hand anything back to the model, so an automatic variant
  would reflect after every single answer on every colleague's machine. The
  same reasoning kept modes and permanent hooks out of `ponytail-review`.
  `handoff` covers the other half of session memory: `/buzz-comms:handoff`
  writes what only the current session knows, outside the repository, before a
  compaction takes it. Its skill states the boundary against
  `docs/LEARNINGS.md`, `tasks/tasks.md` and the channel, so the four do not
  become four competing memories.
- **`scripts/project-buzz`** holds the *mechanics*: identity, project resolution,
  marker construction, validation, deduplication, attachments. The agent is told
  to never bypass it (no direct `buzz messages send` for lifecycle text).

### Helper anatomy

`scripts/project-buzz` is a single file, grouped in this order: regexes and
limits, config/state paths, config and identity IO, agent name and relay,
binary resolution, NIP-OA key material, `buzz` invocation, project resolution,
validation, marker building, `publish`/`publish_attachments`, then one
`command_*` function per subcommand, then the argparse wiring. Keep new code in
the matching group.

The file is installed by copying it, so it must stay one file with no imports
beyond the standard library.

Subcommands: `install`, `provision`, `register`, `resolve`, `context`, `open`,
`start`/`progress`/`blocked`/`result`, `correct`, `attach`, `doctor`.

### Local state

Everything lives under `~/.config/buzz-agent`, overridable with
`BUZZ_AGENT_HOME`:

- `config.json` - relay URL, agent name, binary paths, project mapping
- `identity.json` - agent key pair and auth tag (mode 600 on POSIX)
- `state/publishes/<repo>-<agent>-<phase>-<update-id>.lock/output.json` -
  deduplication markers holding the stored publish result

The helper is installed to `~/.config/buzz-agent/bin/project-buzz` by
`project-buzz install`, so nothing at runtime depends on where the plugin sits.
Docs and skill must always reference the installed path, never the plugin path.

### Identity model

Each colleague generates their own agent key pair locally and attests it to
their **own** Buzz human key via NIP-OA. Both steps happen inside the helper
process, so no extra binary is needed and the owner key never reaches a child
process. The owner key is accepted as `nsec1...` or as 64 hex characters. No
private key is ever shared; only the agent's public key is exchanged. The relay grants access because the owner is a
relay member (`BUZZ_REQUIRE_RELAY_MEMBERSHIP` plus `BUZZ_ALLOW_NIP_OA_AUTH`).

Relay access is not channel access: the Buzz owner must additionally add the
agent's public key to each project channel (`channels add-member`).

Channel convention: every project channel is named `<repo-id>-agent`. The helper
discovers it from that; a deviating channel needs an explicit
`register --channel <uuid>`.

## Invariants

The helper mirrors the owner-side pilot helper wire protocol. Messages from a
colleague's machine must be indistinguishable in shape from the owner's. Do not
change these without changing the owner side in lockstep:

- **Marker format.** `[AGENT-ACTIVITY:started:<agent>:<id>]`,
  `[AGENT-ACTIVITY:progress|blocked|correction:<agent>:<id>]`,
  `[AGENT-RESULT:<agent>:<id>]`. Note that `start` maps to `started` and
  `correction` is a closing phase like `result` and `blocked` (posted
  top-level, supersedes an earlier event).
- **Content validation.** Caller content is 1 to 16000 characters and cannot
  contain `[PILOT-` or `[AGENT-`. Before publishing text with an at-sign, the
  helper resolves current channel profiles and rejects only real identity
  mentions outside code regions. If profiles cannot be resolved, it fails
  closed. Technical text such as `@media`, package scopes, documentation tags,
  and email addresses remains valid.
- **German prose validation.** Common German ASCII substitutions are rejected
  outside inline code, fenced code, URLs, and Markdown block quotes. Paths and
  technical identifiers must use code formatting. Keep this boundary
  deterministic and cover it with examples from real Buzz regressions.
- **Secret validation.** Common credential shapes (`nsec1...`, `sk-...`,
  `ghp_...`/`github_pat_...`, `xox...`, `AKIA...`, `Bearer <token>`, and
  `key: <value>` assignments of at least 16 characters) are rejected before
  any publish. Keep every pattern small, documented, and covered by a test;
  the guard is a safety net, not an exhaustive secret detector.
- **CLI timeouts.** `run_buzz` times out after a bounded number of seconds
  (default 60, `BUZZ_AGENT_CLI_TIMEOUT_SECONDS` for tests). A hung CLI raises
  `UserError`; it must never hang the agent.
- **Agent name shape.** `<client>.<person>`, lowercase, from config only, never a
  caller argument. A bare `claude` would be charged to the owner's seat ledger.
- **Deduplication.** The lock directory is the mutex; a failed publish must
  release it so the documented same-ID retry works.
- **Attachments are top-level** and carry no lifecycle marker. Never fold them
  into the collapsible lifecycle thread.
- **Fail closed.** An unregistered workspace or unknown repo id is an error;
  never fall back to a neighbouring channel.
- **Crypto only for provisioning.** Event signing happens inside the `buzz` CLI.
  The single exception is the agent key pair and the NIP-OA owner attestation,
  which the helper builds itself so a colleague needs no extra binaries for
  their platform. That code stays in the "NIP-OA key material" section, uses
  only `hashlib` and `secrets`, verifies every signature before returning it,
  and is pinned by the published BIP-340 vectors plus a tag produced by the
  Rust reference. Do not grow it: anything beyond provisioning belongs in the
  `buzz` CLI. The helper must never print private key material, not even on
  error, and must never pass a key on a command line.
- **The NIP-OA preimage is a protocol contract.**
  `"nostr:agent-auth:" + agent_pubkey_hex + ":" + conditions`, SHA-256, signed
  BIP-340. It must match `buzz-sdk`'s `nip_oa` exactly; changing it invalidates
  every identity already granted on a relay.

## Editing rules

- **Python 3.8 compatible, standard library only.** No third-party imports, no
  `match`, no PEP 604 unions at runtime (the file uses
  `from __future__ import annotations` plus `typing`).
- Operator-fixable problems raise `UserError`, which is reported without a
  traceback. Reserve exceptions for real bugs.
- Platform behaviour goes through the `is_windows()` seam so tests can exercise
  both paths. Do not scatter `os.name` checks.
- Every behavioural change to the helper needs a test in
  `tests/test_project_buzz.py`. The suite must keep running without a relay.
- **Version bumps touch three places**: `.claude-plugin/marketplace.json`,
  `plugins/buzz-comms/.claude-plugin/plugin.json` and `HELPER_VERSION` in
  `scripts/project-buzz`. The drift test fails on any of the three, and the
  helper is the one that gets forgotten.
- Never invent download URLs, package versions or checksums. This repository
  does not distribute Buzz binaries.

## Windows specifics

This repo is developed on Windows, so Windows must keep working.

- **Never call the helper bare.** The shebang resolves `python3`, which on stock
  Windows is the Microsoft Store placeholder and dies with "Python wurde nicht
  gefunden". Working invocations:

  ```bash
  python ~/.config/buzz-agent/bin/project-buzz <command>   # Git Bash
  project-buzz.cmd <command>                               # cmd / PowerShell
  ```

  `install` writes that `.cmd` launcher next to the helper.
- **`provision` does not prompt under Git Bash.** mintty hands Python a pipe, so
  `sys.stdin.isatty()` is false and the hidden prompt never opens. Run it from
  cmd or PowerShell, prefix with `winpty`, or set `BUZZ_OWNER_PRIVATE_KEY` for
  that single call.
- POSIX permission checks on the identity file are skipped on Windows, because
  `os.stat` reports `0o666` there for every file. The user profile directory is
  the protection instead.
- In the tests the fake `buzz` binary is a `.cmd` shim in front of a `.py` file,
  because Windows executes neither a shebang nor an extensionless file
  (`WinError 193`).
- **Reserved filenames**: never create files named nul, con, prn, aux, com1-9 or
  lpt1-9. They are invalid on Windows.

## Conventions

### Commit messages
- **All commit messages must be written in English**, subject and body
- Conventional Commits with a scope where it helps: `feat(windows): …`,
  `fix(provision): …`, `docs: …`, `fix(tests): …`
- The older commits in this repository have German subjects. That is legacy, not
  a template: do not take the language from `git log`, and never rewrite existing
  commits to align them

### German umlauts
- German text anywhere in this repository must use **real umlauts**:
  `ä ö ü Ä Ö Ü ß`
- Never transliterate them, and convert any transliteration you encounter:
  `ae` to `ä`, `oe` to `ö`, `ue` to `ü`, `ss` to `ß` (no `Gueltigkeit`,
  no `ueberschreiben`, no `Schluessel`)
- Applies to everything: README, skill and command markdown, Python comments and
  docstrings, console and log output, commit subjects and bodies
- If umlauts arrive garbled, fix the encoding instead of rewriting the words:
  write files as UTF-8, use `git commit -F <utf8-file>` instead of `-m`, and
  `-Encoding utf8` for PowerShell output

### No en dashes or em dashes
- Never use `–` (en dash) or `—` (em dash). Not in chat replies, not in files,
  code comments, docstrings, console output or commit messages
- Use a plain hyphen, a comma, a colon, parentheses, or a separate sentence
  instead

### Documentation language
- `README.md`, `SECURITY.md` and the vendored `no-ai-slop` files are German.
  `no-ai-slop` defaults to German for German input and project context, while it
  keeps English checks for English output.
- Other `SKILL.md` files, command markdown and helper comments are English: they
  address the agent and sit next to English tooling.

### Versioning
- Semantic version without a `v` prefix (`0.2.0`, not `v0.2.0`)
- Marketplace and plugin manifest carry the same version

### Plans
- Implementation plans are stored in the `/plans` directory

**⚠️ IMPORTANT**: Never amend existing commits (`git commit --amend`). Always
create new commits instead.
