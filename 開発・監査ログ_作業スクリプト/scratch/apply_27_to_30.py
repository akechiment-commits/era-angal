# -*- coding: utf-8 -*-
import shutil

# バックアップ作成
shutil.copyfile('ERB/AITE_YOBI_相手呼称.ERB', 'ERB/AITE_YOBI_相手呼称.ERB.bak_before_27_30')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = [l.decode('cp932') for l in f.readlines()]

# 1. 第1階層の更新
# CASE 26 の後ろに 27, 29, 30 を追加
c26_found = False
for i, l in enumerate(lines[:120]):
    if l.startswith('\t\tCASE 26\r\n'):
        # CASE 26 のブロックの終わり（ENDIFの行）を探す
        endif_idx = None
        for j in range(i, i+15):
            if lines[j].strip() == 'ENDIF':
                endif_idx = j
                break
        assert endif_idx is not None
        new_tier1_add = [
            '\t\tCASE 27\r\n',
            '\t\t\t;夏野ゆり: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「苗字+さん」\r\n',
            '\t\t\tIF GET_CHARA_GRADE(AI) > 2\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%先輩"\r\n',
            '\t\t\tELSE\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%さん"\r\n',
            '\t\t\tENDIF\r\n',
            '\t\tCASE 29\r\n',
            '\t\t\t;春風なな: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「名前+ちゃん」\r\n',
            '\t\t\tIF GET_CHARA_GRADE(AI) > 2\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%先輩"\r\n',
            '\t\t\tELSE\r\n',
            '\t\t\t\tRESULTS \'= @"%CALLNAME:AI%ちゃん"\r\n',
            '\t\t\tENDIF\r\n',
            '\t\tCASE 30\r\n',
            '\t\t\t;長居ゆう: 上級生(3年)は「苗字+先輩」、同級生(2年)は「名前+ちゃん」、下級生(1年)は「苗字+さん」\r\n',
            '\t\t\tIF GET_CHARA_GRADE(AI) > 2\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%先輩"\r\n',
            '\t\t\tELSEIF GET_CHARA_GRADE(AI) == 2\r\n',
            '\t\t\t\tRESULTS \'= @"%CALLNAME:AI%ちゃん"\r\n',
            '\t\t\tELSE\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%さん"\r\n',
            '\t\t\tENDIF\r\n'
        ]
        lines[endif_idx+1:endif_idx+1] = new_tier1_add
        c26_found = True
        break
assert c26_found

# CASE 25, 35, ... に 28 を追加
c25_group_found = False
for i, l in enumerate(lines[:140]):
    if l.startswith('\t\tCASE 25, 35, 43, 44'):
        lines[i] = '\t\tCASE 25, 28, 35, 43, 44, 45, 47, 48, 49, 52, 54, 55, 57, 60, 62, 65, 67, 68, 69\r\n'
        c25_group_found = True
        break
assert c25_group_found

# 2. 第2階層の更新（CASE 27〜30）
c27_idx = None
c31_idx = None
for i, l in enumerate(lines):
    if l == '\t\tCASE 27\r\n' and i > 500:
        c27_idx = i
    if l == '\t\tCASE 31\r\n' and i > 500:
        c31_idx = i
        break

print(f"c27_idx: {c27_idx}, c31_idx: {c31_idx}")
assert c27_idx is not None and c31_idx is not None
assert lines[c27_idx - 1].strip() == 'ENDSELECT'
assert lines[c31_idx - 1].strip() == 'ENDSELECT'

