#!/usr/bin/env python3
"""Offline Pages parity, strict JSON and local HTML-link checks (stdlib only)."""
import json
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import product_negative_fixtures

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


# Closed negative-fixture registry: these bytes are deliberately NOT valid JSON.
# Names are preserved from the reviewed downloadable lab, never skipped by glob.
CREATIVE_NEGATIVE_FIXTURES = {
    'creative-delivery/r1/source/fixtures/submission-F12a.json': ('625f269d97fafc62b0d010531cad6f1003e55df28af8c8318bb766c9ed8c2a64', 'duplicate JSON key'),
    'creative-delivery/r1/source/fixtures/submission-F12b.json': ('6582fb24bf94678940f760a910b37ee00c1c1a137b0affffff0caa832b0c9c11', 'non-finite JSON constant'),
    'creative-delivery/r1/source/fixtures/submission-F12d.json': ('76c002eec0c9da854ca2ee5dae9fb0069a622274b6638ab712fcb70384304899', 'oversize whitespace-only payload'),
}
NEGATIVE_REGISTRY_SHA = '9ace8359e6da8d9eb4186c0a1f17fe53f289fcb1acb1055ef7c6cba694f7034c'


def negative_fixture(path, directory):
    name=path.relative_to(directory).as_posix()
    if name not in CREATIVE_NEGATIVE_FIXTURES:
        return False
    expected,reason=CREATIVE_NEGATIVE_FIXTURES[name]
    data=path.read_bytes()
    require(hashlib.sha256(data).hexdigest()==expected, 'negative fixture frozen bytes changed: '+name)
    if reason=='oversize whitespace-only payload':
        require(len(data)==65537 and data.strip()==b'', 'negative fixture expected oversize role changed')
        try: json.loads(data.decode('utf-8'),object_pairs_hook=unique_object,parse_constant=invalid_constant)
        except json.JSONDecodeError: return True
        raise ValueError('negative fixture unexpectedly valid JSON')
    try: json.loads(data.decode('utf-8'),object_pairs_hook=unique_object,parse_constant=invalid_constant)
    except ValueError as error:
        require(reason in str(error), 'negative fixture rejection reason changed')
        return True
    raise ValueError('negative fixture unexpectedly valid JSON')


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
    negative_count = 0
    product_negative_count = 0
    product_registry = product_negative_fixtures.registry()
    registry=json.dumps(CREATIVE_NEGATIVE_FIXTURES,sort_keys=True,separators=(',',':')).encode()
    require(hashlib.sha256(registry).hexdigest()==NEGATIVE_REGISTRY_SHA, 'negative fixture registry changed')
    for directory in (generated, pages):
        present={name for name in CREATIVE_NEGATIVE_FIXTURES if (directory/name).is_file()}
        if (directory/'creative-delivery').exists() or (root/'learning/creative-delivery/r1').exists():
            require(present==set(CREATIVE_NEGATIVE_FIXTURES), 'negative fixture closed set missing')
        if (directory/'product-books/books/wps-lingxi-pro/product-book.json').is_file():
            require({name for name in product_registry if (directory/name).is_file()}==set(product_registry),'product negative closed set missing')
        for path in directory.rglob('*.json'):
            if negative_fixture(path,directory):
                negative_count += 1
                continue
            if product_negative_fixtures.check(path,directory):
                product_negative_count += 1
                continue
            product_negative_fixtures.loads(path.read_text(encoding='utf-8'))
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
    print(f'Pages parity: {len(generated_files)} files; strict-valid JSON: {json_count}; fixed invalid teaching fixtures: {negative_count} (3 kinds per copy); product expected-invalid fixtures: {product_negative_count}; HTML: {len(parsed)}. External links not fetched.')


if __name__ == '__main__':
    check()
