"""Build an allowlisted reproducible archive; explicit new local output directory only."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

FILES = ['README.zh.md', 'CHANGELOG.zh.md', 'lab.py', 'package_lab.py', 'tests/test_lab.py',
         'fixtures/meeting.json', 'fixtures/submission-template.json', 'fixtures/submission-good.json',
         'fixtures/submission-bad.json', 'fixtures/review-template.json', 'expected/good-report.json',
         'expected/bad-report.json', 'expected/reviewed-draft.json']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args=p.parse_args()
    root=Path(__file__).resolve().parent
    out=Path(args.out)
    out.mkdir(parents=False,exist_ok=False)
    archive=out/'meeting-action-lab-r1.zip'
    hashes={}
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
        for relative in sorted(FILES):
            data=(root/relative).read_bytes()
            member='meeting-action-lab/'+relative
            info=zipfile.ZipInfo(member,date_time=(2020,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644 << 16
            info.compress_type=zipfile.ZIP_STORED
            z.writestr(info,data)
            hashes[member]=hashlib.sha256(data).hexdigest()
    manifest={'algorithm':'sha256','archive':archive.name,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'members':hashes}
    (out/'SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'archive':archive.name,'sha256':manifest['archive_sha256'],'members':len(hashes)},sort_keys=True))

if __name__=='__main__':main()
