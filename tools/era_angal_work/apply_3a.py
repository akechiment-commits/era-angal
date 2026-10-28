import os
import re
import shutil

erb_path = 'ERB/AITE_YOBI_相手呼称.ERB'
backup_path = 'ERB/AITE_YOBI_相手呼称.ERB.bak_before_3a'

# Restore from backup first to be clean
if os.path.exists(backup_path):
    shutil.copyfile(backup_path, erb_path)

with open(erb_path, 'rb') as f:
    b = f.read()

text = b.decode('cp932')

# 1. Update Layer 1
replacement_l1_46 = """\t\tCASE 46, 49, 50, 52
			;双葉みづき/小松ぼたん/山條ぎん/湖南やこ: 苗字で呼び捨て
			RESULTS '= @"%SUR%"
		CASE 47
			;双葉みなづき: 名前+ちゃん（甘えん坊妹愛称）
			RESULTS '= @"%CALLNAME:AI%ちゃん"
""".replace('\n', '\r\n').replace('\r\r\n', '\r\n')

replacement_l1_sans = """\t\tCASE 25, 28, 45, 48, 51, 54, 55, 57, 60, 62, 65, 67, 68, 69
			;八朔つゆり/星海こよい/円城寺れいか/四方みつる/御影かすみ/久坂あやめ/伊藤さくら/岩戸サン/瀬川かえで/黒森すず/時国そら/日滝ましろ/深鳥ふみ/神樹はじめ: 苗字+さん付け
			RESULTS '= @"%SUR%さん"
""".replace('\n', '\r\n').replace('\r\r\n', '\r\n')

# Check regex matches
m46 = re.search(r'\t\tCASE 46\r\n\t\t\t;[^\r\n]*\r\n\t\t\tRESULTS \'=[^\r\n]*\r\n', text)
assert m46, "m46 not found!"
text = text[:m46.start()] + replacement_l1_46 + text[m46.end():]

m51 = re.search(r'\t\tCASE 51\r\n\t\t\t;[^\r\n]*\r\n\t\t\tRESULTS \'=[^\r\n]*\r\n', text)
assert m51, "m51 not found!"
text = text[:m51.start()] + text[m51.end():]

m50 = re.search(r'\t\tCASE 50\r\n\t\t\t;[^\r\n]*\r\n\t\t\tRESULTS \'=[^\r\n]*\r\n', text)
assert m50, "m50 not found!"
text = text[:m50.start()] + text[m50.end():]

msans = re.search(r'\t\tCASE 25, 28, 45, 47, 48, 49, 52[^\r\n]*\r\n\t\t\t;[^\r\n]*\r\n\t\t\tRESULTS \'=[^\r\n]*\r\n', text)
assert msans, "msans not found!"
text = text[:msans.start()] + replacement_l1_sans + text[msans.end():]

print("Layer 1 updated successfully.")

# -------------------------------------------------------------
# 2. Update Layer 2 (CASE 45 to CASE 52)
# -------------------------------------------------------------
b_new = text.encode('cp932')

p_c45 = b_new.find(b'\t\tCASE 45\r\n\t\t\t;\x82\xea\x82\xa2\x82\xa9')
assert p_c45 != -1, "CASE 45 not found in Layer 2!"

p_c54 = b_new.find(b'\t\tCASE 54\r\n\t\t\t;\x82\xa0\x82\xe2\x82\xdf', p_c45)
assert p_c54 != -1, "CASE 54 not found in Layer 2!"

