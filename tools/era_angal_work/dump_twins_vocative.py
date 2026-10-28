import re

with open('tools/output/みなづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text_mina = f.read()
with open('tools/output/みづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text_midu = f.read()

quotes_mina = re.findall(r'「([^」]+)」', text_mina)
quotes_midu = re.findall(r'「([^」]+)」', text_midu)

out = []
out.append("=== みづきがみなづきに呼びかけるセリフ ===")
for q in quotes_midu:
    if any(k in q for k in ['みな', '妹', 'みなづき']):
        out.append("  みづき: 「" + q + "」")

out.append("\n=== みなづきがみづきに呼びかけるセリフ ===")
for q in quotes_mina:
    if any(k in q for k in ['みづき', '姉', 'お姉', 'みづ']):
        out.append("  みなづき: 「" + q + "」")

with open('tools/era_angal_work/twins_vocative.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Saved twins vocative analysis.")
