"""Regresiones de los filtros que causaron falsas ejecuciones fallidas en Actions."""
import unittest

from catalog import cases
from select_tag import normalize_tag, resolve_tag


class SelectTagTests(unittest.TestCase):
    def test_case_variations_use_the_actual_gherkin_tag(self):
        for value in ('TC13', 'tc13', 'Tc13', '@TC13', '@tc13', '  @tC13  '):
            with self.subTest(value=value):
                self.assertEqual('@TC13', normalize_tag(value))

    def test_every_case_and_real_issue_resolves(self):
        for case in cases():
            for tag in ('@' + case['id'], '@GH-' + str(case['issue'])):
                with self.subTest(tag=tag):
                    self.assertEqual(tag, normalize_tag(tag.lower()))

    def test_feature_and_smoke_tags(self):
        for tag in ('api', 'barista', 'climatizacion', 'smoketest'):
            self.assertEqual('@' + tag, normalize_tag('@' + tag.upper()))

    def test_full_suite_aliases(self):
        for value in ('', ' ', None, 'todos', 'TODOS', 'all'):
            self.assertEqual('', normalize_tag(value))

    def test_issue_event_uses_issue_number(self):
        self.assertEqual('@GH-13', resolve_tag('issues', {'issue': {'number': 13}}, 'TC01'))

    def test_manual_and_reusable_events_use_requested_input(self):
        for event in ('workflow_dispatch', 'workflow_call', 'push'):
            self.assertEqual('@TC13', resolve_tag(event, {}, '@tc13'))

    def test_nonexistent_tags_do_not_become_full_suite(self):
        for value in ('TC00', 'TC23', 'TC99', '@GH-99999'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_tag(value)

    def test_malformed_or_multiple_tags_are_rejected(self):
        for value in ('@', '@@TC13', 'TC1', 'TC001', '@TC13 or @TC01', 'GH-0', 'TC13\nTC14', '--help', '$(whoami)'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_tag(value)


if __name__ == '__main__':
    unittest.main()
