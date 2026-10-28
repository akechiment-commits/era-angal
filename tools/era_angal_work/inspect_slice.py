with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    b = f.read()

import re
# check CASE 52 to CASE 65
p_c52 = b.find(b'\t\tCASE 52\r\n')
p_c52_endselect = b.find(b'\t\t\tENDSELECT\r\n', p_c52)
p_start_3b = p_c52_endselect + len(b'\t\t\tENDSELECT\r\n')

p_c65 = b.find(b'\t\tCASE 65\r\n', p_start_3b)
print('p_start_3b:', p_start_3b, 'p_c65:', p_c65)

slice_to_replace = b[p_start_3b:p_c65].decode('cp932')
print("Slice to replace:\n", slice_to_replace)

sel = len(re.findall(r'SELECTCASE', slice_to_replace))
esel = len(re.findall(r'ENDSELECT', slice_to_replace))
print(f"In old slice: SELECTCASE={sel}, ENDSELECT={esel}")
