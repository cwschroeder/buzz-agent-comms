---
name: engineering-contract
description: >-
  Enforce the shared development contract for project work: dedicated Git
  worktrees, contributor-owned branches and merge requests, maintainer-only
  merges, deployments and infrastructure changes, Impeccable for UI design,
  and verified local AI when customer data is involved. Use whenever an agent
  plans, changes, reviews, tests, builds, deploys, or diagnoses a software
  project.
---

# Engineering Contract

Apply this contract before project work. Read the repository's `AGENTS.md`,
`CLAUDE.md`, contribution guide, product vision, and testing guidance that apply
to the requested surface. Project rules may add stricter requirements. Surface a
conflict instead of silently weakening either contract.

## Establish the role

Determine the acting role before the first mutation:

- Treat the agent as a contributor unless the repository instructions or the
  user's current request explicitly designate it as the maintainer for the
  affected project and operation.
- Repository ownership, credentials, branch permissions, or the ability to run
  a deployment command do not establish maintainer authority.
- If the role is unclear and the next action would merge, deploy, or change
  infrastructure, stop and ask for an explicit designation.

## Worktree and merge request workflow

All implementation work happens in a dedicated Git worktree on a task-specific
branch. A checkout of `master` or another protected integration branch is a
coordination and integration checkout, not an implementation workspace.

Before editing:

1. Inspect repository status, remotes, divergence, existing worktrees, active
   branches, and parallel work.
2. Reuse the current checkout only when it is already a dedicated worktree for
   this task. Otherwise create a new worktree and feature or fix branch from the
   approved base.
3. Keep the change scoped to the task and preserve unrelated work in every
   checkout.

Contributors must:

- implement and verify the change in their dedicated worktree;
- commit according to the repository's signing and message rules;
- push the task branch and create or update a merge request;
- include the verified tests, known limits, source branch, and target branch in
  the merge request;
- stop at `Review-ready` and leave the merge to the maintainer.

Only the maintainer may merge into `master` or the repository's explicitly
configured protected integration branch. Contributors must not enable
auto-merge, merge their own request, push implementation commits directly to
that branch, or describe review-ready work as merged.

## Deployment and infrastructure ownership

Only the maintainer deploys and manages the infrastructure used for delivery.
This includes production and shared runtime configuration, credentials,
networking, runners, deployment targets, service lifecycle, migrations, and
rollback operations.

Contributors may inspect these systems read-only when the task and their access
allow it. They may prepare code, configuration changes, migration plans,
runbooks, and a merge request. They must leave the external mutation to the
maintainer and report `Nicht live` while that step is open.

The maintainer must verify the exact merged commit or build on the canonical
runtime, perform the required acceptance checks, and keep `docs/DEPLOYMENT.md`
current. Merge authority and deployment authority remain separate from a
successful local build.

## UI work uses Impeccable

Use the installed `impeccable` skill for any design, redesign, UX review,
frontend surface, component, form, dashboard, settings page, responsive change,
visual polish, accessibility pass, or design-system work.

Before UI editing:

1. Read the complete `impeccable/SKILL.md`. If the skill is unavailable, stop
   before changing UI code and tell the user it must be installed.
2. Follow Impeccable's session setup and load the one playbook that owns the
   requested UI task.
3. Read the project's `PRODUCT.md`, `DESIGN.md`, relevant surface brief, and a
   representative source of the shipped visual system.
4. Load Impeccable's craft floor immediately before editing UI.
5. Use its bounded inspection cycle for the relevant desktop, mobile, or native
   surfaces. Keep review-ready screenshots distinct from screenshots captured
   after a maintainer deployment on the canonical runtime.

Do not substitute an ad hoc visual pass when Impeccable applies. Preserve its
own refinement, redesign, product-truth, and verification rules.

## Customer data and model routing

Before sending data to an AI model or AI-backed tool, determine whether the
input can contain customer data. Treat production records, documents, exports,
logs, support content, screenshots, identifiers, prompts containing customer
facts, embeddings, audio, and derived extracts as customer data unless the
project defines a stricter classification.

Apply these rules:

1. Minimize first. Prefer schemas, synthetic fixtures, aggregates, or a small
   redacted sample when they can answer the question.
2. When customer data is still required, use a verified local AI route by
   default. Inference, embeddings, optical character recognition,
   transcription, storage, and telemetry must stay on approved local or
   company-controlled on-premises infrastructure. Cloud fallbacks and cloud
   egress must be disabled.
3. Verify the actual provider and endpoint before submitting the data. A local
   alias with an unknown cloud fallback does not count as local.
4. If the route cannot be verified as local, treat it as cloud-bound and stop.
   Do not silently fall back to a cloud model.
5. A cloud model may receive the material only after customer data has been
   removed or irreversibly anonymized, or when the user gives explicit approval
   and the repository's data-protection rules permit that transfer.
6. Keep customer data out of Buzz posts, merge requests, issues, commits, test
   fixtures, screenshots, logs, and durable agent memory. Redact evidence before
   publication.

Local processing does not remove the need for least privilege, data
minimization, retention limits, or repository-specific security controls.

## Buzz coordination and status language

For projects registered with Buzz, also read and follow the sibling
`buzz-team-communication` skill. Buzz records coordination and evidence; it does
not grant merge, deployment, infrastructure, or customer-data authority.

Use the narrowest accurate completion state:

- `Review-ready`: contributor branch pushed and merge request opened.
- `Merged`: maintainer merged the verified change.
- `Deployed`: maintainer deployed the named commit or build.
- `Extern verifiziert`: canonical runtime acceptance was completed.

Name any remaining maintainer action instead of implying delivery.
