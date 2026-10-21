import os
import re

erb_path = 'ERB/AITE_YOBI_相手呼称.ERB'

with open(erb_path, 'rb') as f:
    raw_content = f.read()

text = raw_content.decode('cp932')

# 1. Update Layer 1
# Locate CASE 46
p_case46 = text.find('\t\tCASE 46\r\n')
# Locate CASE 50 in Layer 1
p_case50 = text.find('\t\tCASE 50\r\n')

# Let's verify layer 1 text around CASE 46 and CASE 50
print("--- Old Layer 1 snippets ---")
print(repr(text[p_case46:p_case46+100]))
print(repr(text[p_case50:p_case50+100]))

# Also check 25, 28, 45, 47, 48, 49, 52...
p_case_sans = text.find('\t\tCASE 25, 28, 45,')
print(repr(text[p_case_sans:p_case_sans+150]))

# Also check CASE 51
p_case51 = text.find('\t\tCASE 51\r\n')
print(repr(text[p_case51:p_case51+100]))

