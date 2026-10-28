# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

def audit_calls(cname):
    print(f"==================== {cname} 全呼称監査 ====================")
    with open(f'tools/output/{cname}.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # 相手を直接呼んでいるセリフ（「〜先輩」「〜さん」「〜ちゃん」「〜部長」「〜団長」「〜先生」「〜くん」）
    pats = [
        r'([^\s「」]*(?:先輩|さん|ちゃん|部長|団長|先生|くん|君|どの|殿)[^\s「」]*)'
    ]
    
    calls = []
    for l in lines:
        for p in pats:
            for m in re.finditer(p, l):
                calls.append((m.group(1), l.strip()))
    
    # キャラ名・苗字が含まれるもの
    print(f"Total call candidates: {len(calls)}")
    from collections import Counter
    c = Counter([x[0] for x in calls])
    for term, count in c.most_common(50):
        print(f"  {term}: {count}回")

audit_calls('なな')
audit_calls('ゆう')
audit_calls('ゆり')
audit_calls('こよい')
