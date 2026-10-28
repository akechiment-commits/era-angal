# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict
from check_batch1_clean import check_batch

b2_issues = check_batch(13, 23)
total_b2 = sum(len(v) for v in b2_issues.values())
print(f"Batch 2 (CHAR 13-23) Total issues: {total_b2}")

with open('tools/era_angal_work/batch2_clean_report.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(b2_issues.keys()):
        out.write(f"### CHAR_{cid:02d} ({len(b2_issues[cid])} issues)\n")
        for iss in b2_issues[cid]:
            com_str = f"[COM{iss['com']}] " if iss['com'] else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_str}{iss['desc']}\n")
            out.write(f"      {iss['text']}\n")
        out.write("\n")

print("Wrote batch2_clean_report.txt successfully!")
