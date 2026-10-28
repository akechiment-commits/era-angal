import re
import sys

# Read original ERB
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

text = raw.decode('cp932')

# 1. Update Tier 1
# (a) CASE 47, 63 -> CASE 47, 63, 66, 72
t1_a_target = "\t\tCASE 47, 63\r\n\t\t\t;双葉みなづき/八雲ちづる: 名前+ちゃん\r\n\t\t\tRESULTS '= @\"%CALLNAME:AI%ちゃん\""
t1_a_repl = "\t\tCASE 47, 63, 66, 72\r\n\t\t\t;双葉みなづき/八雲ちづる/曽根セイラ/あんず: 名前+ちゃん\r\n\t\t\tRESULTS '= @\"%CALLNAME:AI%ちゃん\""
assert t1_a_target in text, "t1_a_target not found"
text = text.replace(t1_a_target, t1_a_repl, 1)

# (b) CASE 70 -> CASE 70, 71
t1_b_target = "\t\tCASE 70\r\n\t\t\t;神無月ほとり: 苗字+ちゃん付け\r\n\t\t\tRESULTS '= @\"%SUR%ちゃん\""
t1_b_repl = "\t\tCASE 70, 71\r\n\t\t\t;神無月ほとり/棗ひびき: 苗字+ちゃん付け\r\n\t\t\tRESULTS '= @\"%SUR%ちゃん\""
assert t1_b_target in text, "t1_b_target not found"
text = text.replace(t1_b_target, t1_b_repl, 1)

# (c) CASE 53, 66 -> CASE 53
t1_c_target = "\t\tCASE 53, 66\r\n\t\t\t;花丘まり/曽根セイラ: 呼び名+さん付け\r\n\t\t\tRESULTS '= @\"%CALLNAME:AI%さん\""
t1_c_repl = "\t\tCASE 53\r\n\t\t\t;花丘まり: 呼び名+さん付け\r\n\t\t\tRESULTS '= @\"%CALLNAME:AI%さん\""
assert t1_c_target in text, "t1_c_target not found"
text = text.replace(t1_c_target, t1_c_repl, 1)

# 2. Update Tier 2 (Cases 64 to 72)
# Locate after CASE 63 block
target_t2_start = "\t\tCASE 65\r\n\t\t\t;そら"
assert target_t2_start in text, "target_t2_start not found"

target_t2_end = "\tENDSELECT\r\n\tRETURN\r\n\r\n;============================================================"
assert target_t2_end in text, "target_t2_end not found"

pos_start = text.find(target_t2_start)
pos_end = text.find(target_t2_end)

