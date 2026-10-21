# -*- coding: utf-8 -*-
import sys, os

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

text = raw.decode('cp932')

# 1. 第1階層
pattern_26 = "\t\tCASE 26, 33, 46\r\n"
assert pattern_26 in text

new_tier1_26 = """\t\tCASE 33, 46
\t\t\t;柊るな/双葉みづき: 苗字で呼び捨て
\t\t\tRESULTS '= @"%SUR%"
\t\tCASE 26
\t\t\t;堀田さあや: 上級生(3年)は「苗字+先輩」、同級生・下級生(2年・1年)は「苗字呼び捨て」
\t\t\tIF GET_CHARA_GRADE(AI) > 2
\t\t\t\tRESULTS '= @"%SUR%先輩"
\t\t\tELSE
\t\t\t\tRESULTS '= @"%SUR%"
\t\t\tENDIF\r\n""".replace('\r\n', '\n').replace('\n', '\r\n')

pattern_24 = "\t\tCASE 24, 59, 61, 63\r\n"
assert pattern_24 in text

new_tier1_24 = """\t\tCASE 24
\t\t\t;三波なつみ: 上級生(3年)は「苗字+さん」、同級生(2年)は「名前+ちゃん」、下級生(1年)は「苗字+さん」
\t\t\tIF GET_CHARA_GRADE(AI) == 2
\t\t\t\tRESULTS '= @"%CALLNAME:AI%ちゃん"
\t\t\tELSE
\t\t\t\tRESULTS '= @"%SUR%さん"
\t\t\tENDIF
\t\tCASE 59, 61, 63\r\n""".replace('\r\n', '\n').replace('\n', '\r\n')

pattern_25_group = "\t\tCASE 35, 43, 44, 45, 47, 48, 49, 52, 54, 55, 57, 60, 62, 65, 67, 68, 69\r\n"
assert pattern_25_group in text

new_tier1_25 = "\t\tCASE 25, 35, 43, 44, 45, 47, 48, 49, 52, 54, 55, 57, 60, 62, 65, 67, 68, 69\r\n"

# 2. 第2階層
idx_start = text.find("\t\tCASE 24\r\n", 4000)
idx_end = text.find("\t\tCASE 27\r\n", idx_start)

