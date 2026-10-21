import sys

# Safe print to cp932 console
def safe_print(text):
    print(text.encode('cp932', errors='replace').decode('cp932'))

cid = sys.argv[1] if len(sys.argv) > 1 else "45"
next_cid = str(int(cid) + 1)

with open('tools/era_angal_work/3a_analysis_detailed.txt', 'r', encoding='utf-8') as f:
    text = f.read()

part = text.split(f'【ID {int(cid):02d}')[1]
if f'【ID {int(next_cid):02d}' in part:
    part = part.split(f'【ID {int(next_cid):02d}')[0]

safe_print(part)
