import re

with open('tools/output/みなづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Lines where Minaduki addresses Miduki directly
lines = text.splitlines()
direct_calls = []
for l in lines:
    # Look for calls to Miduki
    if 'みづき' in l or 'お姉' in l:
        direct_calls.append(l.strip())

with open('tools/era_angal_work/minaduki_to_miduki_direct.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(direct_calls))

print(f"Saved {len(direct_calls)} lines.")
