# -*- coding: utf-8 -*-
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    lines = [l.decode('cp932') for l in f.readlines()]

# 1. 中黒除去ガード
guard_found = False
for i in range(14, 20):
    if 'REPLACE(NAME:AI, CALLNAME:AI, "")' in lines[i]:
        if 'REPLACE(SUR, "・", "")' not in lines[i+1]:
            lines.insert(i+1, '\tSUR \'= REPLACE(SUR, "・", "")\r\n')
            guard_found = True
            break
print("Guard inserted:", guard_found)

# 2. 第1階層の置換
for i, l in enumerate(lines[:100]):
    if l.startswith('\t\tCASE 26, 33, 46\r\n'):
        # 置換
        new_lines_26 = [
            '\t\tCASE 33, 46\r\n',
            '\t\t\t;柊るな/双葉みづき: 苗字で呼び捨て\r\n',
            '\t\t\tRESULTS \'= @"%SUR%"\r\n',
            '\t\tCASE 26\r\n',
            '\t\t\t;堀田さあや: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「苗字呼び捨て」\r\n',
            '\t\t\tIF GET_CHARA_GRADE(AI) > 2\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%先輩"\r\n',
            '\t\t\tELSE\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%"\r\n',
            '\t\t\tENDIF\r\n'
        ]
        # 元の2行（CASE 26, 33, 46 と その次のコメントとRESULTS）を置き換える
        # 元の構造を確認
        lines[i:i+3] = new_lines_26
        break

for i, l in enumerate(lines[:120]):
    if l.startswith('\t\tCASE 35, 43, 44, 45, 47, 48, 49, 52, 54, 55, 57, 60, 62, 65, 67, 68, 69\r\n'):
        lines[i] = '\t\tCASE 25, 35, 43, 44, 45, 47, 48, 49, 52, 54, 55, 57, 60, 62, 65, 67, 68, 69\r\n'
        break

for i, l in enumerate(lines[:120]):
    if l.startswith('\t\tCASE 24, 59, 61, 63\r\n'):
        new_lines_24 = [
            '\t\tCASE 24\r\n',
            '\t\t\t;三波なつみ: 上級生(3年)は「苗字+さん」、同級生(2年)は「名前+ちゃん」、下級生(1年)は「苗字+さん」\r\n',
            '\t\t\tIF GET_CHARA_GRADE(AI) == 2\r\n',
            '\t\t\t\tRESULTS \'= @"%CALLNAME:AI%ちゃん"\r\n',
            '\t\t\tELSE\r\n',
            '\t\t\t\tRESULTS \'= @"%SUR%さん"\r\n',
            '\t\t\tENDIF\r\n',
            '\t\tCASE 59, 61, 63\r\n'
        ]
        lines[i:i+1] = new_lines_24
        break

# 3. 第2階層の置換
# 外側の CASE 24 と CASE 27 の位置を再探索
c24_idx = None
c27_idx = None
for i, l in enumerate(lines):
    if l == '\t\tCASE 24\r\n' and i > 200:
        c24_idx = i
    if l == '\t\tCASE 27\r\n' and i > 200:
        c27_idx = i
        break

print(f"Outer CASE 24 index: {c24_idx}, CASE 27 index: {c27_idx}")
assert c24_idx is not None and c27_idx is not None
assert lines[c24_idx - 1].strip() == "ENDSELECT"
assert lines[c27_idx - 1].strip() == "ENDSELECT"

