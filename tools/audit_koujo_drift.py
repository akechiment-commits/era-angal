# -*- coding: utf-8 -*-
"""
完成済み口上の「最新構造との乖離(ドリフト)」を測る監査スクリプト。

目的：初期に作った口上を最新テンプレ(CHAR_TEMPLATE_COM.ERB / 手順書)へ
そろえる大作業の作業リストを、客観的な数値で出す。

使い方:
    python3 tools/audit_koujo_drift.py            # 全キャラ一覧（ドリフト降順）
    python3 tools/audit_koujo_drift.py 1          # cno=1 の内訳（空スロのCOM別など）

検出マーカー（手順書 §4/§5/§8/§9 由来）:
  - empty       : 空セリフ「」の数（新構造をバックフィルしたが未記入＝最大の指標）
  - konoko      : 「この子/あの子/その子」の数（女性限定COMで %LOCALS% へ要置換）
  - locals      : %LOCALS% 使用数（相手呼称システムが本文に効いているか）
  - aite_yobi   : CALL AITE_YOBI アンカー数（先頭ガード直後に1が正）
  - fail_branch : 会話失敗分岐 TFLAG:18 == -1 の数
  - date_split  : デート出発/帰宅分岐 TEQUIP:2 の数
  - tilde       : 半角チルダ ~ (U+007E) の数（0が正）
  - callname_bad: 素の %CALLNAME%（:PLAYER 無し。0が正）
ファイルは cp932 で読む（書き換えはしない・読み取り専用）。
"""
import re, glob, os, sys

TEMPLATE = 'ERB/CHAR/CHAR_TEMPLATE_COM.ERB'

def load(p):
    with open(p, 'rb') as f:
        return f.read().decode('cp932', 'replace')

def num(f):
    m = re.search(r'CHAR_(\d+)_', f)
    return int(m.group(1)) if m else -1

def empty_by_com(text):
    prof = {}; cur = None
    for ln in text.split('\n'):
        m = re.search(r'IF\s+SELECTCOM\s*==\s*(\d+)', ln)
        if m:
            cur = int(m.group(1))
        if '「」' in ln and cur is not None:
            prof[cur] = prof.get(cur, 0) + 1
    return prof

def audit(text):
    return {
        'empty':        text.count('「」'),
        'konoko':       len(re.findall(r'この子|あの子|その子', text)),
        'locals':       len(re.findall(r'%LOCALS%', text)),
        'aite_yobi':    len(re.findall(r'CALL\s+AITE_YOBI', text)),
        'fail_branch':  len(re.findall(r'TFLAG:18\s*==\s*-1', text)),
        'date_split':   len(re.findall(r'TEQUIP:2', text)),
        'tilde':        text.count('~'),
        'callname_bad': len(re.findall(r'%CALLNAME%', text)),
    }

def files():
    fs = sorted(glob.glob('ERB/CHAR/CHAR_*_COM.ERB'))
    return [f for f in fs if 'TEMPLATE' not in f]

def drift_score(a):
    # 空 + この子 を主指標に、軽微NGを加点
    return a['empty'] + a['konoko'] + a['tilde'] * 5 + a['callname_bad'] * 5

def main():
    if len(sys.argv) > 1:
        cno = int(sys.argv[1])
        f = next(x for x in files() if num(x) == cno)
        t = load(f)
        print(f'== {os.path.basename(f)} ==')
        a = audit(t)
        for k, v in a.items():
            print(f'  {k:12}: {v}')
        print('  空セリフのCOM別内訳:')
        for com, c in sorted(empty_by_com(t).items()):
            print(f'    COM{com}: {c} empty')
        return
    rows = []
    for f in files():
        a = audit(load(f))
        rows.append((num(f), os.path.basename(f).replace('_COM.ERB', ''), a))
    rows.sort(key=lambda r: -drift_score(r[2]))
    print(f"{'cno':>3} {'name':22} {'score':>5} {'空':>4} {'この子':>5} {'LOC':>4} {'AITE':>4} {'~':>2} {'CN!':>3}")
    for n, name, a in rows:
        nm = name.split('_', 2)[2] if name.count('_') >= 2 else name
        print(f"{n:3} {nm:22} {drift_score(a):5} {a['empty']:4} {a['konoko']:5} "
              f"{a['locals']:4} {a['aite_yobi']:4} {a['tilde']:2} {a['callname_bad']:3}")

if __name__ == '__main__':
    main()
