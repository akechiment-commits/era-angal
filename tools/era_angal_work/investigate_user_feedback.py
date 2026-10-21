import os
import re

out = []

# 1. Inspect Twin calls (みづき & みなづき)
out.append("=== 1. TWINS CALLS INSPECTION ===")
for fname in ['みづき.txt', 'みなづき.txt', 'みづき・みなづき.txt', 'みづき_関係性.txt', 'みなづき_関係性.txt']:
    p = os.path.join('tools/output', fname)
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            t = f.read()
        out.append(f"\n--- File: {fname} ---")
        
        # Look for dialogue lines: 「...」 or 【...】
        lines = t.splitlines()
        for l in lines:
            # check lines where one speaks to the other
            if any(k in l for k in ['姉', '妹', 'お姉', 'みなづき', 'みづき', '半身', '双子']):
                if len(l.strip()) > 0:
                    out.append("  " + l.strip()[:100])

# 2. Inspect Kasumi calls
out.append("\n=== 2. KASUMI CALLS INSPECTION ===")
kasumi_files = [f for f in os.listdir('tools/output') if 'かすみ' in f or '御影' in f]
out.append(f"Kasumi files: {kasumi_files}")
kasumi_text = ""
for kf in kasumi_files:
    with open(os.path.join('tools/output', kf), 'r', encoding='utf-8', errors='replace') as f:
        kasumi_text += f.read() + "\n"

# Look for quotes in Kasumi's text
quotes = re.findall(r'「([^」]+)」', kasumi_text)
out.append(f"Total quotes in Kasumi text: {len(quotes)}")
for q in quotes:
    out.append("  Kasumi quote: " + q)

# 3. Inspect Yako's call to Chika (トミ子 vs トミコ)
out.append("\n=== 3. YAKO CALLS CHIKA (トミ子 vs トミコ) ===")
yako_text = ""
for yf in [f for f in os.listdir('tools/output') if 'やこ' in f or '湖南' in f]:
    with open(os.path.join('tools/output', yf), 'r', encoding='utf-8', errors='replace') as f:
        yako_text += f.read() + "\n"

out.append(f"トミ子 count in Yako text: {len(re.findall(r'トミ子', yako_text))}")
out.append(f"トミコ count in Yako text: {len(re.findall(r'トミコ', yako_text))}")
for m in re.findall(r'([^。！？\n]{0,30}トミ[^。！？\n]{0,30})', yako_text)[:15]:
    out.append("  " + m.strip())

with open('tools/era_angal_work/feedback_result_utf8.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Saved UTF-8 result.")
