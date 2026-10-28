# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

def check_seniors(cname):
    print(f"=== {cname} senior calls ===")
    with open(f'tools/output/{cname}.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    hits = [l.strip() for l in lines if any(k in l for k in ['先輩', 'せんぱい', '部長', '会長'])]
    print(f"Total senior-word hits: {len(hits)}")
    for h in hits[:10]:
        print(f"  {h[:120]}")

for cn in ['ゆり', 'こよい', 'なな', 'ゆう']:
    check_seniors(cn)
