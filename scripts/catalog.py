"""Deriva casos e issues del Gherkin; nunca asigna números de issue ficticios."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Isaac-Chaves-G/karate-isaac'


def cases():
    result = []
    for path in sorted((ROOT / 'src/test/resources/features').glob('*.feature')):
        text = path.read_text(encoding='utf-8')
        pattern = r'^  (@TC\d+[^\n]*)\n  (Scenario(?: Outline)?): ([^\n]+)\n(.*?)(?=\n  @TC|\Z)'
        for match in re.finditer(pattern, text, re.M | re.S):
            tags, kind, title, steps = match.groups()
            issue = re.search(r'@GH-(\d+)\b', tags)
            result.append(dict(id=re.search(r'@TC\d+', tags)[0][1:], title=title,
                               tags=tags.split(), feature=path.relative_to(ROOT).as_posix(),
                               module=path.stem, steps=steps.strip(), kind=kind,
                               issue=int(issue[1]) if issue else None))
    result.sort(key=lambda item: item['id'])
    if [c['id'] for c in result] != [f'TC{i:02d}' for i in range(1, 23)]:
        raise ValueError('Se requieren TC01..TC22, sin duplicados')
    return result


def generate():
    catalog = cases()
    out = ROOT / 'docs/issues'
    out.mkdir(parents=True, exist_ok=True)
    table = ['# Trazabilidad', '', '| Caso | Escenario | Requisito | Issue |', '|---|---|---|---|']
    for case in catalog:
        requirements = ', '.join(t for t in case['tags'] if t.startswith('@REQ-'))
        issue = f"[#{case['issue']}](https://github.com/{REPO}/issues/{case['issue']})" if case['issue'] else 'Pendiente'
        table.append(f"| {case['id']} | {case['title']} | {requirements} | {issue} |")
        tag = f"@GH-{case['issue']}" if case['issue'] else '@' + case['id']
        body = f"# {case['id']}: {case['title']}\n\nRequisito: {requirements}.\n\n"
        body += f"Archivo: `{case['feature']}`.\n\n"
        body += '## Precondiciones y resultado esperado\n\n'
        body += 'Barista se reinicia y alcanza su estado inicial mediante `barista-state.feature`; no depende del caso anterior. Climatización recibe tres booleanos: temperatura alta, presencia y apertura prolongada.\n\n'
        body += f"```gherkin\n{case['kind']}: {case['title']}\n{case['steps']}\n```\n\n"
        body += f"## Ejecución\n\nAñade la etiqueta **ejecutar-prueba** a este issue, o abre Actions → Karate API → Run workflow y escribe `{tag}`. Para repetir desde el issue, quita la etiqueta y vuelve a añadirla.\n\n"
        body += f"Local: `./gradlew clean test '-Dkarate.options=--tags {tag}'`.\n\n"
        body += '## Evidencia\n\nEl workflow publica el resultado y el enlace a la corrida en este issue, y actualiza `automated-passed` o `automated-failed`. Descarga `karate-reports-N` en Artifacts y abre `karate-summary.html`. Un fallo no demuestra por sí solo un bug: revisa la respuesta y las precondiciones.\n'
        (out / f"{case['id']}.md").write_text(body, encoding='utf-8')
    (ROOT / 'docs/TRAZABILIDAD.md').write_text('\n'.join(table) + '\n', encoding='utf-8')
    (ROOT / 'docs/testcases.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return catalog


if __name__ == '__main__':
    print(f'{len(generate())} casos catalogados')
