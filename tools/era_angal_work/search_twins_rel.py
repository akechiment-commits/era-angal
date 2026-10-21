import os
import re

# Search all files mentioning 双葉みづき or 双葉みなづき relationship
out = []
files_to_check = [
    'tools/output/みづき・みなづき.txt',
    'tools/output/みづき・みなづき_関係性.txt',
    'tools/output/みづき_関係性.txt',
    'tools/output/みなづき_関係性.txt',
    'tools/output/みづき.txt',
    'tools/output/みなづき.txt'
]

for fpath in files_to_check:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            t = f.read()
        out.append(f"=== File: {fpath} ===")
        # search for 呼び方 or お互い or 呼称
        for l in t.splitlines():
            if any(k in l for k in ['呼', 'お姉', '妹', 'みな', 'みづ', 'あだ名', 'ちゃん']):
                if any(x in l for x in ['みづき', 'みなづき', '双子', '姉', '妹']):
                    out.append(l.strip()[:100])

with open('tools/era_angal_work/twins_rel_search.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out[:200]))

print("Saved twins_rel_search.txt")
