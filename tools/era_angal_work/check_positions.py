import os
import re

erb_path = 'ERB/AITE_YOBI_相手呼称.ERB'

with open(erb_path, 'rb') as f:
    raw_content = f.read()

text = raw_content.decode('cp932')

p1_start = text.find(';--- (1)')
p1_end = text.find(';--- (2)')

print("p1_start:", p1_start, "p1_end:", p1_end)

# Find CASE 45 in Layer 2
c45_start = text.find('\t\tCASE 45\r\n', p1_end)
if c45_start == -1:
    c45_start = text.find('\t\tCASE 45\n', p1_end)

c54_start = text.find('\t\tCASE 54\r\n', c45_start)
if c54_start == -1:
    c54_start = text.find('\t\tCASE 54\n', c45_start)

# Check if CASE 53 is there or CASE 54
c53_start = text.find('CASE 53', c45_start)
print("c45_start:", c45_start)
print("c53_start:", c53_start)
print("c54_start:", c54_start)
print("Snippet from c45_start:\n", text[c45_start:c45_start+300])
