import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

chara_names = {}
with open('tools/era_angal_work/list_names.py', 'r', encoding='utf-8') as f:
    pass

# Load from list_names logic
import glob
for cid in range(1, 73):
    files = glob.glob(f'CSV/Chara{cid}_*.csv') + glob.glob(f'CSV/Chara0{cid}_*.csv')
    if files:
        with open(files[0], 'r', encoding='cp932', errors='ignore') as fp:
            for l in fp:
                if l.startswith('名前,'):
                    chara_names[cid] = l.strip().split(',')[1]
                    break

with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    text = f.read()

print("=== Checking 53 to 63 AI target mappings ===")
for sp in range(53, 64):
    m = re.search(rf'^\t\tCASE {sp}\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI([\s\S]*?)^\t\t\tENDSELECT', text, re.MULTILINE)
    if not m:
        continue
    sp_name = m.group(1).strip()
    body = m.group(2)
    # find all CASE X
    cases = re.findall(r'CASE\s+(\d+)\s*\r?\n(?:\t+;([^\r\n]*)\r?\n)?\t+RESULTS \'= @"([^"]+)"', body)
    print(f"\nSP {sp:02d}: {sp_name}")
    for ai_str, cmt, res in cases:
        ai = int(ai_str)
        if ai == 0:
            target_name = "主人公"
        else:
            target_name = chara_names.get(ai, f"UNKNOWN_{ai}")
        print(f"  AI {ai:02d} ({target_name:10s}): {res:12s} | コメント: {cmt}")
