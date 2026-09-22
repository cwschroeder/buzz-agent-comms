---
name: show-me
description: Make Buzz updates concrete with before/after comparisons, useful lists, screenshots, rendered diagrams or short recordings. Use before substantive result posts and whenever the user wants a change or concept shown visually.
---

# Show Me

Choose the smallest view that makes the change understandable. Lead the caption
with what the reader should notice. Keep the post readable without opening media.
Do not force an image into a start message or a minor status update.

## Choose the format

| What the reader needs | Format |
|---|---|
| Several independent changes | Short list, one effect per item |
| Old and new behavior | Same-case before/after comparison |
| Visible UI change | Matched screenshots with clear Before / After labels |
| Process, dependency or architecture | Rendered diagram; use installed `archify` when available |
| Measured performance or quality | Small table or chart with units and test conditions |
| Multi-step interaction | Short recording of the real application |
| Proposed behavior or explanatory concept | Clearly labelled concept illustration or animation |

## Before and after

Compare the same task, data, viewport, zoom and crop where practical. Identify
versions or capture times when they matter. Explain the one change the reader
should see. A pair is one visual unit, whether composed into one image or attached
as two labelled files. On mobile, stack the pair if side-by-side text becomes tiny.

If no trustworthy old capture exists, show the current state and describe only
the evidenced earlier behavior in text. Never generate or reconstruct a screenshot
and present it as proof of the old or new application.

## Diagrams and optional tools

For a meaningful flow or architecture change, use the installed `archify` skill:
read its instructions, build from verified facts, validate, export a PNG and
inspect its labels, arrows and readability. Attach the image; an interactive HTML
file may accompany it, but a local `file://` URL is not a usable channel link.

For a requested concept illustration or explanatory animation, an installed
`higgsfield-generate` skill can help. Read its routing instructions and use its
specialized skills when required. Label generated work `Concept` (German:
`Konzept`) and keep it separate from product evidence. Follow the engineering
contract for customer data and cloud processing. Do not automatically start paid
generation for routine updates; respect the user's authorization and budget.

These tools are optional and are not bundled with this plugin. If unavailable,
use a truthful text comparison, a small table or a narrow fenced ASCII diagram.
Do not auto-install tools, invent commands or claim an export succeeded.
Mermaid source is useful for authoring, but do not assume Buzz renders it.
If rendering is unavailable, prefer a readable text diagram over raw Mermaid.

## Publish and check

- One focused visual unit per update is normally enough. Include additional views
  when evidence requires them, such as desktop and mobile acceptance.
- Inspect the actual export or recording, not just the source. Check crop,
  legibility, labels and consistency with the caption.
- Use real verified labels and measurements. Synthetic training examples belong
  in documentation, not in posts claiming delivery.
- Remove private data, credentials and unrelated content before upload.
- Publish media top-level with the attachment workflow in
  `buzz-team-communication`, then cite its event in the lifecycle result.
- Keep text diagrams below 80 columns and inside fenced blocks.
- Apply the public `no-ai-slop` profile and checklist to captions as well as prose.
  Preserve useful lists and comparisons during the plain-language pass.
