import sys

def safe_print(text):
    print(text.encode('cp932', errors='replace').decode('cp932'))

cid = sys.argv[1] if len(sys.argv) > 1 else "53"
next_cid = str(int(cid) + 1)

with open('tools/era_angal_work/3b_analysis_deep.txt', 'r', encoding='utf-8') as f:
    text = f.read()

header = f"【ID {int(cid):02d} :"
parts = text.split(header)
if len(parts) > 1:
    content = parts[1]
    next_header = f"【ID {int(next_cid):02d} :"
    if next_header in content:
        content = content.split(next_header)[0]
    safe_print(header + content)
else:
    print(f"ID {cid} not found.")

