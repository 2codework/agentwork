"""Offline entry-label contract, not a browser accessibility-tree audit.

ENTRY_LABEL_ROOT can point at an old checkout to demonstrate regression failures.
"""
from html.parser import HTMLParser
import os
from pathlib import Path
import unittest

ROOT = Path(os.environ.get('ENTRY_LABEL_ROOT', Path(__file__).resolve().parents[1]))


class Element:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self, accessible=False):
        if accessible and self.attrs.get('aria-hidden') == 'true':
            return ''
        return ''.join(c.text(accessible) if isinstance(c, Element) else c
                       for c in self.children)

    def name(self):
        return self.attrs.get('aria-label', self.text(accessible=True)).strip()


class EntryParser(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.stack = [Element()]
        self.entries = {}
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs)
        self.stack[-1].children.append(node)
        for cls in node.attrs.get('class', '').split():
            if cls in ('brand', 'search-label', 'edition'):
                if cls in self.entries:
                    raise AssertionError('duplicate entry: ' + cls)
                self.entries[cls] = node
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img',
                       'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append(node)

    def handle_endtag(self, tag):
        assert self.stack[-1].tag == tag, 'unbalanced HTML: ' + tag
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)


class EntryLabelsTests(unittest.TestCase):
    def entries(self):
        for folder in ('web', 'site', 'docs'):
            yield folder, EntryParser((ROOT / folder / 'index.html').read_text()).entries

    def test_brand_clear_and_decoration_hidden(self):
        for folder, entries in self.entries():
            with self.subTest(folder=folder):
                brand = entries['brand']
                self.assertEqual(brand.tag, 'a')
                self.assertEqual(brand.attrs['href'], '?view=home')
                self.assertEqual(brand.text().strip(), 'AW AgentWork')
                self.assertEqual(brand.name(), 'AgentWork 首页')
                self.assertEqual(brand.text(accessible=True).strip(), 'AgentWork')
                self.assertEqual(brand.children[0].attrs.get('aria-hidden'), 'true')

    def test_search_replaces_hero_cta_with_explicit_accessible_label(self):
        for folder, entries in self.entries():
            with self.subTest(folder=folder):
                label = entries['search-label']
                self.assertEqual(label.tag, 'label')
                self.assertEqual(label.attrs['for'], 'search')
                self.assertEqual(label.name(), '搜索实践')
                html = (ROOT / folder / 'index.html').read_text()
                self.assertIn('id="search" type="search"', html)
                self.assertIn('id="clear" type="button">清空筛选', html)
                self.assertNotIn('class="hero"', html)

    def test_edition_is_batch_independent(self):
        for folder, entries in self.entries():
            with self.subTest(folder=folder):
                self.assertEqual(entries['edition'].text(), '开放实践手册')


if __name__ == '__main__':
    unittest.main()
