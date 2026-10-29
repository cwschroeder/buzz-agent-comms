import contextlib
import io
import json
import os
import xml.etree.ElementTree as ET
from test_project_buzz import HelperTestCase, project_buzz


class CommunicationContract(HelperTestCase):
    def test_visible_code_counts_for_buzz_but_not_jira(self):
        text = 'Ergebnis.\n\n```text\n' + 'wert ' * 310 + '\n```'
        self.assertTrue(project_buzz.komm_check(text, 'buzz')[0])
        self.assertFalse(project_buzz.komm_check(text, 'jira')[0])

    def test_report_keeps_state_evidence_and_one_decision(self):
        spec = {'summary': 'Die Änderung ist geprüft.', 'state': 'review_ready',
                'delivery': 'pending', 'owner': 'Review-Team',
                'evidence': [{'label': 'Prüfung', 'url': 'https://example.org/pr/1'}],
                'decision': {'id': 'd-1', 'state': 'open', 'question': 'Variante wählen?',
                             'url': 'https://example.org/decisions/d-1', 'options': ['A', 'B']}}
        text = project_buzz.render_report(spec)
        self.assertTrue(text.startswith('Nicht live:'))
        self.assertEqual(text.count('Variante wählen?'), 1)
        self.assertIn('https://example.org/pr/1', text)
        self.assertIn('Review-Team', text)

    def test_report_does_not_invent_deployment_for_analysis(self):
        text = project_buzz.render_report({'summary': 'Prüfung abgeschlossen.', 'state': 'analysed',
                                          'delivery': 'not_required', 'evidence': []})
        self.assertNotIn('Nicht live', text)
        self.assertIn('nicht erforderlich', text)

    def test_report_rejects_false_live_state_and_unsafe_links(self):
        for spec in [dict(summary='Fertig.', state='review_ready', delivery='live', evidence=[]),
                     dict(summary='Geprüft.', state='analysed', delivery='not_required',
                          evidence=[dict(label='Beleg', url='javascript:alert(1)')])]:
            with self.assertRaises(project_buzz.UserError):
                project_buzz.render_report(spec)

    def test_withdrawn_decision_is_not_an_open_action(self):
        text = project_buzz.render_report(dict(summary='Stand geprüft.', state='analysed',
            delivery='not_required', evidence=[], decision=dict(id='d-1', state='withdrawn',
            question='Entfernen?', url='https://example.org/decisions/d-1', options=['Ja', 'Nein'])))
        self.assertIn('zurückgezogen', text)
        self.assertNotIn('1. Ja', text)

    def test_mobile_sketch_bounds_and_long_labels(self):
        svg = project_buzz.skizze_svg({'typ': 'ablauf', 'layout': 'mobil',
            'titel': 'Ein langer Titel ' * 8, 'schritte': ['A' * 90, 'Zweiter Schritt', 'Ende']})
        root = ET.fromstring(svg)
        width = float(root.attrib['width'])
        self.assertLessEqual(width, 480)
        for node in root.iter():
            if node.tag.endswith('rect'):
                self.assertLessEqual(float(node.get('x', 0))+float(node.get('width', 0)), width)
            if node.tag.endswith('text'):
                self.assertLessEqual(len(node.text or ''), 48)

    def test_sketch_rejects_unbounded_input(self):
        with self.assertRaises(project_buzz.UserError):
            project_buzz.skizze_svg({'typ': 'ablauf', 'schritte': ['x'] * 101})

    def test_code_image_syntax_cannot_hide_visible_words(self):
        text = '```text\n![' + 'wort ' * 310 + '](https://example.org)\n```'
        self.assertTrue(project_buzz.komm_check(text, 'buzz')[0])

    def test_notice_is_top_level_without_broadcast(self):
        self.run_cli(['notice', 'notice-1', 'b' * 64, 'Ergebnis geprüft.', 'codeapp'])
        call = self.calls()[-1]
        self.assertNotIn('--broadcast', call)
        self.assertNotIn('--reply-to', call)
        self.assertIn('id=' + 'b' * 64, call[call.index('--content') + 1])

    def test_routine_reuses_daily_root_and_deduplicates_finding(self):
        args = ('routine', '2026-10-24', 'a' * 16, 'Ein neuer Befund.', 'codeapp')
        self.run_cli(list(args))
        self.run_cli(list(args))
        sends = [x for x in self.calls() if x[:2] == ['messages', 'send']]
        self.assertEqual(len(sends), 2)
        self.assertNotIn('--reply-to', sends[0])
        self.assertIn('--reply-to', sends[1])
        self.assertNotIn('--broadcast', sends[1])

    def test_chart_preserves_missing_values_and_requires_units_and_source(self):
        spec = dict(typ='messwerte', einheit='ms', quelle='Lokale Testdaten',
                    werte=[dict(name='A', wert=4), dict(name='B', wert=None)])
        svg = project_buzz.skizze_svg(spec)
        self.assertIn('nicht gemessen', svg)
        self.assertIn('4 ms', svg)
        del spec['einheit']
        with self.assertRaises(project_buzz.UserError):
            project_buzz.skizze_svg(spec)

    def test_invalid_types_fail_as_user_errors(self):
        for spec in [dict(state=[]), dict(state='verified', delivery='not_required')]:
            with self.assertRaises(project_buzz.UserError):
                project_buzz.render_report(spec)
        with self.assertRaises(project_buzz.UserError):
            project_buzz.skizze_svg(dict(schritte=['A'], ton=[]))

    def test_routine_preserves_recurrence_after_recovery(self):
        for fingerprint, content in [('a'*16, 'Störung.'), ('b'*16, 'Erholt.'), ('a'*16, 'Störung.')]:
            self.run_cli(['routine', '2026-10-24', fingerprint, content, 'codeapp'])
        sends = [x for x in self.calls() if x[:2] == ['messages', 'send']]
        self.assertEqual(len(sends), 4)

    def test_notice_cannot_reuse_a_progress_receipt(self):
        self.run_cli(['progress', 'same-id', 'b'*64, 'Zwischenstand.', 'codeapp'])
        self.run_cli(['notice', 'same-id', 'b'*64, 'Ergebnis.', 'codeapp'])
        sends = [x for x in self.calls() if x[:2] == ['messages', 'send']]
        self.assertEqual(len(sends), 2)

    def test_routine_reports_a_corrupt_checkpoint_as_user_error(self):
        args = ('routine', '2026-10-24', 'a' * 16, 'Erster Befund.', 'codeapp')
        self.run_cli(list(args))
        config = project_buzz.load_config()
        repo, channel = project_buzz.resolve_project(config, 'codeapp')
        agent = project_buzz.agent_name(config)
        path = (project_buzz.state_root() / 'routines' /
                '{0}-{1}-{2}-2026-10-24.json'.format(repo, channel, agent))
        path.write_text('{broken', encoding='utf-8')
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(1, self.run_cli(list(args)))
        self.assertIn('ist kein gültiges JSON', err.getvalue())
        self.assertIn('routines', err.getvalue())

    def test_in_progress_lock_error_names_the_recovery_doc(self):
        os.chdir(self.workspace)
        config = project_buzz.load_config()
        repo, channel = project_buzz.resolve_project(config, 'codeapp')
        lock = project_buzz.lock_directory(repo, 'claude.stratos', 'progress', 'stale-1')
        lock.mkdir(parents=True)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(1, self.run_cli(
                ['progress', 'stale-1', 'b' * 64, 'Text', 'codeapp']))
        message = err.getvalue()
        self.assertIn('retry with the same update ID', message)
        self.assertIn('docs/COMMUNICATION-ROLLOUT.md', message)
        self.assertIn(str(lock), message)