t2_repl = """\t\tCASE 64
\t\t\t;峰山しおん (3-C / 華道家元令嬢・図書委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 文芸部後輩・足長おじさん後継者 (46回登場！) ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (溺愛する後輩)
\t\t\t\t\tRESULTS '= @"あいかくん"
\t\t\t\t;--- 演劇部後輩 ---
\t\t\t\tCASE 8
\t\t\t\t\t;桐山ゆゆ (文通後輩・6回登場)
\t\t\t\t\tRESULTS '= @"ゆゆくん"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (原作直接呼びかけ「少年」多数！)
\t\t\t\t\tRESULTS '= @"少年"
\t\t\tENDSELECT
\t\tCASE 65
\t\t\t;時国そら (3-C / オカルト研究部・天文部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 親友・双葉姉妹 (ちゃん付け！) ---
\t\t\t\tCASE 46
\t\t\t\t\t;双葉みづき (親友・14回登場)
\t\t\t\t\tRESULTS '= @"みづきちゃん"
\t\t\t\tCASE 47
\t\t\t\t\t;双葉みなづき (親友・37回登場)
\t\t\t\t\tRESULTS '= @"みなづきちゃん"
\t\t\t\t;--- オカルト崇拝 ---
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (生き神さま・26回登場！)
\t\t\t\t\tRESULTS '= @"生き神さま"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"転校生さん"
\t\t\tENDSELECT
\t\tCASE 66
\t\t\t;曽根セイラ (3-C / 軽音部ギターボーカル)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 最愛の親友 (151回登場！) ---
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (最愛のクロちゃん！)
\t\t\t\t\tRESULTS '= @"クロちゃん"
\t\t\t\t;--- 軽音部仲間 (カタカナ愛称) ---
\t\t\t\tCASE 9
\t\t\t\t\t;樋山るか (軽音部・26回登場)
\t\t\t\t\tRESULTS '= @"ルカちゃん"
\t\t\t\tCASE 20
\t\t\t\t\t;藤猪しずく (軽音部・20回登場)
\t\t\t\t\tRESULTS '= @"シズちゃん"
\t\t\t\t;--- 固有愛称 ---
\t\t\t\tCASE 35
\t\t\t\t\t;梅園かな (5回登場)
\t\t\t\t\tRESULTS '= @"梅ちゃん"
\t\t\t\tCASE 3
\t\t\t\t\t;三善かなえ (3回登場)
\t\t\t\t\tRESULTS '= @"みよちゃん"
\t\t\tENDSELECT
\t\tCASE 67
\t\t\t;日滝ましろ (3-C / チアリーディング部部長・科学部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- チア部部員 (団長からの団員呼び・圧倒的！) ---
\t\t\t\tCASE 29
\t\t\t\t\t;春風なな (チア部相棒・111回登場！)
\t\t\t\t\tRESULTS '= @"春風団員"
\t\t\t\tCASE 14
\t\t\t\t\t;花音ことり (チア部部員・51回登場！)
\t\t\t\t\tRESULTS '= @"花音団員"
\t\t\t\t;--- 固有ちゃん付け ---
\t\t\t\tCASE 37
\t\t\t\t\t;龍泉寺レンレン
\t\t\t\t\tRESULTS '= @"レンレンちゃん"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (85回登場！)
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\tENDSELECT
\t\tCASE 68
\t\t\t;深鳥ふみ (3-C / 新聞部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 新聞部最愛の相棒 (呼び捨て・195回登場！) ---
\t\t\t\tCASE 44
\t\t\t\t\t;笹芽ひよの (相棒)
\t\t\t\t\tRESULTS '= @"ひよの"
\t\t\t\t;--- 敬愛する元部長 (43回登場！) ---
\t\t\t\tCASE 64
\t\t\t\t\t;峰山しおん (しおん部長)
\t\t\t\t\tRESULTS '= @"しおん部長"
\t\t\t\t;--- 正義の味方 ---
\t\t\t\tCASE 40
\t\t\t\t\t;夜霧はやて (40回登場)
\t\t\t\t\tRESULTS '= @"はやてちゃん"
\t\t\t\t;--- 生徒会長 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり
\t\t\t\t\tRESULTS '= @"生徒会長"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (28回登場・呼び捨て)
\t\t\t\t\tRESULTS '= @"転校生"
\t\t\tENDSELECT
\t\tCASE 69
\t\t\t;神樹はじめ (3-C / 弓道部・美化委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 実妹 (呼び捨て・233回登場！) ---
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (実妹)
\t\t\t\t\tRESULTS '= @"いちか"
\t\t\t\t;--- 幼馴染親友 (140回登場！) ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (ひ～ちゃん)
\t\t\t\t\tRESULTS '= @"ひ～ちゃん"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (98回登場！)
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\tENDSELECT
\t\tCASE 70
\t\t\t;神無月ほとり (3-C / 陸上部・走高跳・図書委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 陸上部親友 (217回以上登場！) ---
\t\t\t\tCASE 28
\t\t\t\t\t;星海こよい (相棒)
\t\t\t\t\tRESULTS '= @"星ちゃん"
\t\t\t\t;--- 幼馴染 (呼び捨て・110回以上登場！) ---
\t\t\t\tCASE 58
\t\t\t\t\t;天宮るり (呼び捨て)
\t\t\t\t\tRESULTS '= @"るり"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (94回登場！)
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\tENDSELECT
\t\tCASE 71
\t\t\t;棗ひびき (3-C / 水泳部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 水泳部相棒 (128回登場！) ---
\t\t\t\tCASE 22
\t\t\t\t\t;鯱いかり (相棒)
\t\t\t\t\tRESULTS '= @"しゃっちん"
\t\t\t\t;--- 水泳仲間 (94回登場！) ---
\t\t\t\tCASE 59
\t\t\t\t\t;水嶌うしお (金魚ちん)
\t\t\t\t\tRESULTS '= @"金魚ちん"
\t\t\t\t;--- 敬愛する同級生部長 (22回登場！) ---
\t\t\t\tCASE 53
\t\t\t\t\t;花丘まり (まり姐さん)
\t\t\t\t\tRESULTS '= @"まり姐さん"
\t\t\t\t;--- 水泳講座・固有ちん付け ---
\t\t\t\tCASE 18
\t\t\t\t\t;熊沢ひめの (13回登場)
\t\t\t\t\tRESULTS '= @"熊沢ちん"
\t\t\t\tCASE 8
\t\t\t\t\t;桐山ゆゆ (9回登場)
\t\t\t\t\tRESULTS '= @"ダニエルちん"
\t\t\t\tCASE 49
\t\t\t\t\t;小松ぼたん (8回登場)
\t\t\t\t\tRESULTS '= @"こまっちん"
\t\t\t\tCASE 65
\t\t\t\t\t;時国そら (7回登場)
\t\t\t\t\tRESULTS '= @"とっき～"
\t\t\t\tCASE 7
\t\t\t\t\t;木之下ゆの (7回登場)
\t\t\t\t\tRESULTS '= @"木之下ちん"
\t\t\t\tCASE 19
\t\t\t\t\t;猫塚みけ (4回登場)
\t\t\t\t\tRESULTS '= @"猫塚ちん"
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (4回登場)
\t\t\t\t\tRESULTS '= @"れいかちん"
\t\t\t\t;--- 会長ちゃん・ぎんちゃん ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (5回登場)
\t\t\t\t\tRESULTS '= @"会長ちゃん"
\t\t\t\tCASE 50
\t\t\t\t\t;山條ぎん (8回登場)
\t\t\t\t\tRESULTS '= @"ぎんちゃん"
\t\t\t\t;--- 転校生 ---
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (57回登場！)
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\tENDSELECT
\t\tCASE 72
\t\t\t;あんず (3-C扱い / 茶道部元部長・転校生プロデューサー)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 幼馴染妹分 (呼び捨て) ---
\t\t\t\tCASE 24
\t\t\t\t\t;三波なつみ (弟の幼馴染)
\t\t\t\t\tRESULTS '= @"なつみ"
\t\t\t\t;--- 親友同級生 (呼び捨て) ---
\t\t\t\tCASE 52
\t\t\t\t\t;湖南やこ (大親友)
\t\t\t\t\tRESULTS '= @"やこ"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (天使として慕われる)
\t\t\t\t\tRESULTS '= @"すず"
\t\t\t\tCASE 63
\t\t\t\t\t;八雲ちづる (親友)
\t\t\t\t\tRESULTS '= @"ちづる"
\t\t\t\tCASE 36
\t\t\t\t\t;遠見ちか
\t\t\t\t\tRESULTS '= @"ちか"
\t\t\tENDSELECT
"""

# Normalize CRLF in t2_repl
t2_repl = t2_repl.replace('\r\n', '\n').replace('\n', '\r\n')

# Replace in text
text = text[:pos_start] + t2_repl + text[pos_end:]

# Encode to cp932 with strict error handling
new_raw = text.encode('cp932')

# Verify CRLF integrity
assert b'\r\r\n' not in new_raw, "Corrupted CRLF detected"
assert b'\n' not in new_raw.replace(b'\r\n', b''), "Bare LF detected"

with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(new_raw)

print("Successfully applied 3-C definitions to ERB/AITE_YOBI_相手呼称.ERB!")
