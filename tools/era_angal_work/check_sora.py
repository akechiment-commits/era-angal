# -*- coding: utf-8 -*-
import glob, re

# Check 時国そら dialogue for protagonist calls
with open('tools/output/そら.txt', 'r', encoding='utf-8', errors='ignore') as fp:
    text = fp.read()

calls = set()
for l in text.splitlines():
    for p in ['転校生', '先輩', 'あなた', 'プロデューサー', '君', 'キミ', 'お前']:
        m = re.findall(rf'({p}[^\s、。！？「」…―]*)', l)
        for x in m: calls.add(x)

with open('tools/era_angal_work/sora_calls.txt', 'w', encoding='utf-8') as out:
    for c in sorted(list(calls)):
        out.write(c + '\n')

print("Wrote sora_calls.txt")