new_tier2 = [
    '\t\tCASE 27\r\n',
    '\t\t\t;夏野ゆり (2-A / 吹奏楽部・美化委員会)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\tCASE 72\r\n',
    '\t\t\t\t\t;あんず\r\n',
    '\t\t\t\t\tRESULTS \'= @"あんずさん"\r\n',
    '\t\t\t\t;--- 同級生 ---\r\n',
    '\t\t\t\tCASE 24\r\n',
    '\t\t\t\t\t;三波なつみ\r\n',
    '\t\t\t\t\tRESULTS \'= @"なつみちゃん"\r\n',
    '\t\t\t\tCASE 25\r\n',
    '\t\t\t\t\t;八朔つゆり (大親友)\r\n',
    '\t\t\t\t\tRESULTS \'= @"つゆりちゃん"\r\n',
    '\t\t\t\tCASE 26\r\n',
    '\t\t\t\t\t;堀田さあや\r\n',
    '\t\t\t\t\tRESULTS \'= @"さあやちゃん"\r\n',
    '\t\t\t\tCASE 29\r\n',
    '\t\t\t\t\t;春風なな\r\n',
    '\t\t\t\t\tRESULTS \'= @"ななちゃん"\r\n',
    '\t\t\t\tCASE 30\r\n',
    '\t\t\t\t\t;長居ゆう\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆうちゃん"\r\n',
    '\t\t\t\t;--- 下級生 (吹奏楽部後輩への呼び捨て) ---\r\n',
    '\t\t\t\tCASE 1\r\n',
    '\t\t\t\t\t;三善かなえ (吹奏楽部後輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"三善"\r\n',
    '\t\t\t\tCASE 4\r\n',
    '\t\t\t\t\t;早川きこ (吹奏楽部後輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"早川"\r\n',
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 28\r\n',
    '\t\t\t;星海こよい (2-A / 天文部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 58\r\n',
    '\t\t\t\t\t;天宮るり (天文部部長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"るりちゃん部長"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長さん"\r\n',
    '\t\t\t\tCASE 70\r\n',
    '\t\t\t\t\t;神無月ほとり (天文部副部長・親愛の愛称)\r\n',
    '\t\t\t\t\tRESULTS \'= @"月ちゃん先輩"\r\n',
    '\t\t\t\t;--- 同級生 ---\r\n',
    '\t\t\t\tCASE 25\r\n',
    '\t\t\t\t\t;八朔つゆり (従姉妹)\r\n',
    '\t\t\t\t\tRESULTS \'= @"つゆりちゃん"\r\n',
    '\t\t\t\tCASE 38\r\n',
    '\t\t\t\t\t;クー・カロア\r\n',
    '\t\t\t\t\tRESULTS \'= @"クーさん"\r\n',
    '\t\t\t\t;--- 下級生 ---\r\n',
    '\t\t\t\tCASE 10\r\n',
    '\t\t\t\t\t;木之下ゆゆ\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆゆちゃん"\r\n',
    '\t\t\t\tCASE 11\r\n',
    '\t\t\t\t\t;氷野くるみ\r\n',
    '\t\t\t\t\tRESULTS \'= @"くるみちゃん"\r\n',
    '\t\t\t\tCASE 20\r\n',
    '\t\t\t\t\t;藤猪しずく\r\n',
    '\t\t\t\t\tRESULTS \'= @"しずくちゃん"\r\n',
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 29\r\n',
    '\t\t\t;春風なな (2-A / チアリーディング部 副部長)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長さん"\r\n',
    '\t\t\t\tCASE 67\r\n',
    '\t\t\t\t\t;日滝ましろ (チア部部長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"ましろさん"\r\n',
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
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 30\r\n',
    '\t\t\t;長居ゆう (2-A / 合唱部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\tCASE 68\r\n',
    '\t\t\t\t\t;深鳥ふみ (合唱部部長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"部長さん"\r\n',
    '\t\t\t\t;--- 同級生 ---\r\n',
    '\t\t\t\tCASE 34\r\n',
    '\t\t\t\t\t;桐島かいり (合唱部同級生)\r\n',
    '\t\t\t\t\tRESULTS \'= @"かいりちゃん"\r\n',
    '\t\t\t\tCASE 37\r\n',
    '\t\t\t\t\t;龍泉寺レンレン\r\n',
    '\t\t\t\t\tRESULTS \'= @"レンレンちゃん"\r\n',
    '\t\t\t\t;--- 下級生 (親しい後輩への「〜ちゃん」) ---\r\n',
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

lines[c27_idx:c31_idx] = new_tier2

out_text = "".join(lines)
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(out_text.encode('cp932'))

print("Updated cases 27 to 30 successfully!")
