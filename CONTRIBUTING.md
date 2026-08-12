# Contributing

Thanks for improving buzz-agent-comms.

## Safety first

This is a public repository. Use synthetic examples only. Never commit or paste
real relay URLs, channel UUIDs, identity keys, auth tags, customer data, private
screenshots, internal hostnames, or proprietary source code.

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
