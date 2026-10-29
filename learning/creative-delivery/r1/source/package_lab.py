"""Package only the fixed author allowlist into a NEW directory; never package user data."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from lab import safe_read
from contract import Invalid
ROOT=Path(__file__).resolve().parent
CASES=('good','F01','F02','F03','F04','F05','F06a','F06b','F07a','F07b','F08','F09','F10a','F10b','F10c','F11a','F11b','F11c','F11d','F11e','F12a','F12b','F12c','F12d')
MEMBERS=('README.zh.md','CONTRACT.zh-CN.md','lab.py','contract.py','timeline.py','package_lab.py','tests/test_lab.py','expected/cases.json','expected/HAND_ORACLE.r3.json','fixtures/source.json','fixtures/edit.json','fixtures/submission-template.json')+tuple('fixtures/submission-'+n+'.json' for n in CASES)

def build(out):
    # All inputs preflight before any output is created; fixed names, no recursive collection.
    payload={name:safe_read(ROOT/name, max_bytes=65537) for name in sorted(MEMBERS)}
    out=Path(out);out.mkdir(parents=False,exist_ok=False)
    archive=out/'creative-delivery-lab-r1.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_STORED) as z:
        for name,data in payload.items():
            info=zipfile.ZipInfo('creative-delivery-lab/'+name,date_time=(2020,1,1,0,0,0))
            info.create_system=3;info.external_attr=0o100644<<16
            info.compress_type=zipfile.ZIP_STORED
            z.writestr(info,data)
    result=dict(archive=archive.name,archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),members={'creative-delivery-lab/'+n:hashlib.sha256(d).hexdigest() for n,d in payload.items()},mode='rule-simulation',publish_allowed=False)
    (out/'SHA256.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args()
    try: result=build(args.out)
    except (OSError,Invalid):
        print(json.dumps(dict(status='invalid',error='PACKAGE_INPUT_OR_OUTPUT_INVALID',publish_allowed=False)))
        return 2
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2));return 0

if __name__=='__main__': raise SystemExit(main())
