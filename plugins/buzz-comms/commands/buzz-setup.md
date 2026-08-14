---
description: Set up this machine to report agent work into the team's Buzz project channels
---

Walk the user through setting up Buzz agent reporting on this machine. Work
through the steps in order and stop at the first one that fails, telling the user
exactly what is missing.

## 0. Install the helper at a stable path

Locate the helper inside this plugin. Try `${CLAUDE_PLUGIN_ROOT}/scripts/project-buzz`
first; if that path does not resolve, find it with
`ls ~/.claude/plugins/*/*/buzz-comms/scripts/project-buzz` or an equivalent search.

Then install it so nothing later depends on the plugin directory:

```bash
<found-path> install
```

Confirm that the copied helper matches this plugin version:

```bash
<found-path> install --check
```

Stop if the check does not report `"up_to_date": true`.

From here on, the helper is `~/.config/buzz-agent/bin/project-buzz`. Use that
path in every following step and tell the user to use it too.

## 1. Check the prerequisites

Verify `python3 --version` (3.8 or newer) and that these binaries are reachable,
either on `PATH` or as absolute paths the user can supply:

- `buzz` - required for all reporting
- `buzz-admin` - required only for creating the agent identity
- `compute_auth_tag` - required only for creating the agent identity

Use binaries supplied by the user's Buzz deployment or build the tools from the
Buzz source tree. This plugin does not distribute Buzz binaries. Never invent a
download URL, package version, or checksum.

Windows specifics to check before continuing:

- Git for Windows must be installed, because the shell tooling runs under Git Bash.
- `python` must be on PATH. `install` writes a `project-buzz.cmd` next to the
  helper so the documented call works from cmd, PowerShell and Git Bash.

## 2. Make sure the user's own Buzz key is admitted to the relay

Many relays only serve their members. The agent identity created in step 4
carries no membership of its own: it authenticates through a NIP-OA attestation
to the user's own Buzz key, so that key has to be a member of the same relay.

Ask whether the user already uses this relay with their own Buzz client. If they
do, this step is done. If they do not, they send their own Buzz public key to the
relay owner and wait for confirmation. Buzz Desktop shows that key in the profile
settings as "Public key". The owner adds it on the relay host, where `buzz-admin`
reaches the relay database:

```bash
buzz-admin add-member --pubkey <human-public-key>
```

Do not continue before the owner confirms. Step 4 is the first one that talks to
the relay; without membership it fails with `relay_membership_required`.

This is a different grant from the channel access in step 5: membership opens the
relay for the user, channel membership opens one project for their agent.

## 3. Write the config

Create `~/.config/buzz-agent/config.json` (or `$BUZZ_AGENT_HOME/config.json`).
Ask the user for the relay URL and their first name, then write:

```json
{
  "relay_url": "<relay url from the Buzz owner>",
  "agent_name": "claude.<firstname-lowercase>",
  "buzz_bin": "buzz",
  "buzz_admin_bin": "buzz-admin",
  "auth_tag_bin": "compute_auth_tag",
  "projects": {}
}
```

`agent_name` must be `<client>.<person>`, all lowercase. This keeps the user's
agent distinct from the Buzz owner's own fleet seats. Never set a bare `claude`.

## 4. Create the agent identity

This creates a key pair for the agent and attests it to the user's own Buzz
identity, so the agent posts as itself and the user stays its owner.

Tell the user to run this themselves so their private key never passes through
the conversation:

```bash
~/.config/buzz-agent/bin/project-buzz provision \
  --display-name "<Name> (Claude Code)" \
  --about "Coding agent on <machine>"
```

The command prompts for the key without echoing it, so it never reaches the
shell history or this conversation. Point out that the key is used locally only,
to sign the owner attestation, and is neither stored nor transmitted. The
command prints the agent's public key.

In a non-interactive shell the helper reads `BUZZ_OWNER_PRIVATE_KEY` instead. In
that case tell the user to prefix the assignment with a space so most shells keep
it out of the history.

If this command fails with `relay_membership_required`, step 2 is still open: the
user's own Buzz key is not admitted to this relay. The key pair on disk stays
valid, so repeat the command with `--force` once the owner has confirmed.

## 5. Ask for channel access

The user sends the agent public key printed in step 4 to the Buzz owner and names
the projects they work on. The owner adds that key to each project channel.
Nothing else works until that grant exists, by design.

## 6. Register the projects

Once the grant is in place, run inside each project checkout:

```bash
~/.config/buzz-agent/bin/project-buzz register <repo-id>
```

The repo id is the one the Buzz owner used in the grant. The helper finds the
matching channel and stores the mapping.

## 7. Verify

```bash
~/.config/buzz-agent/bin/project-buzz doctor
```

Report the result plainly. Everything must be `ok` before telling the user that
reporting works. If a project check fails, the grant for that repository is
missing or incomplete.
