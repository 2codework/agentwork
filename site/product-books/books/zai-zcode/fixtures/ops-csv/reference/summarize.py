import csv,json
from pathlib import Path
rows=list(csv.DictReader(Path("orders.csv").open()))
valid=[]; errors=[]
for row in rows:
    if row["status"] != "paid": continue
    if not row["amount_cents"].isascii() or not row["amount_cents"].isdigit():
        errors.append(row); continue
    valid.append(int(row["amount_cents"]))
Path("summary.json").write_text(json.dumps({"paid_count":len(valid),"revenue_cents":sum(valid)},sort_keys=True)+"\n")
with Path("errors.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["order_id","status","amount_cents"]); w.writeheader(); w.writerows(errors)
