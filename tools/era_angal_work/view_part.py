import sys

def safe_print(text):
    print(text.encode('cp932', errors='replace').decode('cp932'))

cid = sys.argv[1] if len(sys.argv) > 1 else "46"

with open('tools/era_angal_work/3a_all_verified.txt', 'r', encoding='utf-8') as f:
    text = f.read()

header = f"=== ID {int(cid):02d}:"
parts = text.split(header)
if len(parts) > 1:
    content = parts[1].split('=== ID')[0]
    safe_print(f"=== ID {int(cid):02d}:" + content)
else:
    print(f"ID {cid} not found.")

