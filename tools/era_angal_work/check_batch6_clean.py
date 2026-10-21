# -*- coding: utf-8 -*-
from check_batch1_clean import check_batch

b6_issues = check_batch(58, 72)
total_b6 = sum(len(v) for v in b6_issues.values())
print(f"Batch 6 (CHAR 58-72) Total issues: {total_b6}")

with open('tools/era_angal_work/batch6_clean_report.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(b6_issues.keys()):
        out.write(f"### CHAR_{cid:02d} ({len(b6_issues[cid])} issues)\n")
        for iss in b6_issues[cid]:
            com_str = f"[COM{iss['com']}] " if iss['com'] else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_str}{iss['desc']}\n")
            out.write(f"      {iss['text']}\n")
        out.write("\n")

print("Wrote batch6_clean_report.txt successfully!")
