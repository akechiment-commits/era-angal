# -*- coding: utf-8 -*-
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    line_str = l.decode('cp932', errors='ignore').strip()
    if any(line_str.startswith(f"CASE {c}") for c in [24, 25, 26]):
        print(f"--- Line {i+1}: {line_str} ---")
        for j in range(i, min(i+40, len(lines))):
            print(f"{j+1}: {lines[j].decode('cp932', errors='ignore').rstrip()}")
