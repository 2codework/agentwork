#!/usr/bin/env python3
"""Offline Pages parity, strict JSON and local HTML-link checks (stdlib only)."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f'non-finite JSON constant: {value}')


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            require(attrs['id'] not in self.ids, 'duplicate HTML ID')
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


def check(root=ROOT):
    generated = root / ('site' if (root / 'content/cases.json').exists() else 'dist')
    pages = root / 'docs'
    require(generated.is_dir() and pages.is_dir(), 'missing generated/Pages directory')
    generated_files = [p for p in generated.rglob('*') if p.is_file()]
    require(generated_files, 'empty generated site')
    require((generated / '.nojekyll').is_file(), 'missing .nojekyll')
    for source in generated_files:
        relative = source.relative_to(generated)
        target = pages / relative
        require(not source.is_symlink() and not target.is_symlink(), f'symlink: {relative}')
        require(target.is_file(), f'Pages missing: {relative}')
        require(source.read_bytes() == target.read_bytes(), f'Pages differs: {relative}')
    # docs/ can also contain project documentation; these need not exist in site/.
    parsed = {}
    json_count = 0
    for directory in (generated, pages):
        for path in directory.rglob('*.json'):
            json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                       parse_constant=invalid_constant)
            json_count += 1
        for path in directory.rglob('*.html'):
            parser = Links()
            parser.feed(path.read_text(encoding='utf-8'))
            parsed[path.resolve()] = parser
    for path, parser in parsed.items():
        directory = generated if path.is_relative_to(generated.resolve()) else pages
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                require(url.scheme in ('https', 'http', 'mailto'), f'unsafe link: {link}')
                continue  # No external requests: HTTP status is not checked here.
            require(not url.path.startswith('/'), f'project-path incompatible link: {link}')
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            require(target.is_relative_to(directory.resolve()), f'link escapes site: {link}')
            if target.is_dir():
                target /= 'index.html'
            require(target.is_file(), f'broken local link: {link}')
            if url.fragment and target in parsed:
                require(unquote(url.fragment) in parsed[target].ids, f'broken anchor: {link}')
    print(f'Pages parity: {len(generated_files)} files; strict JSON: {json_count}; HTML: {len(parsed)}. External links not fetched.')


if __name__ == '__main__':
    check()
