import os
import re

# Read all files for Kasumi
files = [f for f in os.listdir('tools/output') if 'かすみ' in f or '御影' in f]
kasumi_text = ""
for f in files:
    with open(os.path.join('tools/output', f), 'r', encoding='utf-8', errors='replace') as fp:
        kasumi_text += fp.read() + "\n"

print("Files:", files)
print("Text length:", len(kasumi_text))

# Find all lines starting with [ or quotes 「
lines = kasumi_text.splitlines()
all_vocatives = []
for l in lines:
    l_str = l.strip()
    # Check if dialogue
    if '「' in l_str or '[' in l_str:
        # Search patterns of address
        all_vocatives.append(l_str)

with open('tools/era_angal_work/kasumi_all_dialogue.txt', 'w', encoding='utf-8') as out:
    for l in all_vocatives:
        out.write(l + "\n")

print(f"Saved {len(all_vocatives)} dialogue lines.")
