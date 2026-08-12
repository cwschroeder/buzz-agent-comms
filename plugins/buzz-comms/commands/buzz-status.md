---
description: Show Buzz reporting health and recent project-channel context
---

Run the helper's diagnostics and show the user where they stand.

1. Locate `${CLAUDE_PLUGIN_ROOT}/scripts/project-buzz` and run
   `install --check`. Report the plugin/helper version and whether the installed
   helper is current. If the environment variable is unavailable, locate the
   helper using the same search documented in `/buzz-comms:buzz-setup`.

2. Run `~/.config/buzz-agent/bin/project-buzz doctor` and summarise the
   result: config, identity, binaries, relay reachability and per-project channel
   access. Name the concrete open step for anything that is not `ok`.

3. If the current directory belongs to a registered project, also run
   `~/.config/buzz-agent/bin/project-buzz context 15` and summarise the
   recent channel activity: who worked on what, which threads are still open, and
   anything that concerns the work at hand.

Do not publish anything. This command is read-only.
