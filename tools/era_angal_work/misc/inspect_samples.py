import os, glob, re, sys

def inspect_char(ch_id):
    csv_file = (glob.glob(f'CSV/Chara{ch_id}_*.csv') + glob.glob(f'CSV/Chara{ch_id:02d}_*.csv'))[0]
    com_file = (glob.glob(f'ERB/CHAR/CHAR_{ch_id:02d}_*_COM.ERB') + glob.glob(f'ERB/CHAR/CHAR_{ch_id}_*_COM.ERB'))[0]
    
    cstr = {}
    with open(csv_file, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            m = re.match(r'^\s*CSTR\s*,\s*(8[0-4])\s*,\s*(.*)$', line)
            if m:
                cstr[int(m.group(1)) - 80] = m.group(2).strip()
                
    with open(com_file, 'r', encoding='cp932', errors='ignore') as f:
        com_text = f.read()
        
    print(f'================ Chara {ch_id}: {os.path.basename(csv_file)} ================')
    print('CSV Names:')
    for i in range(5):
        print(f'  CSTR:{80+i} = {cstr.get(i)}')
        
    print('\nDialogues (SELECTCOM == 280-284):')
    for i in range(5):
        com_num = 280 + i
        m = re.search(rf'(;[^\n]*\bCOM{com_num}\b[^\n]*\n)?\s*IF SELECTCOM == {com_num}\b(.*?)(?=(ELSEIF SELECTCOM|ELSE\b|ENDIF\b))', com_text, re.DOTALL)
        header = m.group(1).strip() if (m and m.group(1)) else ''
        body = m.group(2).strip() if m else ''
        scene_m = re.search(r'場面:\s*([^\）\)\n\r]+)', body)
        scene = scene_m.group(1).strip() if scene_m else ''
        first_dlg = ''
        for line in body.split('\n'):
            if 'PRINTFORMW' in line or 'PRINTFORML' in line:
                first_dlg = line.strip()
                break
        print(f'  COM{com_num}: Header=\"{header}\" | Scene=\"{scene}\"')
        print(f'    Dlg: {first_dlg[:70]}')
        
    print('\nNarrations (@TRAIN_MESSAGE_B280-B284):')
    for i in range(5):
        com_num = 280 + i
        m = re.search(rf'@TRAIN_MESSAGE_B{com_num}_{ch_id}\b\s*\n(.*?)(?=@TRAIN_MESSAGE|\Z)', com_text, re.DOTALL)
        body = m.group(1).strip().replace('\n', ' ') if m else ''
        print(f'  B{com_num}_{ch_id}: {body[:80]}')
    print()

for c in [1, 2, 3, 4, 7, 8, 14, 15, 71]:
    inspect_char(c)
