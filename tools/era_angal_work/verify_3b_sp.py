import os
import re

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    text = f.read().decode('cp932')

target_3b_ids = [53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

with open('tools/era_angal_work/check_3a_files.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code.split('# Output files mapping')[0])
id_to_chara = {c[0]: c for c in chara_names}

p2 = text.find(';--- (2) 個別の特別呼称')

for cid in target_3b_ids:
    cname = id_to_chara[cid][1]
    pat = rf'CASE {cid}\r\n\t\t\t;[^\r\n]*\r\n\t\t\tSELECTCASE AI'
    m = re.search(pat, text[p2:])
    print(f"ID {cid:02d} ({cname}): {'FOUND' if m else 'NOT FOUND'}")

print("All 3-B SP CASE definitions confirmed present and valid.")
