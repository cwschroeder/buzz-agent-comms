# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Claude Code **plugin marketplace** (`buzz-agent-comms`) containing one plugin
(`buzz-comms`). The plugin lets a colleague's coding agent report into the same
private Buzz project channels as the Buzz owner's own agents: one project, one
channel, one shared history, regardless of whose machine the agent runs on.

There is no compiler and no build step. The deliverable is a Python helper
(standard library only) plus markdown that instructs the agent.

Public remote: `https://github.com/cwschroeder/buzz-agent-comms`.

This repository is public. Never add real relay URLs, channel UUIDs, public or
private identity material, auth tags, customer names, proprietary project data,
internal hostnames, or local operator paths. Use synthetic examples only.

## Repository layout

```
.claude-plugin/marketplace.json          # marketplace manifest, lists the plugin
plugins/buzz-comms/
├── .claude-plugin/plugin.json           # plugin manifest (name, version, author)
├── skills/buzz-team-communication/
│   └── SKILL.md                         # the behavioural contract for the agent
├── skills/no-ai-slop/                   # vendored, MIT, Peter Yang — edits every
│   ├── SKILL.md                         #   lifecycle text before it is published
│   ├── eval.md                          #   the post-edit checklist
│   └── LICENSE                          #   keep this file with any copy
├── commands/
│   ├── buzz-setup.md                    # /buzz-comms:buzz-setup: guided onboarding
│   └── buzz-status.md                   # /buzz-comms:buzz-status: read-only diagnostics
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

Two layers with a deliberate split of responsibility:

- **`SKILL.md` and the commands** hold the *policy*: when the agent must read the
  channel, what counts as delivery proof, what must never be published. This
  prose is the contract, so treat wording changes as behaviour changes.
- **`scripts/project-buzz`** holds the *mechanics*: identity, project resolution,
  marker construction, validation, deduplication, attachments. The agent is told
  to never bypass it (no direct `buzz messages send` for lifecycle text).

### Helper anatomy

`scripts/project-buzz` is a single file, grouped in this order: regexes and
limits, config/state paths, config and identity IO, agent name and relay,
binary resolution, `buzz` invocation, project resolution, validation, marker
building, `publish`/`publish_attachments`, then one `command_*` function per
subcommand, then the argparse wiring. Keep new code in the matching group.

Subcommands: `install`, `provision`, `register`, `resolve`, `context`,
`start`/`progress`/`blocked`/`result`, `attach`, `doctor`.

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
their **own** Buzz human key via NIP-OA. No private key is ever shared; only the
agent's public key is exchanged. The relay grants access because the owner is a
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
  `[AGENT-ACTIVITY:progress|blocked:<agent>:<id>]`,
  `[AGENT-RESULT:<agent>:<id>]`. Note that `start` maps to `started`.
- **Content validation.** Caller content is 1 to 4000 characters and cannot
  contain `[PILOT-` or `[AGENT-`. Before publishing text with an at-sign, the
  helper resolves current channel profiles and rejects only real identity
  mentions outside code regions. If profiles cannot be resolved, it fails
  closed. Technical text such as `@media`, package scopes, documentation tags,
  and email addresses remains valid.
- **Agent name shape.** `<client>.<person>`, lowercase, from config only, never a
  caller argument. A bare `claude` would be charged to the owner's seat ledger.
- **Deduplication.** The lock directory is the mutex; a failed publish must
  release it so the documented same-ID retry works.
- **Attachments are top-level** and carry no lifecycle marker. Never fold them
  into the collapsible lifecycle thread.
- **Fail closed.** An unregistered workspace or unknown repo id is an error;
  never fall back to a neighbouring channel.
- **No crypto here.** Signing happens inside the `buzz` CLI. The helper must
  never implement crypto and never print private key material, not even on error.

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
- **Version bumps touch both manifests**: `.claude-plugin/marketplace.json` and
  `plugins/buzz-comms/.claude-plugin/plugin.json` must stay in sync.
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
- `README.md` is German: it addresses the colleague and the Buzz owner
- `SKILL.md`, the command markdown and the helper's comments are English: they
  address the agent and sit next to English tooling

### Versioning
- Semantic version without a `v` prefix (`0.2.0`, not `v0.2.0`)
- Marketplace and plugin manifest carry the same version

### Plans
- Implementation plans are stored in the `/plans` directory

**⚠️ IMPORTANT**: Never amend existing commits (`git commit --amend`). Always
create new commits instead.
