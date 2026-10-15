"""Publica los casos en el repositorio configurado usando la sesión oficial de gh."""
import json
import re
import subprocess
from catalog import ROOT, REPO, generate


def gh(*args):
    return subprocess.run(['gh', *args], check=True, capture_output=True, text=True, encoding='utf-8').stdout.strip()


def main():
    gh('repo', 'view', REPO, '--json', 'nameWithOwner')
    for name, color in [('testcase', '0E8A16'), ('barista', 'A0522D'), ('climatizacion', '1D76DB'),
                        ('ejecutar-prueba', '5319E7'), ('automated-passed', '0E8A16'),
                        ('automated-failed', 'D93F0B'), ('bug', 'B60205')]:
        gh('label', 'create', name, '--repo', REPO, '--color', color, '--force')
    existing = json.loads(gh('issue', 'list', '--repo', REPO, '--state', 'all', '--limit', '1000', '--json', 'number,title,url'))
    by_case = {}
    for issue in existing:
        match = re.match(r'^\[(TC\d{2})\]', issue['title'])
        if match:
            if match[1] in by_case:
                raise ValueError(f'Dos issues para {match[1]}; resolver antes de continuar')
            by_case[match[1]] = issue
    mapping = {'repository': REPO, 'cases': {}}
    created = set()
    for case in generate():
        issue = by_case.get(case['id'])
        if issue is None:
            title = f"[{case['id']}] {case['title']}"
            url = gh('issue', 'create', '--repo', REPO, '--title', title,
                     '--body-file', str(ROOT / 'docs/issues' / f"{case['id']}.md"),
                     '--label', 'testcase', '--label', case['module'])
            issue = dict(number=int(url.rsplit('/', 1)[1]), title=title, url=url)
            created.add(case['id'])
        mapping['cases'][case['id']] = issue
        (ROOT / 'docs/github-mapping.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        path = ROOT / case['feature']
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'^  @' + case['id'] + r'\b[^\n]*',
                      lambda m: re.sub(r'\s+@GH-\d+\b', '', m[0]) + f" @GH-{issue['number']}", text, flags=re.M)
        path.write_text(text, encoding='utf-8')
        print(f"{case['id']} -> {issue['url']}")
    generate()
    for case_id in created:
        gh('issue', 'edit', str(mapping['cases'][case_id]['number']), '--repo', REPO,
           '--body-file', str(ROOT / 'docs/issues' / f'{case_id}.md'))


if __name__ == '__main__':
    main()
