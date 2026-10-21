with open('tools/output/みづき・みなづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

lines = text.splitlines()
with open('tools/era_angal_work/combo_out_utf8.txt', 'w', encoding='utf-8') as f:
    for l in lines[:100]:
        f.write(l + "\n")

print("Saved combo_out_utf8.txt")
