import json

with open('tools/era_angal_work/3b_profiles.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for cid, p in sorted(d.items(), key=lambda x: int(x[0])):
    print(f"ID {int(cid):02d}: {p['name']} | Class: {p.get('class')} | Club: {p.get('club')} | Comm: {p.get('committee')}")
    print(f"   Intro: {p.get('intro')}\n")