new_layer2_code = """\t\tCASE 45
			;円城寺れいか (3-A / 茶道部部長・前生徒会長)
			SELECTCASE AI
				;--- 幼馴染・生徒会長 ---
				CASE 48
					;四方みつる (幼馴染)
					RESULTS '= @"みつる"
				CASE 61
					;鶴海ひまり (後任の生徒会長)
					RESULTS '= @"ひまり"
				;--- 同級生（呼び捨て・愛称） ---
				CASE 46
					;双葉みづき (前書記)
					RESULTS '= @"みづき"
				CASE 47
					;双葉みなづき (前書記)
					RESULTS '= @"みなづき"
				CASE 49
					;小松ぼたん
					RESULTS '= @"ぼたん"
				CASE 50
					;山條ぎん
					RESULTS '= @"山條"
				CASE 51
					;御影かすみ
					RESULTS '= @"かすみ"
				CASE 55
					;伊藤さくら
					RESULTS '= @"さくら"
				CASE 59
					;水嶌うしお
					RESULTS '= @"うしお"
				CASE 60
					;瀬川かえで
					RESULTS '= @"かえで"
				CASE 65
					;時国そら
					RESULTS '= @"そら"
				CASE 67
					;日滝ましろ
					RESULTS '= @"ましろさん"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめさん"
				;--- 後輩（愛称・merry-melody等） ---
				CASE 13
					;羽森つばさ
					RESULTS '= @"つばさ"
				CASE 14
					;花音ことり
					RESULTS '= @"ことり"
				CASE 26
					;堀田さあや
					RESULTS '= @"さあや"
				CASE 28
					;星海こよい
					RESULTS '= @"こよい"
				CASE 41
					;悠木ともこ
					RESULTS '= @"ともこ"
				CASE 72
					;あんず
					RESULTS '= @"あんずさん"
			ENDSELECT
		CASE 46
			;双葉みづき (3-A / オカルト研究部・前生徒会書記)
			SELECTCASE AI
				;--- 最重要（双子の妹） ---
				CASE 47
					;双葉みなづき (双子の妹・110回以上登場)
					RESULTS '= @"みなづき"
				;--- 親友・オカルト仲間・同級生 ---
				CASE 59
					;水嶌うしお (親友の水泳部部長・69回登場)
					RESULTS '= @"うしお"
				CASE 65
					;時国そら (オカルト研究部仲間・60回登場)
					RESULTS '= @"そら"
				CASE 51
					;御影かすみ (34回登場)
					RESULTS '= @"かすみ"
				CASE 61
					;鶴海ひまり (現生徒会長)
					RESULTS '= @"ひまり"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめ"
				CASE 48
					;四方みつる
					RESULTS '= @"みつる"
				;--- 後輩 ---
				CASE 12
					;神樹いちか (神樹姓重複回避)
					RESULTS '= @"いちか"
				CASE 23
					;鶯木こはる
					RESULTS '= @"こはる"
				CASE 44
					;笹芽ひよの (後任の生徒会書記)
					RESULTS '= @"ひよの"
			ENDSELECT
		CASE 47
			;双葉みなづき (3-A / オカルト研究部・前生徒会書記)
			SELECTCASE AI
				;--- 最重要（双子の姉） ---
				CASE 46
					;双葉みづき (双子の姉・124回登場・姉だけ呼び捨て)
					RESULTS '= @"みづき"
				;--- 固有愛称 ---
				CASE 51
					;御影かすみ (11回登場・固有愛称)
					RESULTS '= @"かすみん"
				CASE 41
					;悠木ともこ (12回登場・固有愛称)
					RESULTS '= @"ともちゃん"
				CASE 56
					;八壁ひかる (苗字呼び・原作セリフ準拠)
					RESULTS '= @"八壁ちゃん"
			ENDSELECT
		CASE 48
			;四方みつる (3-A / 陸上部部長・生徒会副会長)
			SELECTCASE AI
				;--- 幼馴染・生徒会長 ---
				CASE 45
					;円城寺れいか (幼馴染・52回登場)
					RESULTS '= @"れいか"
				CASE 61
					;鶴海ひまり (生徒会長・75回登場)
					RESULTS '= @"ひまり"
				;--- 後輩（陸上部・生徒会役員） ---
				CASE 41
					;悠木ともこ (生徒会役員・妹分・65回登場)
					RESULTS '= @"ともこ"
				CASE 42
					;榊むつみ (陸上部後輩・60回登場)
					RESULTS '= @"むつみ"
				;--- 同級生・その他親愛 ---
				CASE 49
					;小松ぼたん (同級生・33回登場)
					RESULTS '= @"ぼたん"
				CASE 63
					;八雲ちづる (27回登場)
					RESULTS '= @"ちづるさん"
				CASE 31
					;夢路まりあ (名前呼びさん)
					RESULTS '= @"まりあさん"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめさん"
				CASE 72
					;あんず (呼び捨て)
					RESULTS '= @"あんず"
			ENDSELECT
		CASE 49
			;小松ぼたん (3-A / バスケットボール部)
			SELECTCASE AI
				;--- 同級生（呼び捨て・愛称） ---
				CASE 48
					;四方みつる (29回登場)
					RESULTS '= @"みつる"
				CASE 57
					;岩戸サン (19回登場・サン呼び捨て)
					RESULTS '= @"サン"
				;--- 敬称（〜さん） ---
				CASE 67
					;日滝ましろ (5回登場)
					RESULTS '= @"ましろさん"
				CASE 60
					;瀬川かえで (9回登場)
					RESULTS '= @"瀬川さん"
				CASE 44
					;笹芽ひよの
					RESULTS '= @"笹芽さん"
				CASE 3
					;小野ちよ (お菓子をくれる後輩)
					RESULTS '= @"小野さん"
				CASE 11
					;氷野くるみ
					RESULTS '= @"氷野さん"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめ"
				CASE 72
					;あんず
					RESULTS '= @"あんず"
			ENDSELECT
		CASE 50
			;山條ぎん (3-A / 剣道部部長)
			SELECTCASE AI
				;--- 剣道部後輩・相棒 ---
				CASE 41
					;悠木ともこ (剣道部副部長・18回登場)
					RESULTS '= @"ともこ"
				;--- 同級生・その他 ---
				CASE 52
					;湖南やこ (原作セリフ準拠)
					RESULTS '= @"湖南さん"
				CASE 12
					;神樹いちか (神樹姓重複回避)
					RESULTS '= @"いちか"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめ"
				CASE 72
					;あんず
					RESULTS '= @"あんずさん"
			ENDSELECT
		CASE 51
			;御影かすみ (3-A / 料理研究部部長)
			SELECTCASE AI
				;--- 料理研究部後輩 ---
				CASE 23
					;鶯木こはる (懐いてくる野生児後輩)
					RESULTS '= @"こはるちゃん"
				;--- 同級生 ---
				CASE 46
					;双葉みづき
					RESULTS '= @"みづき"
				CASE 45
					;円城寺れいか
					RESULTS '= @"れいかちゃん"
				CASE 65
					;時国そら
					RESULTS '= @"そら"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめさん"
				CASE 72
					;あんず
					RESULTS '= @"あんずさん"
			ENDSELECT
		CASE 52
			;湖南やこ (3-A / 演劇部部長)
			SELECTCASE AI
				;--- 演劇部後輩（象徴的呼称） ---
				CASE 36
					;遠見ちか (演劇部後輩・象徴的愛称)
					RESULTS '= @"トミコ"
				;--- 同級生 ---
				CASE 63
					;八雲ちづる (親しい同級生・78回登場)
					RESULTS '= @"ちづる"
				CASE 38
					;クー・カロア (外国人名)
					RESULTS '= @"カロア"
				CASE 12
					;神樹いちか (神樹姓重複回避)
					RESULTS '= @"いちか"
				CASE 69
					;神樹はじめ (神樹姓重複回避)
					RESULTS '= @"はじめ"
				CASE 72
					;あんず
					RESULTS '= @"あんず"
			ENDSELECT
"""

new_layer2_code = new_layer2_code.replace('\n', '\r\n').replace('\r\r\n', '\r\n')
new_layer2_bytes = new_layer2_code.encode('cp932')

final_bytes = b_new[:p_c45] + new_layer2_bytes + b_new[p_c54:]

with open(erb_path, 'wb') as f:
    f.write(final_bytes)

print(f"Successfully updated {erb_path}")
print(f"Final file size: {len(final_bytes)} bytes")
