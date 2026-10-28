# -*- coding: utf-8 -*-
import shutil

# バックアップ作成
shutil.copyfile('ERB/AITE_YOBI_相手呼称.ERB', 'ERB/AITE_YOBI_相手呼称.ERB.bak_before_33_34')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = [l.decode('cp932') for l in f.readlines()]

# 1. 第1階層の更新
# CASE 33, 46 -> CASE 46
c46_found = False
for i, l in enumerate(lines[:80]):
    if l.startswith('\t\tCASE 33, 46\r\n'):
        lines[i] = '\t\tCASE 46\r\n'
        c46_found = True
        break
assert c46_found

# CASE 26 -> CASE 26, 33
c26_found = False
for i, l in enumerate(lines[:80]):
    if l.startswith('\t\tCASE 26\r\n'):
        lines[i] = '\t\tCASE 26, 33\r\n'
        lines[i+1] = '\t\t\t;堀田さあや/柊るな: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「苗字呼び捨て」\r\n'
        c26_found = True
        break
assert c26_found

# CASE 29 -> CASE 29, 34
c29_found = False
for i, l in enumerate(lines[:100]):
    if l.startswith('\t\tCASE 29\r\n'):
        lines[i] = '\t\tCASE 29, 34\r\n'
        lines[i+1] = '\t\t\t;春風なな/桐島かいり: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「名前+ちゃん」\r\n'
        c29_found = True
        break
assert c29_found

# 2. 第2階層の更新（CASE 33 を新設し、CASE 34 を更新）
c34_idx = None
c35_idx = None

for i, l in enumerate(lines):
    if l == '\t\tCASE 34\r\n' and i > 500:
        c34_idx = i
    elif l == '\t\tCASE 35\r\n' and i > 500:
        c35_idx = i
        break

print(f"c34_idx: {c34_idx}, c35_idx: {c35_idx}")
assert c34_idx is not None and c35_idx is not None
assert lines[c34_idx - 1].strip() == 'ENDSELECT'
assert lines[c35_idx - 1].strip() == 'ENDSELECT'

new_tier2 = [
    '\t\tCASE 33\r\n',
    '\t\t\t;柊るな (2-B / ラクロス部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 45\r\n',
    '\t\t\t\t\t;円城寺れいか\r\n',
    '\t\t\t\t\tRESULTS \'= @"円城寺のお嬢"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"会長はん"\r\n',
    '\t\t\t\t;--- 同級生 (苗字呼び捨てからちゃん付けへ) ---\r\n',
    '\t\t\t\tCASE 26\r\n',
    '\t\t\t\t\t;堀田さあや\r\n',
    '\t\t\t\t\tRESULTS \'= @"堀田ちゃん"\r\n',
    '\t\t\t\t;--- 下級生 (苗字呼び捨てからちゃん付けへ) ---\r\n',
    '\t\t\t\tCASE 6\r\n',
    '\t\t\t\t\t;藍乃あいか (夏祭りの手伝い)\r\n',
    '\t\t\t\t\tRESULTS \'= @"あいかちゃん"\r\n',
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 34\r\n',
    '\t\t\t;桐島かいり (2-B / 合唱部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 52\r\n',
    '\t\t\t\t\t;湖南やこ (合唱部の恩人)\r\n',
    '\t\t\t\t\tRESULTS \'= @"湖南先輩"\r\n',
    '\t\t\t\tCASE 60\r\n',
    '\t\t\t\t\t;瀬川かえで (幼馴染み・メリメロ仲間)\r\n',
    '\t\t\t\t\tRESULTS \'= @"かえでちゃん"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\t;--- 同級生 (第1階層の「〜ちゃん」から距離のある「〜さん」へ) ---\r\n',
    '\t\t\t\tCASE 24\r\n',
    '\t\t\t\t\t;三波なつみ\r\n',
    '\t\t\t\t\tRESULTS \'= @"三波さん"\r\n',
    '\t\t\t\tCASE 26\r\n',
    '\t\t\t\t\t;堀田さあや\r\n',
    '\t\t\t\t\tRESULTS \'= @"堀田さん"\r\n',
    '\t\t\t\t;--- 下級生 ---\r\n',
    '\t\t\t\tCASE 8\r\n',
    '\t\t\t\t\t;丸子みさき (幼馴染み・最重要愛称)\r\n',
    '\t\t\t\t\tRESULTS \'= @"マルちゃん"\r\n',
    '\t\t\t\tCASE 3\r\n',
    '\t\t\t\t\t;小野ちよ (第1階層の「〜ちゃん」から距離のある「〜さん」へ)\r\n',
    '\t\t\t\t\tRESULTS \'= @"小野さん"\r\n',
    '\t\t\t\tCASE 17\r\n',
    '\t\t\t\t\t;小鳩あずさ (第1階層の「〜ちゃん」から距離のある「〜さん」へ)\r\n',
    '\t\t\t\t\tRESULTS \'= @"小鳩さん"\r\n',
    '\t\t\tENDSELECT\r\n'
]

lines[c34_idx:c35_idx] = new_tier2

out_text = "".join(lines)
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(out_text.encode('cp932'))

print("Updated cases 33 and 34 successfully!")
