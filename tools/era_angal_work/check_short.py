# -*- coding: utf-8 -*-
with open('tools/era_angal_work/audit_full_inventory.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
entries = re.findall(r'\[VERIFIED\s*\]\s+CHAR_(\d+)\s+(.*?)\s+->\s+AI_(\d+)\s+(.*?):\s+"([^"]+)"\s+\(count=(\d+)\)', text)
short_entries = [e for e in entries if len(e[4]) <= 2 and '%' not in e[4]]

with open('tools/era_angal_work/short_verified_calls.txt', 'w', encoding='utf-8') as out:
    out.write(f'Short verified calls (<= 2 chars): {len(short_entries)}\n\n')
    for e in short_entries:
        out.write(f'CHAR_{e[0]} {e[1]} -> AI_{e[2]} {e[3]}: "{e[4]}" (count={e[5]})\n')

print(f'Short verified calls: {len(short_entries)}')
