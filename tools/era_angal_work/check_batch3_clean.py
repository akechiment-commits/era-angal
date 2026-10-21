# -*- coding: utf-8 -*-
from check_batch1_clean import check_batch

b3_issues = check_batch(24, 34)
total_b3 = sum(len(v) for v in b3_issues.values())
print(f"Batch 3 (CHAR 24-34) Total issues: {total_b3}")

with open('tools/era_angal_work/batch3_clean_report.txt', 'w', encoding='utf-8') as out:
    for cid in sorted(b3_issues.keys()):
        out.write(f"### CHAR_{cid:02d} ({len(b3_issues[cid])} issues)\n")
        for iss in b3_issues[cid]:
            com_str = f"[COM{iss['com']}] " if iss['com'] else ""
            out.write(f"  - [{iss['type']}] {iss['file']}:{iss['line']} {com_str}{iss['desc']}\n")
            out.write(f"      {iss['text']}\n")
        out.write("\n")

print("Wrote batch3_clean_report.txt successfully!")
