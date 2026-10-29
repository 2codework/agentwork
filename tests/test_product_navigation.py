import copy, hashlib, importlib.util, json, tempfile, unittest, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pbnav',ROOT/'scripts/product_books.py');pb=importlib.util.module_from_spec(spec);spec.loader.exec_module(pb)
class Navigation(unittest.TestCase):
 def test_role_facets_preserve_every_source_role_and_are_complete(self):
  books=pb.catalog()['books'];count=0
  for b in books:
   original=pb.load(ROOT/'product-books/books'/b['product']['product_id']/'product-book.json')
   for old,new in zip(original['recipes'],b['recipes']):
    self.assertEqual(old['role'],new['role']);self.assertTrue(new['role_tags']);self.assertTrue(all(len(x)<=12 for x in new['role_tags']));count+=1
  self.assertEqual(32,count)
 def test_all_thirteen_known_source_routes_are_hashed_local_and_resolve(self):
  books=pb.catalog()['books'];routes=[route for b in books for route in b['handbook_routes'].values()];self.assertEqual(13,len(routes))
  self.assertEqual(8,sum(r['kind']=='recipe' for r in routes));self.assertEqual(5,sum(r['kind']=='handbook' for r in routes))
  for route in routes:self.assertEqual(route['source_sha256'],hashlib.sha256((ROOT/'product-books'/route['source_path']).read_bytes()).hexdigest())
 def test_invalid_navigation_source_or_binding_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);shutil.copytree(ROOT/'product-books',root/'product-books');folder=root/'product-books';original=pb.load(folder/'editorial-navigation.json')
   for mode in ['traversal','hash','wrong_recipe','role_source','long_role']:
    nav=copy.deepcopy(original)
    if mode=='traversal':nav['handbook_routes'][0]['href']='../MANUAL.md'
    elif mode=='hash':nav['handbook_routes'][0]['source_sha256']='0'*64
    elif mode=='wrong_recipe':nav['handbook_routes'][0]['kind']='recipe';nav['handbook_routes'][0]['target_id']='unknown'
    elif mode=='role_source':next(iter(nav['role_facets'].values()))['source_role']='fabricated'
    else:next(iter(nav['role_facets'].values()))['role_tags']=['x'*50]
    file=folder/'editorial-navigation.json';file.write_text(json.dumps(nav));idx=pb.load(folder/'index.json');idx['publication_files']['editorial-navigation.json']=hashlib.sha256(file.read_bytes()).hexdigest();(folder/'index.json').write_text(json.dumps(idx))
    with self.subTest(mode=mode):
     with self.assertRaises(ValueError):pb.catalog(root)
if __name__=='__main__':unittest.main()
