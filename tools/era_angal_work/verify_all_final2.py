# -*- coding: utf-8 -*-
import re

def main():
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        text = f.read()

    # Find speaker blocks in (2) individual section
    pos2 = text.find(';--- (2) 個別の特殊呼称（上書き）---')
    if pos2 == -1:
        # fallback: find second SELECTCASE SP
        parts = text.split('SELECTCASE SP')
        indiv_text = parts[2]
    else:
        indiv_text = text[pos2:]

    speaker_pattern = re.findall(r'(\t\tCASE (\d+)\s*\n\t\t\t;([^\n]+)\n\t\t\tSELECTCASE AI\n(.*?)\t\t\tENDSELECT)', indiv_text, re.DOTALL)

    print(f'Found {len(speaker_pattern)} speaker blocks in individual section!')

    case0_missing = []
    case72_tenkousei = []
    case72_values = {}

    for full_block, sp_id, chara_info, ai_block in speaker_pattern:
        sp_id = int(sp_id)
        # Check CASE 0
        m0 = re.search(r'CASE 0\s*\n\s*RESULTS \'= @"([^"]+)"', ai_block)
        if not m0:
            case0_missing.append((sp_id, chara_info.strip()))
        
        # Check CASE 72
        m72 = re.search(r'CASE 72\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_block)
        if m72:
            val = m72.group(1)
            case72_values[sp_id] = val
            if any(bad in val for bad in ['転校生', '少年', '君', '弟', 'きみ', 'おまえ']):
                case72_tenkousei.append((sp_id, chara_info.strip(), val))

    print(f'CASE 0 missing: {len(case0_missing)}')
    if case0_missing:
        print('Missing:', case0_missing)

    print(f'CASE 72 tenkousei contamination: {len(case72_tenkousei)}')
    if case72_tenkousei:
        print('Contaminated:', case72_tenkousei)

    print(f'All CASE 72 counts: {len(case72_values)}')

    # 3-B check specifically
    print('\n=== 3-B (53-63) verification in ERB ===')
    for sp_id in range(53, 64):
        for full_block, sid, cinfo, ai_block in speaker_pattern:
            if int(sid) == sp_id:
                m0 = re.search(r'CASE 0\s*\n\s*RESULTS \'= @"([^"]+)"', ai_block)
                m72 = re.search(r'CASE 72\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_block)
                val0 = m0.group(1) if m0 else 'MISSING'
                val72 = m72.group(1) if m72 else 'DEFAULT'
                print(f'CHAR_{sp_id} {cinfo.strip()[:20]}: CASE 0="{val0}", CASE 72="{val72}"')

if __name__ == '__main__':
    main()
