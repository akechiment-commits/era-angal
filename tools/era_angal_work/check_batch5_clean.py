# -*- coding: utf-8 -*-
from check_batch1_clean import check_batch

b5_issues = check_batch(45, 57)
total_b5 = sum(len(v) for v in b5_issues.values())
print(f"Batch 5 (CHAR 45-57) Total issues: {total_b5}")

with open('tools/era_angal_work/batch5_clean_report.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(b5_issues.keys()):
        out.write(f"### CHAR_{cid:02d} ({len(b5_issues[cid])} issues)\n")
        for iss in b5_issues[cid]:
            com_str = f"[COM{iss['com']}] " if iss['com'] else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_str}{iss['desc']}\n")
            out.write(f"      {iss['text']}\n")
        out.write("\n")

print("Wrote batch5_clean_report.txt successfully!")
