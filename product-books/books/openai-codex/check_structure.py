"""Small stdlib validator for the JSON-schema keywords used in this package, not a general JSON Schema implementation."""
import json,re,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent

def check(value,schema,path='$'):
    if 'const' in schema: assert value==schema['const'],(path,'const')
    if 'type' in schema:
        types=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
        kind='null' if value is None else 'boolean' if isinstance(value,bool) else 'object' if isinstance(value,dict) else 'array' if isinstance(value,list) else 'string' if isinstance(value,str) else 'integer' if isinstance(value,int) else 'number'
        assert kind in types,(path,'type',kind,types)
    if isinstance(value,dict):
        for key in schema.get('required',[]):assert key in value,(path,'missing',key)
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False:assert not set(value)-set(props),(path,'extra',set(value)-set(props))
        for key,sub in props.items():
            if key in value:check(value[key],sub,path+'.'+key)
    if isinstance(value,list):
        assert len(value)>=schema.get('minItems',0),(path,'minItems')
        assert len(value)<=schema.get('maxItems',10**9),(path,'maxItems')
        if 'items' in schema:
            for i,item in enumerate(value):check(item,schema['items'],path+f'[{i}]')
    if isinstance(value,str) and 'pattern' in schema:assert re.search(schema['pattern'],value),(path,'pattern')
book=json.loads((R/'product-book.json').read_text());schema=json.loads((R/'schema.json').read_text());check(book,schema)
ids=set()
for recipe in book['recipes']:
    assert recipe['recipe_id'] not in ids;ids.add(recipe['recipe_id'])
    for item in recipe['input_artifacts']:
        p=(R/item['path']).resolve();assert p.is_relative_to(R)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],item['path']
    for p in recipe['expected_output']['files']:assert (R/p).is_file(),p
    for s in recipe['sources']:assert s['url'].startswith('https://learn.chatgpt.com/')
print('PASS: package schema subset, unique recipe IDs, input hashes, output paths, official sources')
