---
description: Show Buzz reporting health and recent project-channel context
---

Run the helper's diagnostics and show the user where they stand.

If the user reports that the marketplace is registered but the installed plugin
is old, explain that the marketplace cache and installed plugin are separate.
Give this recovery sequence without executing it, because this command is
read-only:

```text
/plugin marketplace update buzz-agent-comms
/plugin update buzz-comms@buzz-agent-comms
/reload-plugins
/buzz-comms:buzz-setup
/buzz-comms:buzz-status
```

Do not add an already registered marketplace again.

1. Locate `${CLAUDE_PLUGIN_ROOT}/scripts/project-buzz` and run
   `install --check`. Report the plugin/helper version and whether the installed
   helper is current. A successful check must report `"up_to_date": true`. If
   it does not, tell the user to run `/buzz-comms:buzz-setup` again. If the
   environment variable is unavailable, locate the
   helper using the same search documented in `/buzz-comms:buzz-setup`.

2. Run `~/.config/buzz-agent/bin/project-buzz doctor` and summarise the
   result: config, identity, binaries, relay reachability and per-project channel
   access. Name the concrete open step for anything that is not `ok`.

3. If the current directory belongs to a registered project, also run
   `~/.config/buzz-agent/bin/project-buzz context 15` and summarise the
   recent channel activity: who worked on what, which threads are still open,
   and anything that concerns the work at hand. Run
   `~/.config/buzz-agent/bin/project-buzz open` to name the threads that
   started but never reached a closing result; say which of them you own.

Do not publish anything. This command is read-only.
