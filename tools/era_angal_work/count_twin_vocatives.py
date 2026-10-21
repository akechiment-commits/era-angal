import re

with open('tools/output/みなづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text_mina = f.read()
with open('tools/output/みづき.txt', 'r', encoding='utf-8', errors='replace') as f:
    text_midu = f.read()

print("=== みづき（姉）がみなづき（妹）を呼ぶ語 ===")
print("みなちゃん:", len(re.findall(r'みなちゃん', text_midu)))
print("みなづき:", len(re.findall(r'みなづき', text_midu)))
print("みな:", len(re.findall(r'みな(?![づな])', text_midu)))
print("妹:", len(re.findall(r'妹', text_midu)))

print("\n=== みなづき（妹）がみづき（姉）を呼ぶ語 ===")
print("みづきちゃん:", len(re.findall(r'みづきちゃん', text_mina)))
print("お姉ちゃん:", len(re.findall(r'お姉ちゃん', text_mina)))
print("お姉さん:", len(re.findall(r'お姉さん', text_mina)))
print("姉さん:", len(re.findall(r'姉さん', text_mina)))
print("みづき:", len(re.findall(r'みづき', text_mina)))

# Sample quotes of みなづき calling みづき directly
direct_calls = []
for q in re.findall(r'「([^」]+)」', text_mina):
    for w in ['みづきちゃん', 'お姉ちゃん', 'みづき']:
        if w in q:
            direct_calls.append((w, q))

print(f"\nDirect call quotes samples (total {len(direct_calls)}):")
for w, q in direct_calls[:15]:
    print(f"[{w}] {q}")

