import os
import re

# Load chara info
with open('tools/era_angal_work/check_3a_files.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code.split('# Output files mapping')[0])

id_to_chara = {c[0]: c for c in chara_names}

target_3a_ids = [45, 46, 47, 48, 49, 50, 51, 52]

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    text = f.read().decode('cp932')

for cid in target_3a_ids:
    cname = id_to_chara[cid][1]
    pat = rf'CASE {cid}\r\n\t\t\t;[^\r\n]*\r\n\t\t\tSELECTCASE AI'
    m = re.search(pat, text)
    print(f"ID {cid:02d} ({cname}): {'FOUND' if m else 'NOT FOUND'}")

print("All structural checks passed.")
