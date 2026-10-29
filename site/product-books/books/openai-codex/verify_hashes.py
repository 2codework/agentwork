from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
rows=json.loads((R/'SHA256SUMS.json').read_text())
for name,want in rows.items():
    p=(R/name).resolve();assert p.is_relative_to(R)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==want,name
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual==set(rows),'file inventory changed'
print(f'PASS: {len(rows)} file hashes and exact inventory')
