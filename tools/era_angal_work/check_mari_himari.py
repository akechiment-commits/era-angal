import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Mari
with open('tools/output/まり.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== 花丘まり (tools/output/まり.txt) ===")
for c in ['私', 'わたし', 'あたし', 'わたくし', 'うち', 'ウチ', '自分', 'まり']:
    p = rf'(?:^|[「『（(\s、。！？!?])({re.escape(c)})(?:[はがものにをって]|自身|たち|ら)'
    m = re.findall(p, text)
    print(f"  {c}: {len(m)}")

# Samples
for s in re.findall(r'([^\n。！？!?]*?わたくし[^\n。！？!?]*)', text)[:3]:
    print("  わたくし sample:", s.strip())
for s in re.findall(r'([^\n。！？!?]*?わたし[^\n。！？!?]*)', text)[:3]:
    print("  わたし sample:", s.strip())

# Himari
with open('tools/output/ひまり.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("\n=== 鶴海ひまり (tools/output/ひまり.txt) ===")
for c in ['私', 'わたし', 'あたし', 'わたくし', 'うち', 'ウチ', '自分', 'ひまり']:
    p = rf'(?:^|[「『（(\s、。！？!?])({re.escape(c)})(?:[はがものにをって]|自身|たち|ら)'
    m = re.findall(p, text)
    print(f"  {c}: {len(m)}")

for s in re.findall(r'([^\n。！？!?]*?私[はがもの][^\n。！？!?]*)', text)[:3]:
    print("  私 sample:", s.strip())
