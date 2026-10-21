# -*- coding: utf-8 -*-
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = [l.decode('cp932') for l in f.readlines()]

print(f"Total lines: {len(lines)}")
print("Line 549 (0-indexed 548):", repr(lines[548])) # ENDSELECT of CASE 23
print("Line 550 (0-indexed 549):", repr(lines[549])) # \t\tCASE 24\r\n
print("Line 633 (0-indexed 632):", repr(lines[632])) # ENDSELECT of CASE 25
print("Line 634 (0-indexed 633):", repr(lines[633])) # \t\tCASE 27\r\n

assert lines[548].strip() == "ENDSELECT"
assert lines[549].strip() == "CASE 24"
assert lines[632].strip() == "ENDSELECT"
assert lines[633].strip() == "CASE 27"
print("Line checks passed!")
