#!/usr/bin/env python3
"""Parity tests for the Buzz 1.0 lifecycle plugin.

The plugin in ``buzz-app-plugins/lifecycle/plugin.js`` parses the markers that
project-buzz writes and judges threads open or closed. These tests feed both
the helper and the plugin the same input and require the same answer, so a
change to the marker format or the open rule fails here instead of in the app.

Run with:  python3 -m unittest discover -s plugins/buzz-comms/tests
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

from test_project_buzz import HelperTestCase, project_buzz

PLUGIN = (
    Path(__file__).resolve().parents[3]
    / "buzz-app-plugins"
    / "lifecycle"
    / "plugin.js"
)

# Imports the plugin as an ES module without a build step or package.json.
NODE_RUNNER = """
import { readFileSync } from "node:fs";
const [pluginPath, inputPath] = process.argv.slice(1);
const source = readFileSync(pluginPath, "utf8");
const plugin = await import(
  "data:text/javascript;base64," + Buffer.from(source).toString("base64")
);
const input = JSON.parse(readFileSync(inputPath, "utf8"));
const threads = {};
for (const [root, messages] of Object.entries(input.threads)) {
  const state = plugin.threadState(messages);
  threads[root] = { state: state.state, closing: state.closing?.phase ?? null };
}
process.stdout.write(
  JSON.stringify({
    parsed: input.contents.map((content) => plugin.parseLifecycle(content)),
    threads,
  }),
);
"""

THREAD_MESSAGES = [
    ("r1", "r1", "[AGENT-ACTIVITY:started:codex.petra:petra-1-start]: #\n\nBeginnt", 100),
    ("r1a", "r1", "[AGENT-RESULT:codex.petra:petra-1]: #\n\nAbgeschlossen", 110),
    ("r2", "r2", "[AGENT-ACTIVITY:started:claude.stratos:open-1-start]: #\n\nOffen", 120),
    ("r2a", "r2", "[AGENT-ACTIVITY:progress:claude.stratos:open-1]: #\n\nHalbzeit", 121),
    ("r3", "r3", "[AGENT-ACTIVITY:started:claude.stratos:block-1-start]: #\n\nBlocker", 130),
    ("r3a", "r3", "[AGENT-ACTIVITY:blocked:claude.stratos:block-1]: #\n\nWarte", 131),
    ("r4", "r4", "[AGENT-ACTIVITY:started:claude.stratos:corr-1-start]: #\n\nKorrigiert", 140),
    ("r4a", "r4", "[AGENT-RESULT:claude.stratos:corr-1]: #\n\nErstes Ergebnis", 141),
    ("r4b", "r4", "[AGENT-ACTIVITY:correction:claude.stratos:corr-2]: #\n\nKorrektur", 142),
    ("n1", "n1", "Normale Nachricht ohne Marker", 150),
]


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class BuzzAppLifecyclePlugin(HelperTestCase):
    def run_plugin(self, contents=(), threads=None):
        path = self.root / "plugin-input.json"
        path.write_text(
            json.dumps({"contents": list(contents), "threads": threads or {}}),
            encoding="utf-8",
        )
        completed = subprocess.run(
            ["node", "--input-type=module", "-e", NODE_RUNNER, str(PLUGIN), str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_plugin_parses_every_marker_the_helper_writes(self):
        contents = [
            project_buzz.compose_payload(
                project_buzz.build_marker(phase, "claude.stratos", "lc-1"),
                "**Titel**\n\nText mit [Link](https://example.invalid).",
            )
            for phase in project_buzz.LIFECYCLE_PHASES + ("correction",)
        ]
        # Posts from before helper 0.28 carry the marker as plain text.
        contents.append("[AGENT-RESULT:codex.petra:petra-1] Abgeschlossen")
        parsed = self.run_plugin(contents)["parsed"]
        for content, plugin in zip(contents, parsed):
            match = project_buzz.parse_marker(content)
            self.assertIsNotNone(match, content)
            self.assertEqual(
                plugin,
                {
                    "phase": match.group(1) or "result",
                    "agent": match.group(2),
                    "updateId": match.group(3),
                    "text": project_buzz.text_after_marker(content, match),
                },
            )

    def test_plugin_marks_only_posts_that_open_with_a_marker(self):
        parsed = self.run_plugin(
            [
                "Normale Nachricht ohne Marker",
                "Siehe [AGENT-RESULT:claude.stratos:lc-1] weiter oben.",
                "[PILOT-RESULT:claude:lc-1]: #\n\nFremdes Protokoll",
            ]
        )["parsed"]
        self.assertEqual(parsed, [None, None, None])

    def test_plugin_judges_threads_like_project_buzz_open(self):
        os.chdir(self.workspace)
        os.environ["FAKE_BUZZ_MESSAGES"] = json.dumps(
            [
                {
                    "id": event_id,
                    "tags": [["e", root, "", "root" if event_id == root else "reply"]],
                    "content": content,
                    "created_at": created_at,
                }
                for event_id, root, content, created_at in THREAD_MESSAGES
            ]
        )
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(self.run_cli(["open"]), 0)
        helper_open = {thread["root"] for thread in json.loads(stdout.getvalue())["open"]}

        threads = {}
        for event_id, root, content, created_at in THREAD_MESSAGES:
            threads.setdefault(root, []).append(
                {"id": event_id, "content": content, "createdAt": created_at}
            )
        plugin = self.run_plugin(threads=threads)["threads"]

        self.assertEqual(helper_open, {"r2"})
        self.assertEqual(
            {root for root, state in plugin.items() if state["state"] == "open"},
            helper_open,
        )
        self.assertEqual(
            plugin,
            {
                "r1": {"state": "closed", "closing": "result"},
                "r2": {"state": "open", "closing": None},
                "r3": {"state": "closed", "closing": "blocked"},
                "r4": {"state": "closed", "closing": "correction"},
                "n1": {"state": "none", "closing": None},
            },
        )


if __name__ == "__main__":
    unittest.main()
