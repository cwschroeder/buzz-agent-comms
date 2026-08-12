# Security Policy

## Reporting a vulnerability

Please report vulnerabilities through GitHub Security Advisories for this
repository. Do not open a public issue for a suspected vulnerability.

Do not include real private keys, auth tags, relay URLs, channel identifiers,
customer data, or proprietary source code in the report. Use minimal synthetic
examples and coordinate a secure transfer method with the maintainer if private
evidence is required.

## Scope

The plugin stores an agent identity locally and passes it to the Buzz CLI through
process environment variables. Reports involving key handling, file permissions,
command construction, project routing, mention safety, or unintended publication
are in scope.

The Buzz relay and clients are maintained separately in the upstream Buzz
project.
