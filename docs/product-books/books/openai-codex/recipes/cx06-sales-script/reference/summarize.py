import csv, json, sys

def summarize(path):
    totals={}; seen={}; duplicates=0
    with open(path,newline='',encoding='utf8') as f:
        for row in csv.DictReader(f):
            key=row['id']
            if key in seen:
                if seen[key] != row: raise ValueError('conflicting duplicate')
                duplicates+=1; continue
            seen[key]=dict(row)
            amount=int(row['amount_cents'])
            if amount<0 or row['status'] not in ('paid','refund','cancelled'): raise ValueError('invalid row')
            if row['status']=='cancelled': continue
            totals[row['region']]=totals.get(row['region'],0)+(amount if row['status']=='paid' else -amount)
    return {'net_cents':dict(sorted(totals.items())), 'duplicate_rows':duplicates}
if __name__=='__main__': print(json.dumps(summarize(sys.argv[1]),sort_keys=True))