new_tier2 = [
    '\t\tCASE 24\r\n',
    '\t\t\t;三波なつみ (2-A / 美術部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 49\r\n',
    '\t\t\t\t\t;小松ぼたん (美術部先輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"ぼたん先輩"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\tCASE 67\r\n',
    '\t\t\t\t\t;日滝ましろ (チア部先輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"日滝先輩"\r\n',
    '\t\t\t\t;--- 同級生 (第1階層の「〜ちゃん」から距離のある「〜さん」へ) ---\r\n',
    '\t\t\t\tCASE 31\r\n',
    '\t\t\t\t\t;夢路まりあ\r\n',
    '\t\t\t\t\tRESULTS \'= @"まりあさん"\r\n',
    '\t\t\t\tCASE 32\r\n',
    '\t\t\t\t\t;安条まい\r\n',
    '\t\t\t\t\tRESULTS \'= @"安条さん"\r\n',
    '\t\t\t\tCASE 34\r\n',
    '\t\t\t\t\t;桐島かいり\r\n',
    '\t\t\t\t\tRESULTS \'= @"桐島さん"\r\n',
    '\t\t\t\tCASE 35\r\n',
    '\t\t\t\t\t;梅園かな\r\n',
    '\t\t\t\t\tRESULTS \'= @"梅園さん"\r\n',
    '\t\t\t\tCASE 36\r\n',
    '\t\t\t\t\t;遠見ちか\r\n',
    '\t\t\t\t\tRESULTS \'= @"遠見さん"\r\n',
    '\t\t\t\tCASE 40\r\n',
    '\t\t\t\t\t;夜霧はやて\r\n',
    '\t\t\t\t\tRESULTS \'= @"夜霧さん"\r\n',
    '\t\t\t\t;--- 下級生 (第1階層の「苗字+さん」から親しい「名前+ちゃん」へ) ---\r\n',
    '\t\t\t\tCASE 2\r\n',
    '\t\t\t\t\t;北川ゆき\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆきちゃん"\r\n',
    '\t\t\t\tCASE 4\r\n',
    '\t\t\t\t\t;早川きこ\r\n',
    '\t\t\t\t\tRESULTS \'= @"きこちゃん"\r\n',
    '\t\t\t\tCASE 11\r\n',
    '\t\t\t\t\t;氷野くるみ\r\n',
    '\t\t\t\t\tRESULTS \'= @"くるみちゃん"\r\n',
    '\t\t\t\tCASE 12\r\n',
    '\t\t\t\t\t;神樹いちか\r\n',
    '\t\t\t\t\tRESULTS \'= @"いちかちゃん"\r\n',
    '\t\t\t\tCASE 14\r\n',
    '\t\t\t\t\t;花音ことり\r\n',
    '\t\t\t\t\tRESULTS \'= @"ことりちゃん"\r\n',
    '\t\t\t\tCASE 17\r\n',
    '\t\t\t\t\t;小鳩あずさ\r\n',
    '\t\t\t\t\tRESULTS \'= @"あずさちゃん"\r\n',
    '\t\t\t\tCASE 20\r\n',
    '\t\t\t\t\t;藤猪しずく\r\n',
    '\t\t\t\t\tRESULTS \'= @"しずくちゃん"\r\n',
    '\t\t\t\tCASE 21\r\n',
    '\t\t\t\t\t;雉子すみれ (美術部後輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"すみれちゃん"\r\n',
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 25\r\n',
    '\t\t\t;八朔つゆり (2-A / 保健委員会)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 同級生 ---\r\n',
    '\t\t\t\tCASE 24\r\n',
    '\t\t\t\t\t;三波なつみ\r\n',
    '\t\t\t\t\tRESULTS \'= @"なつみちゃん"\r\n',
    '\t\t\t\tCASE 26\r\n',
    '\t\t\t\t\t;堀田さあや\r\n',
    '\t\t\t\t\tRESULTS \'= @"さあやちゃん"\r\n',
    '\t\t\t\tCASE 27\r\n',
    '\t\t\t\t\t;夏野ゆり (大親友)\r\n',
    '\t\t\t\t\tRESULTS \'= @"なっちゃん"\r\n',
    '\t\t\t\tCASE 28\r\n',
    '\t\t\t\t\t;星海こよい (従姉妹)\r\n',
    '\t\t\t\t\tRESULTS \'= @"こよちゃん"\r\n',
    '\t\t\t\tCASE 29\r\n',
    '\t\t\t\t\t;春風なな\r\n',
    '\t\t\t\t\tRESULTS \'= @"ななちゃん"\r\n',
    '\t\t\t\tCASE 30\r\n',
    '\t\t\t\t\t;長居ゆう\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆうちゃん"\r\n',
    '\t\t\t\tCASE 31\r\n',
    '\t\t\t\t\t;夢路まりあ (親友・保健室仲間)\r\n',
    '\t\t\t\t\tRESULTS \'= @"まりあちゃん"\r\n',
    '\t\t\t\tCASE 38\r\n',
    '\t\t\t\t\t;クー・カロア\r\n',
    '\t\t\t\t\tRESULTS \'= @"クーさん"\r\n',
    '\t\t\t\t;--- 下級生 ---\r\n',
    '\t\t\t\tCASE 1\r\n',
    '\t\t\t\t\t;三善かなえ\r\n',
    '\t\t\t\t\tRESULTS \'= @"かなえちゃん"\r\n',
    '\t\t\t\tCASE 11\r\n',
    '\t\t\t\t\t;氷野くるみ (保健委員会後輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"くるみちゃん"\r\n',
    '\t\t\t\tCASE 17\r\n',
    '\t\t\t\t\t;小鳩あずさ (保健委員会後輩)\r\n',
    '\t\t\t\t\tRESULTS \'= @"あずさちゃん"\r\n',
    '\t\t\t\tCASE 20\r\n',
    '\t\t\t\t\t;藤猪しずく (親愛・家族ごっこ)\r\n',
    '\t\t\t\t\tRESULTS \'= @"しずくちゃん"\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 50\r\n',
    '\t\t\t\t\t;山條ぎん\r\n',
    '\t\t\t\t\tRESULTS \'= @"ぎんさん"\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長さん"\r\n',
    '\t\t\t\tCASE 65\r\n',
    '\t\t\t\t\t;時国そら (保健委員会・オカ研)\r\n',
    '\t\t\t\t\tRESULTS \'= @"時国先輩"\r\n',
    '\t\t\t\tCASE 66\r\n',
    '\t\t\t\t\t;曽根セイラ (入院仲間)\r\n',
    '\t\t\t\t\tRESULTS \'= @"曽根先輩"\r\n',
    '\t\t\t\tCASE 67\r\n',
    '\t\t\t\t\t;日滝ましろ\r\n',
    '\t\t\t\t\tRESULTS \'= @"ましろさん"\r\n',
    '\t\t\tENDSELECT\r\n',
    '\t\tCASE 26\r\n',
    '\t\t\t;堀田さあや (2-A / バレー部)\r\n',
    '\t\t\tSELECTCASE AI\r\n',
    '\t\t\t\t;--- 上級生 ---\r\n',
    '\t\t\t\tCASE 61\r\n',
    '\t\t\t\t\t;鶴海ひまり (生徒会長)\r\n',
    '\t\t\t\t\tRESULTS \'= @"生徒会長"\r\n',
    '\t\t\t\t;--- 同級生 (苗字呼び捨てからさん付けへ) ---\r\n',
    '\t\t\t\tCASE 31\r\n',
    '\t\t\t\t\t;夢路まりあ\r\n',
    '\t\t\t\t\tRESULTS \'= @"夢路さん"\r\n',
    '\t\t\t\tCASE 33\r\n',
    '\t\t\t\t\t;柊るな\r\n',
    '\t\t\t\t\tRESULTS \'= @"柊さん"\r\n',
    '\t\t\t\tCASE 36\r\n',
    '\t\t\t\t\t;遠見ちか\r\n',
    '\t\t\t\t\tRESULTS \'= @"遠見さん"\r\n',
    '\t\t\t\t;--- 下級生 (苗字呼び捨てからさん付け・ちゃん付けへ) ---\r\n',
    '\t\t\t\tCASE 6\r\n',
    '\t\t\t\t\t;藍乃あいか (怪我の手当て・おんぶ)\r\n',
    '\t\t\t\t\tRESULTS \'= @"あいかちゃん"\r\n',
    '\t\t\t\tCASE 8\r\n',
    '\t\t\t\t\t;丸子みさき\r\n',
    '\t\t\t\t\tRESULTS \'= @"丸子さん"\r\n',
    '\t\t\t\tCASE 10\r\n',
    '\t\t\t\t\t;木之下ゆゆ\r\n',
    '\t\t\t\t\tRESULTS \'= @"ゆゆちゃん"\r\n',
    '\t\t\t\tCASE 15\r\n',
    '\t\t\t\t\t;長町やえ\r\n',
    '\t\t\t\t\tRESULTS \'= @"長町さん"\r\n',
    '\t\t\t\tCASE 23\r\n',
    '\t\t\t\t\t;鶯木こはる\r\n',
    '\t\t\t\t\tRESULTS \'= @"鶯木さん"\r\n',
    '\t\t\tENDSELECT\r\n'
]

lines[c24_idx:c27_idx] = new_tier2

# 書き出し（厳密なバイナリ書き込み）
out_text = "".join(lines)
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(out_text.encode('cp932'))

print("Applied perfectly with line precision!")
