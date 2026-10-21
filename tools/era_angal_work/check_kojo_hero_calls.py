import os
import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Checking hero callings in existing KOJO COM files ===")
for cid in range(1, 73):
    files = glob.glob(f"ERB/CHAR/CHAR_{cid:02d}_*_COM.ERB") + glob.glob(f"ERB/CHAR/CHAR_{cid}_*_COM.ERB")
    if not files:
        continue
    fpath = files[0]
    calls = []
    with open(fpath, 'r', encoding='cp932', errors='ignore') as f:
        text = f.read()
        dialogue_lines = re.findall(r'PRINTFORMW?\s+「([^」]+)」', text)
        for d in dialogue_lines:
            found = re.findall(r'(転校生[くん|さん|ちゃん|しゃん|殿|様]*|プロデューサー[さん|様]*|お兄ちゃん先輩|お兄ちゃん|おにーさん|おに～さん|せんぱい|先輩|ダーリン|ヘルプマン|少年|キミ|あんた|お前)', d)
            calls.extend(found)
    from collections import Counter
    top_calls = Counter(calls).most_common(3)
    call_str = ", ".join([f"{k}:{v}" for k, v in top_calls])
    print(f"[{cid:02d}] {os.path.basename(fpath)[:20]:20s} : {call_str}")
