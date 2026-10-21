# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

print("==================== ななの「ましろ」への呼び方 ====================")
with open('tools/output/なな.txt', 'r', encoding='utf-8', errors='ignore') as f:
    nana_text = f.read()

for m in re.finditer(r'([^。\n]*ましろ[^。\n]*)', nana_text):
    print(m.group(1).strip()[:120])

print("\n==================== ななの「日滝」「部長」「団長」 ====================")
for m in re.finditer(r'([^。\n]*(?:日滝|団長|部長)[^。\n]*)', nana_text):
    print(m.group(1).strip()[:120])

print("\n==================== ゆうの「部長」「合唱」 ====================")
with open('tools/output/ゆう.txt', 'r', encoding='utf-8', errors='ignore') as f:
    yu_text = f.read()

for m in re.finditer(r'([^。\n]*(?:部長|合唱|深鳥|ふみ)[^。\n]*)', yu_text):
    print(m.group(1).strip()[:120])
