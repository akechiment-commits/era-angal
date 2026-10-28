# -*- coding: utf-8 -*-
import shutil

# バックアップ作成
shutil.copyfile('ERB/AITE_YOBI_相手呼称.ERB', 'ERB/AITE_YOBI_相手呼称.ERB.bak_before_31_32')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = [l.decode('cp932') for l in f.readlines()]

# 1. 第1階層の更新
# CASE 32, 37, 50 から 32 を分離
c32_found = False
for i, l in enumerate(lines[:140]):
    if l.startswith('\t\tCASE 32, 37, 50\r\n'):
        new_tier1_32 = [
            '\t\tCASE 32\r\n',
            '\t\t\t;安条まい: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「苗字+ちゃん」\r\n',
            '\t\t\tIF GET_CHARA_GRADE(AI) > 2\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%先輩"\r\n',
            '\t\t\tELSE\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%ちゃん"\r\n',
            '\t\t\tENDIF\r\n',
            '\t\tCASE 37, 50\r\n'
        ]
        lines[i:i+1] = new_tier1_32
        c32_found = True
        break
assert c32_found

# 2. 第2階層の更新（CASE 31 と CASE 32）
c31_idx = None
c34_idx = None

for i, l in enumerate(lines):
    if l == '\t\tCASE 31\r\n' and i > 500:
        c31_idx = i
    elif l == '\t\tCASE 34\r\n' and i > 500:
        c34_idx = i
        break

print(f"c31_idx: {c31_idx}, c34_idx: {c34_idx}")
assert c31_idx is not None and c34_idx is not None
assert lines[c31_idx - 1].strip() == 'ENDSELECT'
assert lines[c34_idx - 1].strip() == 'ENDSELECT'

new_tier2 = [
    '\t\tCASE 31\r\n',
    '\t\t\t;夢路まりあ (2-B / 帰宅部・保健委員会)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 49\r\n',
    '\t\t\t\t\t;小松ぼたん (守護聖人)\r\n',
    '\t\t\t\t\tRESULTS \'= @"小松先輩"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長さま"\r\n',
    '\t\t\t\t;--- 同級生 (唯一無二の大親友・幼馴染み) ---\r\n',
    '\t\t\t\tCASE 35\r\n',
    '\t\t\t\t\t;梅園かな (幼馴染み)\r\n',
    '\t\t\t\t\tRESULTS \'= @"梅ちゃん"\r\n',
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 32\r\n',
    '\t\t\t;安条まい (2-B / 帰宅部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\tCASE 66\r\n',
    '\t\t\t\t\t;曽根セイラ\r\n',
    '\t\t\t\t\tRESULTS \'= @"セイラちゃん"\r\n',
    '\t\t\t\t;--- 同級生 ---\r\n',
    '\t\t\t\tCASE 37\r\n',
    '\t\t\t\t\t;龍泉寺レンレン\r\n',
    '\t\t\t\t\tRESULTS \'= @"レンレン"\r\n',
    '\t\t\t\tCASE 38\r\n',
    '\t\t\t\t\t;クー・カロア\r\n',
    '\t\t\t\t\tRESULTS \'= @"クー"\r\n',
    '\t\t\t\t;--- 下級生 (最重要の妹分・名前ちゃん付け) ---\r\n',
    '\t\t\t\tCASE 2\r\n',
    '\t\t\t\t\t;北川ゆき (妹分・「ねえさん」)\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆきちゃん"\r\n',
    '\t\t\tENDSELECT\r\n'
]

lines[c31_idx:c34_idx] = new_tier2

out_text = "".join(lines)
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(out_text.encode('cp932'))

print("Updated cases 31 and 32 successfully!")
