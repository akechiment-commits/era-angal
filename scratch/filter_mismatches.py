# -*- coding: utf-8 -*-
import re

# Specific known cross-variant mismatches:
# ABL:
#   マゾっ気: era-angal is 8. If code uses 21, 22, etc.
#   サドっ気: era-angal is 15. If code uses 20, etc.
#   奉仕精神: era-angal is 6. If code uses 13, 16, 7, etc. (wait, is 7 露出癖?)
#   露出癖: era-angal is 7. If code uses 8, 14, 17, etc.
# TALENT:
#   服従: era-angal is 180. If code uses 160, etc.
#   恋慕: era-angal is 85. If code uses 85.
#   親愛: era-angal is 88. If code uses 88.
#   淫乱: era-angal is 76. If code uses 76.

with open('scratch_mismatches.txt', 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.split('\n\n')
print(f"Total entries: {len(entries)}")

high_confidence = []
for e in entries:
    lines = e.strip().split('\n')
    if len(lines) < 3: continue
    header = lines[0]
    comment = lines[1]
    code = lines[2]
    
    # Check for direct: ;マゾっ気 or ;服従
    if 'マゾ' in comment and ('ABL' in header and 'used 21' in header or 'used 20' in header):
        high_confidence.append(e)
    elif 'サド' in comment and ('ABL' in header and 'used 20' in header):
        high_confidence.append(e)
    elif '服従' in comment and ('TALENT' in header and 'used 160' in header):
        high_confidence.append(e)
    elif '淫乱' in comment and ('TALENT' in header and ('used 4' in header or 'used 74' in header)):
        high_confidence.append(e)

print(f"High confidence mismatches: {len(high_confidence)}")
with open('scratch_high_mismatches.txt', 'w', encoding='utf-8') as out:
    for item in high_confidence:
        out.write(item + '\n\n')
