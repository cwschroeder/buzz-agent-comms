#!/usr/bin/env python3
"""Isolated tests for the portable project-buzz helper.

No relay and no real Buzz CLI are involved: a fake ``buzz`` binary records the
arguments it was called with, so the tests assert the protocol contract
(marker format, validation, deduplication, project routing) rather than
network behaviour.

Run with:  python3 -m unittest discover -s plugins/buzz-comms/tests
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

# The helper has no .py suffix, so an explicit source loader is required.
import importlib.util
from importlib.machinery import SourceFileLoader

_loader = SourceFileLoader("project_buzz", str(SCRIPTS / "project-buzz"))
_spec = importlib.util.spec_from_loader("project_buzz", _loader)
project_buzz = importlib.util.module_from_spec(_spec)
_loader.exec_module(project_buzz)


FAKE_BUZZ = """#!/usr/bin/env python3
import json, os, sys
log = os.environ["FAKE_BUZZ_LOG"]
with open(log, "a", encoding="utf-8") as handle:
    handle.write(json.dumps(sys.argv[1:]) + "\\n")
if os.environ.get("FAKE_BUZZ_FAIL") == "1":
    sys.stderr.write("relay unavailable\\n")
    sys.exit(2)
if os.environ.get("FAKE_BUZZ_MEMBERSHIP_DENIED") == "1":
    sys.stderr.write("relay error 403: relay_membership_required\\n")
    sys.exit(2)
if sys.argv[1:3] == ["channels", "list"]:
    print(json.dumps([
        {"channel_id": "11111111-1111-1111-1111-111111111111", "name": "codeapp-agent"},
        {"channel_id": "22222222-2222-2222-2222-222222222222", "name": "maas-ng-agent"},
    ]))
elif sys.argv[1:3] == ["channels", "members"]:
    print(json.dumps(["c" * 64, "d" * 64]))
elif sys.argv[1:5] == ["--format", "compact", "users", "get"]:
    if os.environ.get("FAKE_BUZZ_BAD_PROFILES") == "1":
        print("not-json")
    else:
        print(json.dumps([
            {"pubkey": "c" * 64, "display_name": "FirstMate"},
            {"pubkey": "d" * 64, "display_name": "CodeApp Repo-Agent"},
        ]))
else:
    print(json.dumps({"accepted": True, "event_id": "a" * 64}))