new_tier2_24_26 = """\t\tCASE 24
\t\t\t;三波なつみ (2-A / 美術部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 上級生 ---
\t\t\t\tCASE 49
\t\t\t\t\t;小松ぼたん (美術部先輩)
\t\t\t\t\tRESULTS '= @"ぼたん先輩"
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (生徒会長)
\t\t\t\t\tRESULTS '= @"生徒会長"
\t\t\t\tCASE 67
\t\t\t\t\t;日滝ましろ (チア部先輩)
\t\t\t\t\tRESULTS '= @"日滝先輩"
\t\t\t\t;--- 同級生 (第1階層の「〜ちゃん」から距離のある「〜さん」へ) ---
\t\t\t\tCASE 31
\t\t\t\t\t;夢路まりあ
\t\t\t\t\tRESULTS '= @"まりあさん"
\t\t\t\tCASE 32
\t\t\t\t\t;安条まい
\t\t\t\t\tRESULTS '= @"安条さん"
\t\t\t\tCASE 34
\t\t\t\t\t;桐島かいり
\t\t\t\t\tRESULTS '= @"桐島さん"
\t\t\t\tCASE 35
\t\t\t\t\t;梅園かな
\t\t\t\t\tRESULTS '= @"梅園さん"
\t\t\t\tCASE 36
\t\t\t\t\t;遠見ちか
\t\t\t\t\tRESULTS '= @"遠見さん"
\t\t\t\tCASE 40
\t\t\t\t\t;夜霧はやて
\t\t\t\t\tRESULTS '= @"夜霧さん"
\t\t\t\t;--- 下級生 (第1階層の「苗字+さん」から親しい「名前+ちゃん」へ) ---
\t\t\t\tCASE 2
\t\t\t\t\t;北川ゆき
\t\t\t\t\tRESULTS '= @"ゆきちゃん"
\t\t\t\tCASE 4
\t\t\t\t\t;早川きこ
\t\t\t\t\tRESULTS '= @"きこちゃん"
\t\t\t\tCASE 11
\t\t\t\t\t;氷野くるみ
\t\t\t\t\tRESULTS '= @"くるみちゃん"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか
\t\t\t\t\tRESULTS '= @"いちかちゃん"
\t\t\t\tCASE 14
\t\t\t\t\t;花音ことり
\t\t\t\t\tRESULTS '= @"ことりちゃん"
\t\t\t\tCASE 17
\t\t\t\t\t;小鳩あずさ
\t\t\t\t\tRESULTS '= @"あずさちゃん"
\t\t\t\tCASE 20
\t\t\t\t\t;藤猪しずく
\t\t\t\t\tRESULTS '= @"しずくちゃん"
\t\t\t\tCASE 21
\t\t\t\t\t;雉子すみれ (美術部後輩)
\t\t\t\t\tRESULTS '= @"すみれちゃん"
\t\t\tENDSELECT
\t\tCASE 25
\t\t\t;八朔つゆり (2-A / 保健委員会)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 同級生 ---
\t\t\t\tCASE 24
\t\t\t\t\t;三波なつみ
\t\t\t\t\tRESULTS '= @"なつみちゃん"
\t\t\t\tCASE 26
\t\t\t\t\t;堀田さあや
\t\t\t\t\tRESULTS '= @"さあやちゃん"
\t\t\t\tCASE 27
\t\t\t\t\t;夏野ゆり (大親友)
\t\t\t\t\tRESULTS '= @"なっちゃん"
\t\t\t\tCASE 28
\t\t\t\t\t;星海こよい (従姉妹)
\t\t\t\t\tRESULTS '= @"こよちゃん"
\t\t\t\tCASE 29
\t\t\t\t\t;春風なな
\t\t\t\t\tRESULTS '= @"ななちゃん"
\t\t\t\tCASE 30
\t\t\t\t\t;長居ゆう
\t\t\t\t\tRESULTS '= @"ゆうちゃん"
\t\t\t\tCASE 31
\t\t\t\t\t;夢路まりあ (親友・保健室仲間)
\t\t\t\t\tRESULTS '= @"まりあちゃん"
\t\t\t\tCASE 38
\t\t\t\t\t;クー・カロア
\t\t\t\t\tRESULTS '= @"クーさん"
\t\t\t\t;--- 下級生 ---
\t\t\t\tCASE 1
\t\t\t\t\t;三善かなえ
\t\t\t\t\tRESULTS '= @"かなえちゃん"
\t\t\t\tCASE 11
\t\t\t\t\t;氷野くるみ (保健委員会後輩)
\t\t\t\t\tRESULTS '= @"くるみちゃん"
\t\t\t\tCASE 17
\t\t\t\t\t;小鳩あずさ (保健委員会後輩)
\t\t\t\t\tRESULTS '= @"あずさちゃん"
\t\t\t\tCASE 20
\t\t\t\t\t;藤猪しずく (親愛・家族ごっこ)
\t\t\t\t\tRESULTS '= @"しずくちゃん"
\t\t\t\t;--- 上級生 ---
\t\t\t\tCASE 50
\t\t\t\t\t;山條ぎん
\t\t\t\t\tRESULTS '= @"ぎんさん"
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (生徒会長)
\t\t\t\t\tRESULTS '= @"生徒会長さん"
\t\t\t\tCASE 65
\t\t\t\t\t;時国そら (保健委員会・オカ研)
\t\t\t\t\tRESULTS '= @"時国先輩"
\t\t\t\tCASE 66
\t\t\t\t\t;曽根セイラ (入院仲間)
\t\t\t\t\tRESULTS '= @"曽根先輩"
\t\t\t\tCASE 67
\t\t\t\t\t;日滝ましろ
\t\t\t\t\tRESULTS '= @"ましろさん"
\t\t\tENDSELECT
\t\tCASE 26
\t\t\t;堀田さあや (2-A / バレー部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 上級生 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (生徒会長)
\t\t\t\t\tRESULTS '= @"生徒会長"
\t\t\t\t;--- 同級生 (苗字呼び捨てからさん付けへ) ---
\t\t\t\tCASE 31
\t\t\t\t\t;夢路まりあ
\t\t\t\t\tRESULTS '= @"夢路さん"
\t\t\t\tCASE 33
\t\t\t\t\t;柊るな
\t\t\t\t\tRESULTS '= @"柊さん"
\t\t\t\tCASE 36
\t\t\t\t\t;遠見ちか
\t\t\t\t\tRESULTS '= @"遠見さん"
\t\t\t\t;--- 下級生 (苗字呼び捨てからさん付け・ちゃん付けへ) ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (怪我の手当て・おんぶ)
\t\t\t\t\tRESULTS '= @"あいかちゃん"
\t\t\t\tCASE 8
\t\t\t\t\t;丸子みさき
\t\t\t\t\tRESULTS '= @"丸子さん"
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ
\t\t\t\t\tRESULTS '= @"ゆゆちゃん"
\t\t\t\tCASE 15
\t\t\t\t\t;長町やえ
\t\t\t\t\tRESULTS '= @"長町さん"
\t\t\t\tCASE 23
\t\t\t\t\t;鶯木こはる
\t\t\t\t\tRESULTS '= @"鶯木さん"
\t\t\tENDSELECT\r\n""".replace('\r\n', '\n').replace('\n', '\r\n')

# 適用
text = text.replace(pattern_26, new_tier1_26)
text = text.replace(pattern_24, new_tier1_24)
text = text.replace(pattern_25_group, new_tier1_25)
text = text[:idx_start] + new_tier2_24_26 + text[idx_end:]

# 保存
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(text.encode('cp932'))

print("Updated successfully with strict CRLF!")
