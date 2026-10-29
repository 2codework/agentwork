"""Static layout contracts only: not rendered pixel/viewport evidence."""
import re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProductCatalogLayout(unittest.TestCase):
 def test_catalog_intro_one_line_heading_source_and_no_forced_line_break(self):
  html=(ROOT/'web/product-library.html').read_text();heading=re.search(r'<h1 id="catalog-title">(.*?)</h1>',html).group(1)
  self.assertEqual('产品使用书',heading);self.assertNotIn('<br',heading)
  description=re.search(r'<p id="catalog-description">(.*?)</p>',html).group(1);self.assertLess(len(description),60)
 def test_scoped_desktop_grid_and_narrow_single_column(self):
  css=(ROOT/'web/product-books.css').read_text();delta=css[css.index('/* r5:'):]
  self.assertIn('.catalog-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))',delta)
  self.assertIn('@media(max-width:760px){.catalog-grid{grid-template-columns:minmax(0,1fr)}',delta)
  self.assertIn('.catalog-intro:not([hidden])~#filters',delta)
  self.assertIn('.catalog-intro:not([hidden])~.layout',delta)
  self.assertNotIn('line-clamp',delta);self.assertNotIn('text-overflow',delta)
 def test_catalog_style_does_not_override_toc_or_detail_reading(self):
  css=(ROOT/'web/product-books.css').read_text();delta=css[css.index('/* r5:'):]
  self.assertNotIn('#toc',delta);self.assertNotIn('.handbook',delta);self.assertNotIn('#prerequisites',delta)
if __name__=='__main__':unittest.main()
