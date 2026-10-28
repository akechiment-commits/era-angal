# -*- coding: utf-8 -*-
with open('ERB/COMF/COMF302.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_present_ring.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines, 1):
        if 'エンゲージリング' in line or '指輪' in line or '85' in line or 'リング' in line:
            start = max(0, i - 10)
            end = min(len(lines), i + 25)
            out.write(f"\n--- MATCH AT LINE {i} ---\n")
            for j in range(start, end):
                out.write(f"{j+1}: {lines[j]}")
            break
