"""Resume Cucumber JSON por TC. Solo publica si se solicita --publish."""
import argparse
import json
import os
import re
from pathlib import Path
from catalog import ROOT, cases
from publish_cases import gh


def collect(directory):
    results = {}
    for path in Path(directory).glob('*.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, list):
            continue
        for feature in data:
            if not isinstance(feature, dict):
                continue
            for element in feature.get('elements', []):
                if element.get('type') != 'scenario':
                    continue
                tags = [t['name'] for t in element.get('tags', [])]
                case_id = next((t[1:] for t in tags if re.fullmatch(r'@TC\d{2}', t)), None)
                if not case_id:
                    continue
                steps = element.get('before', []) + element.get('steps', []) + element.get('after', [])
                statuses = [s.get('result', {}).get('status', 'unknown') for s in steps]
                passed = bool(statuses) and all(s == 'passed' for s in statuses)
                result = results.setdefault(case_id, {'passed': 0, 'failed': 0, 'errors': []})
                result['passed' if passed else 'failed'] += 1
                result['errors'].extend(s['result']['error_message'][:2000] for s in steps if s.get('result', {}).get('error_message'))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    results = collect(ROOT / 'target/karate-reports')
    tag = os.environ.get('TEST_TAG', '')
    selected = [c for c in cases() if not tag or tag in c['tags'] or tag == '@api'
                or tag == '@' + c['module']]
    if not selected:
        raise SystemExit(f'El tag {tag} no selecciona casos del catálogo')
    summary = dict(cases=results, passed=sum(r['passed'] for r in results.values()),
                   failed=sum(r['failed'] for r in results.values()), missing=[c['id'] for c in selected if c['id'] not in results])
    out = ROOT / 'target/resultados.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print(f"::notice title=Resultados Karate::{summary['passed']} correctas; "
              f"{summary['failed']} fallidas; {len(summary['missing'])} casos sin evidencia")
        for case_id, result in sorted(results.items()):
            if result['failed']:
                print(f"::warning title={case_id}::{result['passed']} correctas y {result['failed']} fallidas; revisar reporte de este caso")
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        lines = ['## Resultados Karate', '',
                 f"Filtro: `{tag or 'suite completa'}`. "
                 f"**{summary['passed']} correctas, {summary['failed']} fallidas**. "
                 f"Casos sin evidencia: {len(summary['missing'])}.", '',
                 '| Caso | Correctas | Fallidas |', '|---|---:|---:|']
        for case in selected:
            result = results.get(case['id'])
            lines.append(f"| {case['id']} | {result['passed'] if result else 'sin evidencia'} | {result['failed'] if result else '—'} |")
        lines.extend(['', 'Un caso negativo pasa cuando el sistema rechaza correctamente la entrada. '
                      'Un fallo de aserción requiere revisar el reporte antes de atribuirlo a un defecto.'])
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as output:
            output.write('\n'.join(lines) + '\n')
    mapping_path = ROOT / 'docs/github-mapping.json'
    if not args.publish or not mapping_path.exists():
        if summary['missing']:
            raise SystemExit('Falta evidencia para: ' + ', '.join(summary['missing']))
        return
    mapping = json.loads(mapping_path.read_text(encoding='utf-8'))
    for case in selected:
        issue = mapping['cases'][case['id']]['number']
        result = results.get(case['id'])
        passed = result is not None and result['failed'] == 0
        state = 'PASSED' if passed else 'FAILED'
        detail = f"{result['passed']} ejecuciones correctas y {result['failed']} fallidas." if result else 'No se generó evidencia para este caso; revisar preparación o infraestructura.'
        body = f"**{case['id']}: {state}**\n\n{detail}\n\n[Ver ejecución y descargar reporte Karate]({os.environ['RUN_URL']}).\n\nUn resultado fallido requiere revisar el reporte antes de clasificarlo como bug."
        body_path = ROOT / 'target' / f"comment-{case['id']}.md"
        body_path.write_text(body, encoding='utf-8')
        gh('issue', 'comment', str(issue), '--repo', mapping['repository'], '--body-file', str(body_path))
        current = json.loads(gh('issue', 'view', str(issue), '--repo', mapping['repository'], '--json', 'labels'))
        remove = 'automated-failed' if passed else 'automated-passed'
        args = ['issue', 'edit', str(issue), '--repo', mapping['repository'], '--add-label', 'automated-passed' if passed else 'automated-failed']
        if remove in [label['name'] for label in current['labels']]:
            args.extend(['--remove-label', remove])
        gh(*args)
    if summary['missing']:
        raise SystemExit('Falta evidencia para: ' + ', '.join(summary['missing']))


if __name__ == '__main__':
    main()
