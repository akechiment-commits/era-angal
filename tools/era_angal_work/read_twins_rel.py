import os

files = [f for f in os.listdir('tools/output') if ('みづき' in f or 'みなづき' in f) and '関係性' in f]

with open('tools/era_angal_work/twins_rel_all.txt', 'w', encoding='utf-8') as out:
    for f in files:
        out.write(f"\n=====================================\n")
        out.write(f"FILE: {f}\n")
        with open(os.path.join('tools/output', f), 'r', encoding='utf-8', errors='replace') as inp:
            out.write(inp.read())

print("Saved twins_rel_all.txt")
