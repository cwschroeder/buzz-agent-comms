# Contributing

Thanks for improving buzz-agent-comms.

## Development contract

Contributions follow
[`engineering-contract`](plugins/buzz-comms/skills/engineering-contract/SKILL.md):

- Work in a dedicated Git worktree on a task-specific branch.
- Push the branch and open a merge request. Only the maintainer merges into
  `main`, publishes releases, and changes shared infrastructure.
- Load and follow the installed `impeccable` skill before any UI or UX change.
- Keep customer data out of this public repository. If customer data is needed
  for an authorized diagnosis, use a verified local AI route and never allow a
  silent cloud fallback.

## Safety first

GitHub is the public Marketplace and distribution mirror. Development happens
in the internal GitLab project for the Burglengenfeld office or, for approved
external developers, in the private repository on Buzz's integrated Git server.
Push a task branch there and open a merge request. The maintainer mirrors
released versions to GitHub.

Use synthetic examples only. Never commit or paste real relay URLs, channel
UUIDs, identity keys, auth tags, customer data, private screenshots, internal
hostnames, or proprietary source code.

Report security issues privately as described in [SECURITY.md](SECURITY.md).

## Development

The helper supports Python 3.8 and uses only the standard library.

```bash
python -m py_compile plugins/buzz-comms/scripts/project-buzz
python -m unittest discover -s plugins/buzz-comms/tests
```

Every helper behavior change needs a focused test. Keep both plugin manifests
and `HELPER_VERSION` in sync when changing the version.

Use English Conventional Commit messages and add a Developer Certificate of
Origin sign-off:

```bash
git commit -s -m "fix: describe the change"
```
