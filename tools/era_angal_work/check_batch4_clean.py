# -*- coding: utf-8 -*-
from check_batch1_clean import check_batch

b4_issues = check_batch(35, 44)
total_b4 = sum(len(v) for v in b4_issues.values())
print(f"Batch 4 (CHAR 35-44) Total issues: {total_b4}")

with open('tools/era_angal_work/batch4_clean_report.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(b4_issues.keys()):
        out.write(f"### CHAR_{cid:02d} ({len(b4_issues[cid])} issues)\n")
        for iss in b4_issues[cid]:
            com_str = f"[COM{iss['com']}] " if iss['com'] else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_str}{iss['desc']}\n")
            out.write(f"      {iss['text']}\n")
        out.write("\n")

print("Wrote batch4_clean_report.txt successfully!")
