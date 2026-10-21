import re

with open('tools/output/みなづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Check what Minaduki calls Miduki directly in dialogue
quotes = re.findall(r'「([^」]+)」', text)
for q in quotes:
    if any(k in q for k in ['みづき', 'お姉', '姉']):
        print("Minaduki direct quote:", q)