"""


def write_fake_buzz(directory: Path, stem: str = "buzz") -> Path:
    """Create the fake CLI and return the path that is actually executable.

    Windows honours neither the shebang nor an extensionless file: CreateProcess
    answers WinError 193. So the payload goes into a .py file and a .cmd shim in
    front of it carries the interpreter. `sys.executable` rather than a bare
    `python`, because the test machine may only have the `py` launcher on PATH.
    """
    impl = directory / "{0}_impl.py".format(stem)
    impl.write_text(FAKE_BUZZ, encoding="utf-8")

    if os.name == "nt":
        shim = directory / "{0}.cmd".format(stem)
        shim.write_text(
            '@echo off\r\n"{0}" "{1}" %*\r\n'.format(sys.executable, impl),
            encoding="utf-8",
        )
        return shim

    target = directory / stem
    target.write_text(FAKE_BUZZ, encoding="utf-8")
    target.chmod(0o755)
    return target


class HelperTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="buzz-agent-test-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        # Registered after the rmtree cleanup, so it runs before it (LIFO):
        # Windows refuses to delete a directory that is still the cwd.
        self.addCleanup(os.chdir, os.getcwd())

        self.home = self.root / "config"
        self.home.mkdir()
        self.log = self.root / "calls.jsonl"

        self.fake_buzz = write_fake_buzz(self.root)

        self.workspace = self.root / "work" / "codeapp"
        self.workspace.mkdir(parents=True)

        os.environ["BUZZ_AGENT_HOME"] = str(self.home)
        os.environ["FAKE_BUZZ_LOG"] = str(self.log)
        os.environ.pop("FAKE_BUZZ_FAIL", None)
        os.environ.pop("FAKE_BUZZ_BAD_PROFILES", None)
        os.environ.pop("FAKE_BUZZ_MEMBERSHIP_DENIED", None)
        self.addCleanup(os.environ.pop, "BUZZ_AGENT_HOME", None)
        self.addCleanup(os.environ.pop, "FAKE_BUZZ_LOG", None)
        self.addCleanup(os.environ.pop, "FAKE_BUZZ_BAD_PROFILES", None)
        self.addCleanup(os.environ.pop, "FAKE_BUZZ_MEMBERSHIP_DENIED", None)

        self.write_config()
        self.write_identity()

    def write_config(self, agent_name="claude.stratos", projects=None):
        if projects is None:
            projects = {
                str(self.workspace): {
                    "repo_id": "codeapp",
                    "channel_id": "11111111-1111-1111-1111-111111111111",
                }
            }
        (self.home / "config.json").write_text(
            json.dumps(
                {
                    "relay_url": "https://relay.example",
                    "buzz_bin": str(self.fake_buzz),
                    "agent_name": agent_name,
                    "projects": projects,
                }
            ),
            encoding="utf-8",
        )

    def write_identity(self):
        path = self.home / "identity.json"
        path.write_text(
            json.dumps(
                {
                    "private_key": "deadbeef",
                    "public_key": "b" * 64,
                    "auth_tag": '{"tag":"value"}',
                }
            ),
            encoding="utf-8",
        )
        path.chmod(0o600)

    def calls(self):
        if not self.log.is_file():
            return []
        return [json.loads(line) for line in self.log.read_text().splitlines() if line]

    def sent_content(self, index=0):
        sends = [c for c in self.calls() if c[:2] == ["messages", "send"]]
        return sends[index][sends[index].index("--content") + 1]

    def run_cli(self, argv):
        return project_buzz.main(argv)


class MarkerFormat(HelperTestCase):
    def test_start_marker_matches_the_pilot_protocol(self):
        os.chdir(self.workspace)
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne Arbeit"]))
        self.assertTrue(
            self.sent_content().startswith("[AGENT-ACTIVITY:started:claude.stratos:u-1] ")
        )

    def test_result_marker_matches_the_pilot_protocol(self):
        os.chdir(self.workspace)
        root = "a" * 64
        self.assertEqual(0, self.run_cli(["result", "u-2", root, "Fertig"]))
        self.assertEqual(
            "[AGENT-RESULT:claude.stratos:u-2] Fertig", self.sent_content()
        )

    def test_progress_and_blocked_use_the_phase_in_the_marker(self):
        os.chdir(self.workspace)
        root = "a" * 64
        self.run_cli(["progress", "u-3", root, "Zwischenstand"])
        self.run_cli(["blocked", "u-4", root, "Warte auf Freigabe"])
        self.assertTrue(
            self.sent_content(0).startswith("[AGENT-ACTIVITY:progress:claude.stratos:u-3]")
        )
        self.assertTrue(
            self.sent_content(1).startswith("[AGENT-ACTIVITY:blocked:claude.stratos:u-4]")
        )

    def test_reply_to_is_passed_for_threaded_phases_only(self):
        os.chdir(self.workspace)
        root = "a" * 64
        self.run_cli(["start", "u-5", "Los"])
        self.run_cli(["result", "u-6", root, "Fertig"])
        sends = [c for c in self.calls() if c[:2] == ["messages", "send"]]
        self.assertNotIn("--reply-to", sends[0])
        self.assertIn("--reply-to", sends[1])
        self.assertEqual(root, sends[1][sends[1].index("--reply-to") + 1])


class AgentNameEnforcement(HelperTestCase):
    def test_bare_client_name_is_rejected(self):
        # A bare "claude" would be attributed to the owner's seat ledger.
        self.write_config(agent_name="claude")
        os.chdir(self.workspace)
        self.assertEqual(1, self.run_cli(["start", "u-1", "Beginne"]))
        self.assertEqual([], self.calls())

    def test_uppercase_name_is_rejected(self):
        self.write_config(agent_name="Claude.Stratos")
        os.chdir(self.workspace)
        self.assertEqual(1, self.run_cli(["start", "u-1", "Beginne"]))

    def test_dotted_name_is_accepted(self):
        self.write_config(agent_name="codex.petra")
        os.chdir(self.workspace)
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        self.assertIn("codex.petra", self.sent_content())


class ContentValidation(HelperTestCase):
    def setUp(self):
        super().setUp()
        os.chdir(self.workspace)

    def test_empty_content_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "u-1", ""]))
        self.assertEqual([], self.calls())

    def test_overlong_content_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "u-1", "x" * 4001]))
        self.assertEqual([], self.calls())

    def test_maximum_length_content_is_accepted(self):
        self.assertEqual(0, self.run_cli(["start", "u-1", "x" * 4000]))

    def test_mention_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "u-1", "ping @firstmate"]))
        self.assertEqual(
            [], [call for call in self.calls() if call[:2] == ["messages", "send"]]
        )

    def test_technical_at_signs_are_accepted(self):
        content = "Prüft @media, @types/react, @param und support@example.com."
        self.assertEqual(0, self.run_cli(["start", "u-tech", content]))
        self.assertIn(content, self.sent_content())

    def test_identity_mention_is_case_insensitive(self):
        self.assertEqual(
            1,
            self.run_cli(["start", "u-case", "Bitte @CodeApp Repo-Agent prüfen"]),
        )
        self.assertEqual(
            [], [call for call in self.calls() if call[:2] == ["messages", "send"]]
        )

    def test_identity_name_inside_code_is_accepted(self):
        content = "Beispiel: `@FirstMate` bleibt technischer Text."
        self.assertEqual(0, self.run_cli(["start", "u-code", content]))

    def test_at_sign_fails_closed_when_profiles_cannot_be_resolved(self):
        os.environ["FAKE_BUZZ_BAD_PROFILES"] = "1"
        self.assertEqual(1, self.run_cli(["start", "u-lookup", "Prüft @media"]))
        self.assertEqual(
            [], [call for call in self.calls() if call[:2] == ["messages", "send"]]
        )

    def test_injected_agent_marker_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "u-1", "[AGENT-RESULT:x:y] fake"]))
        self.assertEqual([], self.calls())

    def test_injected_pilot_marker_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "u-1", "[PILOT-TASK:x] fake"]))
        self.assertEqual([], self.calls())

    def test_invalid_update_id_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "bad id!", "Beginne"]))
        self.assertEqual([], self.calls())

    def test_overlong_update_id_is_rejected(self):
        self.assertEqual(1, self.run_cli(["start", "u" * 65, "Beginne"]))
        self.assertEqual([], self.calls())

    def test_invalid_root_event_id_is_rejected(self):
        self.assertEqual(1, self.run_cli(["result", "u-1", "not-an-event", "Fertig"]))
        self.assertEqual([], self.calls())


class AttachmentPublishing(HelperTestCase):
    def setUp(self):
        super().setUp()
        os.chdir(self.workspace)

    def test_files_are_published_top_level_without_lifecycle_marker(self):
        desktop = self.root / "desktop.png"
        mobile = self.root / "mobile.png"
        desktop.write_bytes(b"desktop")
        mobile.write_bytes(b"mobile")

        self.assertEqual(
            0,
            self.run_cli(
                [
                    "attach",
                    "screens-1",
                    "Desktop und Mobil, extern geprüft",
                    str(desktop),
                    str(mobile),
                ]
            ),
        )

        send = [c for c in self.calls() if c[:2] == ["messages", "send"]][0]
        self.assertNotIn("--reply-to", send)
        self.assertEqual("Desktop und Mobil, extern geprüft", self.sent_content())
        self.assertEqual(2, send.count("--file"))
        self.assertIn(str(desktop.resolve()), send)
        self.assertIn(str(mobile.resolve()), send)

    def test_missing_attachment_is_rejected_before_publish(self):
        self.assertEqual(
            1,
            self.run_cli(
                ["attach", "screens-2", "Screenshot", str(self.root / "missing.png")]
            ),
        )
        self.assertEqual([], self.calls())

    def test_attachment_retry_is_deduplicated(self):
        screenshot = self.root / "screen.png"
        screenshot.write_bytes(b"screen")
        arguments = ["attach", "screens-3", "Screenshot", str(screenshot)]

        self.assertEqual(0, self.run_cli(arguments))
        self.assertEqual(0, self.run_cli(arguments))
        sends = [c for c in self.calls() if c[:2] == ["messages", "send"]]
        self.assertEqual(1, len(sends))


class Deduplication(HelperTestCase):
    def setUp(self):
        super().setUp()
        os.chdir(self.workspace)

    def test_same_phase_and_id_publishes_once(self):
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        sends = [c for c in self.calls() if c[:2] == ["messages", "send"]]
        self.assertEqual(1, len(sends))

    def test_failed_publish_releases_the_lock_for_retry(self):
        os.environ["FAKE_BUZZ_FAIL"] = "1"
        self.assertEqual(1, self.run_cli(["start", "u-1", "Beginne"]))
        os.environ.pop("FAKE_BUZZ_FAIL")
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        sends = [c for c in self.calls() if c[:2] == ["messages", "send"]]
        self.assertEqual(2, len(sends))

    def test_different_phases_share_no_lock(self):
        root = "a" * 64
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        self.assertEqual(0, self.run_cli(["result", "u-1", root, "Fertig"]))
        sends = [c for c in self.calls() if c[:2] == ["messages", "send"]]
        self.assertEqual(2, len(sends))


class ProjectRouting(HelperTestCase):
    def test_subdirectory_resolves_to_the_registered_project(self):
        nested = self.workspace / "bridge" / "tests"
        nested.mkdir(parents=True)
        os.chdir(nested)
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        send = [c for c in self.calls() if c[:2] == ["messages", "send"]][0]
        self.assertEqual(
            "11111111-1111-1111-1111-111111111111", send[send.index("--channel") + 1]
        )

    def test_longest_matching_workspace_wins(self):
        inner = self.workspace / "vendor" / "maas-ng"
        inner.mkdir(parents=True)
        projects = {
            str(self.workspace): {
                "repo_id": "codeapp",
                "channel_id": "11111111-1111-1111-1111-111111111111",
            },
            str(inner): {
                "repo_id": "maas-ng",
                "channel_id": "22222222-2222-2222-2222-222222222222",
            },
        }
        self.write_config(projects=projects)
        os.chdir(inner)
        self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        send = [c for c in self.calls() if c[:2] == ["messages", "send"]][0]
        self.assertEqual(
            "22222222-2222-2222-2222-222222222222", send[send.index("--channel") + 1]
        )

    def test_unregistered_directory_fails_closed(self):
        outside = self.root / "elsewhere"
        outside.mkdir()
        os.chdir(outside)
        self.assertEqual(1, self.run_cli(["start", "u-1", "Beginne"]))
        self.assertEqual([], self.calls())

    def test_unknown_explicit_repo_id_fails_closed(self):
        os.chdir(self.workspace)
        self.assertEqual(1, self.run_cli(["start", "u-1", "Beginne", "not-registered"]))
        self.assertEqual([], self.calls())


class ContextArguments(HelperTestCase):
    def setUp(self):
        super().setUp()
        os.chdir(self.workspace)

    def gets(self):
        return [c for c in self.calls() if c[:2] == ["messages", "get"]]

    def test_bare_number_is_read_as_a_limit(self):
        self.assertEqual(0, self.run_cli(["context", "3"]))
        call = self.gets()[0]
        self.assertEqual("3", call[call.index("--limit") + 1])
        self.assertEqual(
            "11111111-1111-1111-1111-111111111111", call[call.index("--channel") + 1]
        )

    def test_repo_id_and_limit_still_work(self):
        self.assertEqual(0, self.run_cli(["context", "codeapp", "7"]))
        call = self.gets()[0]
        self.assertEqual("7", call[call.index("--limit") + 1])

    def test_default_limit_is_twenty(self):
        self.assertEqual(0, self.run_cli(["context"]))
        call = self.gets()[0]
        self.assertEqual("20", call[call.index("--limit") + 1])

    def test_limit_out_of_range_is_rejected(self):
        self.assertEqual(1, self.run_cli(["context", "500"]))
        self.assertEqual([], self.gets())


class Registration(HelperTestCase):
    def test_register_discovers_the_channel_by_convention(self):
        target = self.root / "work" / "maas-ng"
        target.mkdir(parents=True)
        os.chdir(target)
        self.assertEqual(0, self.run_cli(["register", "maas-ng"]))
        config = json.loads((self.home / "config.json").read_text())
        entry = config["projects"][str(target.resolve())]
        self.assertEqual("maas-ng", entry["repo_id"])
        self.assertEqual("22222222-2222-2222-2222-222222222222", entry["channel_id"])

    def test_register_fails_closed_for_a_channel_without_access(self):
        target = self.root / "work" / "seloca"
        target.mkdir(parents=True)
        os.chdir(target)
        self.assertEqual(1, self.run_cli(["register", "seloca"]))


class DesktopCliFallback(HelperTestCase):
    def test_buzz_cli_is_found_in_the_buzz_desktop_install(self):
        # Colleagues already run Buzz Desktop, which ships the CLI as a sidecar.
        desktop = self.root / "Buzz.app" / "Contents" / "MacOS"
        desktop.mkdir(parents=True)
        sidecar = write_fake_buzz(desktop)

        self.write_config()
        config = json.loads((self.home / "config.json").read_text())
        config["buzz_bin"] = "buzz-not-on-path"
        (self.home / "config.json").write_text(json.dumps(config), encoding="utf-8")

        original = project_buzz.desktop_cli_candidates
        project_buzz.desktop_cli_candidates = lambda: [sidecar]
        self.addCleanup(setattr, project_buzz, "desktop_cli_candidates", original)
        try:
            os.chdir(self.workspace)
            self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        finally:
            project_buzz.desktop_cli_candidates = original
        self.assertEqual(1, len([c for c in self.calls() if c[:2] == ["messages", "send"]]))

    def test_fallback_does_not_apply_to_the_provisioning_binaries(self):
        self.write_config()
        config = json.loads((self.home / "config.json").read_text())
        config["buzz_admin_bin"] = "definitely-missing-admin"
        (self.home / "config.json").write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaises(project_buzz.UserError):
            project_buzz.resolve_binary(
                json.loads((self.home / "config.json").read_text()),
                "buzz_admin_bin",
                "buzz-admin",
            )


class Install(HelperTestCase):
    def test_install_places_an_executable_helper_at_the_stable_path(self):
        self.assertEqual(0, self.run_cli(["install"]))
        target = self.home / "bin" / "project-buzz"
        self.assertTrue(target.is_file())
        self.assertTrue(os.access(str(target), os.X_OK))
        self.assertIn("def main(", target.read_text(encoding="utf-8"))

    def test_install_is_idempotent(self):
        self.assertEqual(0, self.run_cli(["install"]))
        first = (self.home / "bin" / "project-buzz").read_text(encoding="utf-8")
        self.assertEqual(0, self.run_cli(["install"]))
        second = (self.home / "bin" / "project-buzz").read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertTrue(len(second) > 0)

    def test_install_check_detects_missing_current_and_drifted_helper(self):
        self.assertEqual(1, self.run_cli(["install", "--check"]))
        self.assertEqual(0, self.run_cli(["install"]))
        self.assertEqual(0, self.run_cli(["install", "--check"]))

        target = self.home / "bin" / "project-buzz"
        target.write_text(target.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
        self.assertEqual(1, self.run_cli(["install", "--check"]))

    def test_helper_version_matches_both_manifests(self):
        repository = SCRIPTS.parents[2]
        marketplace = json.loads(
            (repository / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        plugin = json.loads(
            (
                repository
                / "plugins"
                / "buzz-comms"
                / ".claude-plugin"
                / "plugin.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(project_buzz.HELPER_VERSION, marketplace["metadata"]["version"])
        self.assertEqual(project_buzz.HELPER_VERSION, marketplace["plugins"][0]["version"])
        self.assertEqual(project_buzz.HELPER_VERSION, plugin["version"])


class RelayMembershipDiagnostics(HelperTestCase):
    """A 403 from a members-only relay must name the missing grant.

    Without this the operator sees a bare relay error at the first command that
    touches the relay, two steps before the setup guide mentions the owner.
    """

    def test_denied_membership_names_the_owner_command(self):
        os.environ["FAKE_BUZZ_MEMBERSHIP_DENIED"] = "1"
        config = project_buzz.load_config()
        with self.assertRaises(project_buzz.UserError) as caught:
            project_buzz.member_channels(config)
        message = str(caught.exception)
        self.assertIn("relay_membership_required", message)
        self.assertIn("buzz-admin add-member", message)

    def test_doctor_reports_the_explanation(self):
        os.environ["FAKE_BUZZ_MEMBERSHIP_DENIED"] = "1"
        os.chdir(self.workspace)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(1, self.run_cli(["doctor"]))
        self.assertIn("buzz-admin add-member", stdout.getvalue())

    def test_an_unrelated_failure_stays_unexplained(self):
        # The hint keys on the relay's error code, so a plain outage must not
        # send the operator chasing a membership that is already there.
        os.environ["FAKE_BUZZ_FAIL"] = "1"
        self.addCleanup(os.environ.pop, "FAKE_BUZZ_FAIL", None)
        config = project_buzz.load_config()
        with self.assertRaises(project_buzz.UserError) as caught:
            project_buzz.member_channels(config)
        self.assertNotIn("buzz-admin add-member", str(caught.exception))


class PolicyContract(unittest.TestCase):
    def test_skill_requires_reader_ready_german_and_final_screenshot_evidence(self):
        skill = (
            SCRIPTS.parent / "skills" / "buzz-team-communication" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "real German umlauts",
            "reader-ready",
            "internal reasoning",
            "top-level",
            "before the final user response",
        ):
            self.assertIn(phrase, skill)

    def test_plugin_commands_are_documented_with_namespace(self):
        repository = SCRIPTS.parents[2]
        paths = (
            repository / "README.md",
            repository / "CLAUDE.md",
            SCRIPTS / "project-buzz",
            SCRIPTS.parent / "commands" / "buzz-status.md",
            SCRIPTS.parent / "skills" / "buzz-team-communication" / "SKILL.md",
        )
        bare_command = re.compile(r"(?<!:)/buzz-(?:setup|status)\b")
        for path in paths:
            with self.subTest(path=path):
                self.assertIsNone(
                    bare_command.search(path.read_text(encoding="utf-8"))
                )

        readme = (repository / "README.md").read_text(encoding="utf-8")
        self.assertIn("/buzz-comms:buzz-setup", readme)
        self.assertIn("/buzz-comms:buzz-status", readme)

    def test_relay_admission_is_documented_before_the_agent_identity(self):
        repository = SCRIPTS.parents[2]
        setup = (SCRIPTS.parent / "commands" / "buzz-setup.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("buzz-admin add-member", setup)
        self.assertLess(
            setup.index("buzz-admin add-member"),
            setup.index("project-buzz provision"),
            "relay membership must be settled before provisioning touches the relay",
        )

        readme = (repository / "README.md").read_text(encoding="utf-8")
        self.assertIn("Runbook für den Buzz-Owner", readme)
        for command in (
            "buzz-admin add-member",
            "buzz channels add-member",
            "buzz channels remove-member",
            "buzz-admin remove-member",
        ):
            self.assertIn(command, readme)


class IdentityPermissions(HelperTestCase):
    @unittest.skipIf(os.name == "nt", "POSIX permission bits do not apply on Windows")
    def test_world_readable_identity_is_refused(self):
        (self.home / "identity.json").chmod(0o644)
        os.chdir(self.workspace)
        self.assertEqual(1, self.run_cli(["start", "u-1", "Beginne"]))
        self.assertEqual([], self.calls())

    def test_permission_check_is_skipped_on_windows(self):
        # Windows reports 0o666 for every file, so the POSIX check must not run
        # there or no colleague on Windows could ever publish.
        (self.home / "identity.json").chmod(0o644)
        os.chdir(self.workspace)
        original = project_buzz.is_windows
        project_buzz.is_windows = lambda: True
        self.addCleanup(setattr, project_buzz, "is_windows", original)
        try:
            self.assertEqual(0, self.run_cli(["start", "u-1", "Beginne"]))
        finally:
            project_buzz.is_windows = original
        self.assertEqual(1, len([c for c in self.calls() if c[:2] == ["messages", "send"]]))

    def test_install_writes_a_launcher_on_windows(self):
        original = project_buzz.is_windows
        project_buzz.is_windows = lambda: True
        self.addCleanup(setattr, project_buzz, "is_windows", original)
        try:
            self.assertEqual(0, self.run_cli(["install"]))
        finally:
            project_buzz.is_windows = original
        launcher = self.home / "bin" / "project-buzz.cmd"
        self.assertTrue(launcher.is_file())
        self.assertIn("python", launcher.read_text(encoding="utf-8"))

    @unittest.skipIf(os.name == "nt", "the launcher is exactly what Windows needs")
    def test_no_launcher_on_posix(self):
        self.assertEqual(0, self.run_cli(["install"]))
        self.assertFalse((self.home / "bin" / "project-buzz.cmd").exists())


if __name__ == "__main__":
    unittest.main()
