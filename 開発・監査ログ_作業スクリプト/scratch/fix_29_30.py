# -*- coding: utf-8 -*-
import shutil

shutil.copyfile('ERB/AITE_YOBI_相手呼称.ERB', 'ERB/AITE_YOBI_相手呼称.ERB.bak_before_fix_29_30')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = [l.decode('cp932') for l in f.readlines()]

# CASE 29 と CASE 30 の範囲を特定
c29_idx = None
c30_idx = None
c31_idx = None

for i, l in enumerate(lines):
    if l == '\t\tCASE 29\r\n' and i > 500:
        c29_idx = i
    elif l == '\t\tCASE 30\r\n' and i > 500:
        c30_idx = i
    elif l == '\t\tCASE 31\r\n' and i > 500:
        c31_idx = i
        break

print(f"c29_idx: {c29_idx}, c30_idx: {c30_idx}, c31_idx: {c31_idx}")
assert c29_idx is not None and c30_idx is not None and c31_idx is not None

# CASE 29 の新ブロック
new_case29 = [
    '\t\tCASE 29\r\n',
    '\t\t\t;春風なな (2-A / チアリーディング部 副部長)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長さん"\r\n',
    '\t\t\t\tCASE 67\r\n',
    '\t\t\t\t\t;日滝ましろ (チア部部長・団長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"団長"\r\n',
    '\t\t\t\t;--- 同級生 (第1階層の「〜ちゃん」から距離のある「〜さん」へ) ---\r\n',
    '\t\t\t\tCASE 27\r\n',
    '\t\t\t\t\t;夏野ゆり\r\n',
    '\t\t\t\t\tRESULTS \'= @"夏野さん"\r\n',
    '\t\t\t\tCASE 35\r\n',
    '\t\t\t\t\t;梅園かな\r\n',
    '\t\t\t\t\tRESULTS \'= @"梅園さん"\r\n',
    '\t\t\t\tCASE 41\r\n',
    '\t\t\t\t\t;悠木ともこ\r\n',
    '\t\t\t\t\tRESULTS \'= @"悠木さん"\r\n',
    '\t\t\t\t;--- 下級生 (第1階層の「〜ちゃん」から距離のある「〜さん」へ) ---\r\n',
    '\t\t\t\tCASE 2\r\n',
    '\t\t\t\t\t;北川ゆき\r\n',
    '\t\t\t\t\tRESULTS \'= @"北川さん"\r\n',
    '\t\t\t\tCASE 8\r\n',
    '\t\t\t\t\t;丸子みさき\r\n',
    '\t\t\t\t\tRESULTS \'= @"丸子さん"\r\n',
    '\t\t\tENDSELECT\r\n'
]

# CASE 30 の新ブロック
new_case30 = [
    '\t\tCASE 30\r\n',
    '\t\t\t;長居ゆう (2-A / 合唱部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 52\r\n',
    '\t\t\t\t\t;湖南やこ (特別な先輩・「運命のひと」)\r\n',
    '\t\t\t\t\tRESULTS \'= @"湖南先輩"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\t;--- 同級生 ---\r\n',
    '\t\t\t\tCASE 34\r\n',
    '\t\t\t\t\t;桐島かいり (合唱部同級生)\r\n',
    '\t\t\t\t\tRESULTS \'= @"かいりちゃん"\r\n',
    '\t\t\t\tCASE 37\r\n',
    '\t\t\t\t\t;龍泉寺レンレン\r\n',
    '\t\t\t\t\tRESULTS \'= @"レンレンちゃん"\r\n',
    '\t\t\t\t;--- 下級生 ---\r\n',
    '\t\t\t\tCASE 8\r\n',
    '\t\t\t\t\t;丸子みさき (固有あだ名「マルちゃん」・からかい対象)\r\n',
    '\t\t\t\t\tRESULTS \'= @"マルちゃん"\r\n',
    '\t\t\t\tCASE 2\r\n',
    '\t\t\t\t\t;北川ゆき\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆきちゃん"\r\n',
    '\t\t\t\tCASE 11\r\n',
    '\t\t\t\t\t;氷野くるみ\r\n',
    '\t\t\t\t\tRESULTS \'= @"くるみちゃん"\r\n',
    '\t\t\t\tCASE 13\r\n',
    '\t\t\t\t\t;羽森つばさ (合唱部後輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"つばさちゃん"\r\n',
    '\t\t\t\tCASE 14\r\n',
    '\t\t\t\t\t;花音ことり\r\n',
    '\t\t\t\t\tRESULTS \'= @"ことりちゃん"\r\n',
    '\t\t\tENDSELECT\r\n'
]

lines[c29_idx:c31_idx] = new_case29 + new_case30

out_text = "".join(lines)
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(out_text.encode('cp932'))

print("Fixed CASE 29 and CASE 30 successfully!")
