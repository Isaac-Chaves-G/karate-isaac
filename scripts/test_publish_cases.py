"""Verifica la actualización de alcance de un issue existente sin llamadas a GitHub."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from publish_cases import REPO, update_issue_bodies


class PublishCasesTests(unittest.TestCase):
    def test_existing_issue_preserves_manual_notes_and_only_updates_tc22(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            (root / 'docs/issues').mkdir(parents=True)
            (root / 'docs/issues/TC01.md').write_text('Caso sin cambios\n', encoding='utf-8')
            changed = root / 'docs/issues/TC22.md'
            changed.write_text('**Alcance revisado:** cinco estructuras.\n', encoding='utf-8')
            mapping = {'cases': {'TC01': {'number': 1}, 'TC22': {'number': 22}}}
            previous = {'TC01': 'Notas manuales que difieren del generado',
                        'TC22': "Nota manual inicial\n```gherkin\n      | valor no booleano | { valores: [true, 'si', false] }  |\n```\nNota manual final"}
            with patch('publish_cases.ROOT', root), patch('publish_cases.gh') as gh:
                update_issue_bodies(mapping, previous, set())
                destination = root / 'target/issue-TC22-actualizado.md'
                gh.assert_called_once_with('issue', 'edit', '22', '--repo', REPO,
                                           '--body-file', str(destination))
                updated = destination.read_text(encoding='utf-8')
                self.assertTrue(updated.startswith('Nota manual inicial'))
                self.assertTrue(updated.endswith('Nota manual final'))
                self.assertIn('**Alcance revisado:** cinco estructuras.', updated)
                self.assertNotIn('valor no booleano', updated)

    def test_new_issue_receives_final_body_with_its_real_tag(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            (root / 'docs/issues').mkdir(parents=True)
            body = root / 'docs/issues/TC22.md'
            body.write_text('Caso vinculado a @GH-22\n', encoding='utf-8')
            with patch('publish_cases.ROOT', root), patch('publish_cases.gh') as gh:
                update_issue_bodies({'cases': {'TC22': {'number': 22}}}, {}, {'TC22'})
                gh.assert_called_once_with('issue', 'edit', '22', '--repo', REPO,
                                           '--body-file', str(body))


if __name__ == '__main__':
    unittest.main()
