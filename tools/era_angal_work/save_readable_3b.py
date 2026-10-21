import json

with open('tools/era_angal_work/3b_profiles.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('tools/era_angal_work/3b_profiles_readable.txt', 'w', encoding='utf-8') as out:
    for cid, p in sorted(d.items(), key=lambda x: int(x[0])):
        out.write(f"ID {int(cid):02d}: {p['name']} | Class: {p.get('class')} | Club: {p.get('club')} | Comm: {p.get('committee')}\n")
        out.write(f"   Intro: {p.get('intro')}\n\n")

print("Saved 3b_profiles_readable.txt")
