---
name: ponytail-review
description: >-
  Review a diff for unnecessary complexity when the user explicitly asks for
  Ponytail, an over-engineering review, a simplification review, or invokes
  /buzz-comms:ponytail-review. This is a one-shot, read-only review and does
  not replace correctness, security, architecture, product, or test review.
license: MIT
---

# Ponytail Review

Run one bounded review of the requested diff. Do not edit files, persist a
mode, install hooks, or turn this into a whole-repository audit unless the user
explicitly asks for a wider scope.

This skill is adapted from
[`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) version
4.9.0, commit `0a4dd63ad4541f4f655c4108a295916f3c1d8fda`. Its MIT license is stored beside
this file.

## Establish the review base

Name the exact base and head commits or state that the review covers an
uncommitted working-tree diff. Read the repository rules and the product,
architecture, and testing guidance that apply to the changed surface.

Project requirements outrank this review. Treat required tests, documentation,
validation, error handling, security controls, accessibility, calibration for
real hardware, compatibility work, and explicitly requested behavior as
protected scope.

## Look for avoidable complexity

Check the changed flow for:

- speculative abstractions, configuration, extension points, or wrappers with
  no current consumer;
- code that duplicates an existing project pattern, standard-library feature,
  native platform capability, or already-installed dependency;
- dependencies added for behavior that a small, clear local implementation
  already covers;
- policy spread across callers that belongs at one cohesive boundary;
- hidden side effects or extra public contracts created to save a few local
  lines;
- dead flexibility and code that the current requirement no longer reaches.

Optimize for the fewest concepts, public contracts, hidden behaviors, and
places a maintainer must inspect. A shorter diff is useful only when it keeps
the complete requested behavior and leaves complexity in the right place.

## Verify every finding

Before recommending deletion or inlining, search the whole relevant tree for
callers and references, including tests, fixtures, configuration, generated
bindings, and string or dynamic references. Use the repository's code graph
when available. A symbol used only by tests is still used.

Do not describe a finding as dead or unreferenced when the check is incomplete.
Mark it `unverified` and explain the missing evidence instead. Re-check every
finding against the current head before returning it.

## Report

List findings by impact. Use one entry per finding:

`<path>:<line> <tag>: <complexity>. Replace with <smaller cohesive option>. Evidence: <caller or dependency check>.`

Tags:

- `delete`: behavior or flexibility with no verified consumer;
- `stdlib`: project code already supplied by the language standard library;
- `native`: code or a dependency already supplied by the platform;
- `reuse`: an existing project pattern already covers the requirement;
- `yagni`: scaffolding for an unrequested future need;
- `shrink`: the same cohesive behavior can be expressed more clearly with less
  code;
- `contain`: local minimization spread policy or hidden behavior into callers.

Do not invent a line-savings total. Give a number only when it can be measured
from a concrete replacement diff. If no finding survives verification, return
`Lean enough. No cut recommended.`

End with the reviewed base and any verification limit. Keep correctness,
security, performance, product intent, and test completeness in their normal
review passes.
