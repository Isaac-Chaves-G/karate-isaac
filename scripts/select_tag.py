"""Valida la selección de Actions y devuelve el tag real escrito en el Gherkin."""
import json
import os
import re

from catalog import cases


def normalize_tag(value, catalog=None):
    raw = (value or '').strip()
    if raw.startswith('@'):
        raw = raw[1:]
        if not raw:
            raise ValueError('Falta el nombre del tag después de @')
    if raw.casefold() in ('', 'todos', 'all'):
        return ''
    # Solo un tag; no se aceptan expresiones ni opciones de Karate desde el input.
    if not re.fullmatch(r'TC\d{2}|GH-[1-9]\d*|smoketest|api|barista|climatizacion', raw, re.I):
        raise ValueError('Tag inválido: usa TC01, GH-1, smoketest, barista, climatizacion o todos, con o sin @.')
    catalog = cases() if catalog is None else catalog
    available = {'@api', '@barista', '@climatizacion'}
    available.update(tag for case in catalog for tag in case['tags'])
    canonical = {tag.casefold(): tag for tag in available}
    try:
        return canonical['@' + raw.casefold()]
    except KeyError:
        raise ValueError(f'El tag @{raw} no está vinculado a ningún escenario') from None


def resolve_tag(event_name, event, requested):
    if event_name == 'issues':
        requested = 'GH-' + str(event['issue']['number'])
    return normalize_tag(requested)


def main():
    with open(os.environ['GITHUB_EVENT_PATH'], encoding='utf-8') as source:
        event = json.load(source)
    try:
        tag = resolve_tag(os.environ['GITHUB_EVENT_NAME'], event, os.environ.get('REQUESTED_TAG', ''))
    except (ValueError, KeyError) as error:
        raise SystemExit(str(error)) from None
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
        output.write(f'tag={tag}\n')
    print('Selección: ' + (tag or 'suite completa'))


if __name__ == '__main__':
    main()
