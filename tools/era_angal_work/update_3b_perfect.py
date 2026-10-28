import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

text = raw.decode('cp932')

# Replace CASE 53 to 63 block
target_start = "\t\tCASE 53\r\n\t\t\t;花丘まり"
target_end = "\t\tCASE 64\r\n\t\t\t;峰山しおん"

assert target_start in text, "target_start not found"
assert target_end in text, "target_end not found"

pos_start = text.find(target_start)
pos_end = text.find(target_end)

repl_3b = """\t\tCASE 53
\t\t\t;花丘まり (3-B / テニス部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生さん"
\t\t\t\t;--- テニス部後輩（愛称） ---
\t\t\t\tCASE 18
\t\t\t\t\t;熊沢ひめの (テニス部後輩)
\t\t\t\t\tRESULTS '= @"ひめのちゃん"
\t\t\t\tCASE 17
\t\t\t\t\t;小鳩あずさ (テニス部後輩)
\t\t\t\t\tRESULTS '= @"あずさちゃん"
\t\t\t\tCASE 36
\t\t\t\t\t;遠見ちか
\t\t\t\t\tRESULTS '= @"ちかちゃん"
\t\t\t\t;--- お嬢様・後輩への「～様」 ---
\t\t\t\tCASE 34
\t\t\t\t\t;桐島かいり
\t\t\t\t\tRESULTS '= @"かいり様"
\t\t\t\tCASE 31
\t\t\t\t\t;夢路まりあ
\t\t\t\t\tRESULTS '= @"まりあ様"
\t\t\t\tCASE 38
\t\t\t\t\t;クー・カロア
\t\t\t\t\tRESULTS '= @"クー様"
\t\t\t\tCASE 37
\t\t\t\t\t;龍泉寺レンレン
\t\t\t\t\tRESULTS '= @"レンレン様"
\t\t\t\tCASE 43
\t\t\t\t\t;砂賀みどり
\t\t\t\t\tRESULTS '= @"みどり様"
\t\t\t\tCASE 44
\t\t\t\t\t;笹芽ひよの
\t\t\t\t\tRESULTS '= @"ひよの様"
\t\t\t\t;--- 幼馴染・同級生 ---
\t\t\t\tCASE 48
\t\t\t\t\t;四方みつる (王子様)
\t\t\t\t\tRESULTS '= @"みつるさん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT
\t\tCASE 54
\t\t\t;久坂あやめ (3-B / 華道部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 最重要幼馴染（40回登場） ---
\t\t\t\tCASE 56
\t\t\t\t\t;八壁ひかる (幼馴染！「ひかるちゃん」)
\t\t\t\t\tRESULTS '= @"ひかるちゃん"
\t\t\t\t;--- 特別愛称 ---
\t\t\t\tCASE 57
\t\t\t\t\t;岩戸サン (8回登場)
\t\t\t\t\tRESULTS '= @"サンちゃん"
\t\t\t\tCASE 16
\t\t\t\t\t;大虎いさみ
\t\t\t\t\tRESULTS '= @"いさみちゃん"
\t\t\t\tCASE 29
\t\t\t\t\t;春風なな
\t\t\t\t\tRESULTS '= @"ななちゃん"
\t\t\t\tCASE 38
\t\t\t\t\t;クー・カロア (外国人名)
\t\t\t\t\tRESULTS '= @"カロアさん"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめさん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずちゃん"
\t\t\tENDSELECT
\t\tCASE 55
\t\t\t;伊藤さくら (3-B / 園芸部・美化委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生さん"
\t\t\t\t;--- 崇拝対象 ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (フォロワーとして崇拝)
\t\t\t\t\tRESULTS '= @"れいか様"
\t\t\t\t;--- 親友フォロワー（75回登場） ---
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (親友)
\t\t\t\t\tRESULTS '= @"かえで"
\t\t\t\t;--- 生徒会長 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり
\t\t\t\t\tRESULTS '= @"鶴海会長"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめさん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (35回登場！)
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT
\t\tCASE 56
\t\t\t;八壁ひかる (3-B / 柔道部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生"
\t\t\t\t;--- 最重要幼馴染（72回登場・絶対的呼び捨て） ---
\t\t\t\tCASE 54
\t\t\t\t\t;久坂あやめ (幼馴染！「あやめ」)
\t\t\t\t\tRESULTS '= @"あやめ"
\t\t\t\t;--- 柔道部後輩・ライバル ---
\t\t\t\tCASE 16
\t\t\t\t\t;大虎いさみ (後輩・30回登場)
\t\t\t\t\tRESULTS '= @"いさみ"
\t\t\t\tCASE 37
\t\t\t\t\t;龍泉寺レンレン (宿敵ライバル)
\t\t\t\t\tRESULTS '= @"龍泉寺"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"いちか"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめ"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんず"
\t\t\tENDSELECT
\t\tCASE 57
\t\t\t;岩戸サン (3-B / 陸上部部長・走高跳)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 陸上部（公式設定明記） ---
\t\t\t\tCASE 48
\t\t\t\t\t;四方みつる (副部長)
\t\t\t\t\tRESULTS '= @"みつる"
\t\t\t\tCASE 42
\t\t\t\t\t;榊むつみ (後輩)
\t\t\t\t\tRESULTS '= @"むつみ"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"いちか"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめ"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんず"
\t\t\tENDSELECT
\t\tCASE 58
\t\t\t;天宮るり (3-B / 軽音部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 最重要親友・幼馴染（111回登場） ---
\t\t\t\tCASE 70
\t\t\t\t\t;神無月ほとり (唯一無二の理解者)
\t\t\t\t\tRESULTS '= @"ほとりちゃん"
\t\t\t\t;--- 生徒会長 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり
\t\t\t\t\tRESULTS '= @"生徒会長"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT
\t\tCASE 59
\t\t\t;水嶌うしお (3-B / 水泳部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 最重要親友（138回登場・ちゃん付け！） ---
\t\t\t\tCASE 46
\t\t\t\t\t;双葉みづき (親友)
\t\t\t\t\tRESULTS '= @"みづきちゃん"
\t\t\t\t;--- 親しい友人・後輩 ---
\t\t\t\tCASE 71
\t\t\t\t\t;棗ひびき (水泳部相棒・69回登場)
\t\t\t\t\tRESULTS '= @"ひびきちゃん"
\t\t\t\tCASE 22
\t\t\t\t\t;鯱いかり (水泳部後輩・32回登場)
\t\t\t\t\tRESULTS '= @"いかりちゃん"
\t\t\t\tCASE 65
\t\t\t\t\t;時国そら (14回登場)
\t\t\t\t\tRESULTS '= @"そらちゃん"
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (3回登場)
\t\t\t\t\tRESULTS '= @"ひまりちゃん"
\t\t\t\tCASE 50
\t\t\t\t\t;山條ぎん
\t\t\t\t\tRESULTS '= @"ぎんちゃん"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ
\t\t\t\t\tRESULTS '= @"かすみん"
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (敬称)
\t\t\t\t\tRESULTS '= @"瀬川さん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんず"
\t\t\tENDSELECT
\t\tCASE 60
\t\t\t;瀬川かえで (3-B / 弓道部・風紀委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生"
\t\t\t\t;--- 崇拝対象 ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (フォロワーとして絶対崇拝)
\t\t\t\t\tRESULTS '= @"れいか様"
\t\t\t\t;--- 親友フォロワー（251回登場・さん付け！） ---
\t\t\t\tCASE 55
\t\t\t\t\t;伊藤さくら (親友)
\t\t\t\t\tRESULTS '= @"さくらさん"
\t\t\t\t;--- 特別愛称 ---
\t\t\t\tCASE 56
\t\t\t\t\t;八壁ひかる (3回登場)
\t\t\t\t\tRESULTS '= @"ひかるくん"
\t\t\t\tCASE 57
\t\t\t\t\t;岩戸サン (5回登場)
\t\t\t\t\tRESULTS '= @"サン"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"いちか"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめ"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんず"
\t\t\tENDSELECT
\t\tCASE 61
\t\t\t;鶴海ひまり (3-B / 現生徒会長・合唱部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 敬愛する前会長（183回登場） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長)
\t\t\t\t\tRESULTS '= @"れいか先輩"
\t\t\t\t;--- 愛称 ---
\t\t\t\tCASE 06
\t\t\t\t\t;藍乃あいか (170回登場！)
\t\t\t\t\tRESULTS '= @"あいかちゃん"
\t\t\t\tCASE 54
\t\t\t\t\t;久坂あやめ (80回登場！)
\t\t\t\t\tRESULTS '= @"あやめちゃん"
\t\t\t\tCASE 53
\t\t\t\t\t;花丘まり (56回登場！)
\t\t\t\t\tRESULTS '= @"まりちゃん"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (固有愛称)
\t\t\t\t\tRESULTS '= @"くろりん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (17回登場！)
\t\t\t\t\tRESULTS '= @"アンジー"
\t\t\tENDSELECT
\t\tCASE 62
\t\t\t;黒森すず (3-B / 軽音部ベース担当)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"キミ"
\t\t\t\t;--- 軽音部仲間・固有愛称（公式設定明記） ---
\t\t\t\tCASE 9
\t\t\t\t\t;月永るか (136回登場)
\t\t\t\t\tRESULTS '= @"ルカ"
\t\t\t\tCASE 20
\t\t\t\t\t;藤猪しずく (公式設定)
\t\t\t\t\tRESULTS '= @"シズ"
\t\t\t\tCASE 66
\t\t\t\t\t;曽根セイラ (公式設定)
\t\t\t\t\tRESULTS '= @"セイ"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (ボクの天使・36回登場！)
\t\t\t\t\tRESULTS '= @"あんずちゃん"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"いちか"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめ"
\t\t\tENDSELECT
\t\tCASE 63
\t\t\t;八雲ちづる (3-B / 美化委員・合唱部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 最重要片想い（151回登場・「王子様」） ---
\t\t\t\tCASE 48
\t\t\t\t\t;四方みつる (王子様)
\t\t\t\t\tRESULTS '= @"みつるちゃん"
\t\t\t\t;--- 親友・悪友（264回登場！） ---
\t\t\t\tCASE 52
\t\t\t\t\t;湖南やこ (やこちゃん！)
\t\t\t\t\tRESULTS '= @"やこちゃん"
\t\t\t\t;--- 演劇部後輩（175回登場！） ---
\t\t\t\tCASE 36
\t\t\t\t\t;遠見ちか (ちかちゃん！)
\t\t\t\t\tRESULTS '= @"ちかちゃん"
\t\t\t\t;--- 呼び捨て同級生 ---
\t\t\t\tCASE 57
\t\t\t\t\t;岩戸サン
\t\t\t\t\tRESULTS '= @"サン"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず
\t\t\t\t\tRESULTS '= @"すず"
\t\t\t\tCASE 66
\t\t\t\t\t;曽根セイラ
\t\t\t\t\tRESULTS '= @"セイラちゃん"
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか
\t\t\t\t\tRESULTS '= @"アイカ"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"いちか"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめ"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (27回登場！)
\t\t\t\t\tRESULTS '= @"あんずちゃん"
\t\t\tENDSELECT
"""

# Normalize CRLF
repl_3b = repl_3b.replace('\r\n', '\n').replace('\n', '\r\n')

text = text[:pos_start] + repl_3b + text[pos_end:]

new_raw = text.encode('cp932')
assert b'\r\r\n' not in new_raw, "Corrupted CRLF detected"
assert b'\n' not in new_raw.replace(b'\r\n', b''), "Bare LF detected"

with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(new_raw)

print("Successfully updated 3-B definitions in ERB/AITE_YOBI_相手呼称.ERB!")
