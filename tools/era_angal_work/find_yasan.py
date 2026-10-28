import os
import re

files = [f for f in os.listdir('tools/output') if 'かすみ' in f or '御影' in f]
kasumi_text = ""
for f in files:
    with open(os.path.join('tools/output', f), 'r', encoding='utf-8', errors='replace') as fp:
        kasumi_text += fp.read() + "\n"

yasan_matches = re.findall(r'([^。！？\n]{0,15}[ぁ-んァ-ヶー一-龠]+屋さん[^。！？\n]{0,15})', kasumi_text)
print("Total 屋さん matches:", len(yasan_matches))
for m in sorted(list(set(yasan_matches))):
    print(" ", m.strip())

