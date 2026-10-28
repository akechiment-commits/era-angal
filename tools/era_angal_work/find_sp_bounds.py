with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    b = f.read()

import re

# Find all SP CASE positions (multiline: ^\t\tCASE <num>\r\n\t\t\t;)
matches = list(re.finditer(rb'^\t\tCASE (\d+)\r\n\t\t\t;', b, re.MULTILINE))
for m in matches:
    cid = int(m.group(1))
    if cid >= 50:
        print(f"SP CASE {cid}: start={m.start()}")

# Find CASE 52's endselect
for m in matches:
    if int(m.group(1)) == 52 and m.start() > 20000:
        p_c52_start = m.start()
        p_c52_endselect = b.find(b'\t\t\tENDSELECT\r\n', p_c52_start)
        p_c52_end = p_c52_endselect + len(b'\t\t\tENDSELECT\r\n')
        print(f"SP CASE 52 start={p_c52_start}, end={p_c52_end}")

# Find next SP case after 52
for m in matches:
    if int(m.group(1)) > 63 and m.start() > 30000:
        print(f"Next SP CASE {int(m.group(1))} start={m.start()}")
        break
