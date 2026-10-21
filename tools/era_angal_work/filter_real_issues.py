# -*- coding: utf-8 -*-
with open('tools/era_angal_work/kojo_scan_initial_results.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
entries = re.findall(r'\s+-\s+\[(PUNCTUATION|VIEWPOINT_REVERSAL)\]\s+([^\n]+)\n\s+Text:\s+([^\n]+)', text)

with open('tools/era_angal_work/real_issues.txt', 'w', encoding='utf-8') as out:
    out.write(f"=== REAL ISSUES ({len(entries)}) ===\n\n")
    for t, info, line in entries:
        out.write(f"[{t}] {info}\n  Text: {line}\n\n")

print(f"Wrote {len(entries)} real issues to real_issues.txt")
