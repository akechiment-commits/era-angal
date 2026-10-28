import os
import re

erb_path = 'ERB/AITE_YOBI_相手呼称.ERB'

with open(erb_path, 'rb') as f:
    raw_b = f.read()

text = raw_b.decode('cp932')

# -------------------------------------------------------------
# 1. Layer 1 Update
# -------------------------------------------------------------
# In Layer 1:
# Remove 51 from `CASE 25, 28, 45, 48, 51, 54, 55, 57, 60, 62, 65, 67, 68, 69`
old_l1_sans = """\t\tCASE 25, 28, 45, 48, 51, 54, 55, 57, 60, 62, 65, 67, 68, 69
			;八朔つゆり/星海こよい/円城寺れいか/四方みつる/御影かすみ/久坂あやめ/伊藤さくら/岩戸サン/瀬川かえで/黒森すず/時国そら/日滝ましろ/深鳥ふみ/神樹はじめ: 苗字+さん付け
			RESULTS '= @"%SUR%さん"
""".replace('\n', '\r\n').replace('\r\r\n', '\r\n')

new_l1_sans = """\t\tCASE 25, 28, 45, 48, 54, 55, 57, 60, 62, 65, 67, 68, 69
			;八朔つゆり/星海こよい/円城寺れいか/四方みつる/久坂あやめ/伊藤さくら/岩戸サン/瀬川かえで/黒森すず/時国そら/日滝ましろ/深鳥ふみ/神樹はじめ: 苗字+さん付け
			RESULTS '= @"%SUR%さん"
		CASE 51
			;御影かすみ: 名前+屋さん（独特の呼称・119回以上登場）
			RESULTS '= @"%CALLNAME:AI%屋さん"
""".replace('\n', '\r\n').replace('\r\r\n', '\r\n')

assert old_l1_sans in text, "old_l1_sans not found!"
text = text.replace(old_l1_sans, new_l1_sans)
print("Layer 1 updated with Kasumi %CALLNAME:AI%屋さん rule.")

# -------------------------------------------------------------
# 2. Layer 2 Update: Miduki, Minaduki, Kasumi, Yako
# -------------------------------------------------------------
# (A) Miduki (46): みなづき -> みなちゃん
text = text.replace(
    '\t\tCASE 46\r\n\t\t\t;双葉みづき (3-A / オカルト研究部・前生徒会書記)\r\n\t\t\tSELECTCASE AI\r\n\t\t\t\t;--- 最重要（双子の妹） ---\r\n\t\t\t\tCASE 47\r\n\t\t\t\t\t;双葉みなづき (双子の妹・110回以上登場)\r\n\t\t\t\t\tRESULTS \'= @"みなづき"',
    '\t\tCASE 46\r\n\t\t\t;双葉みづき (3-A / オカルト研究部・前生徒会書記)\r\n\t\t\tSELECTCASE AI\r\n\t\t\t\t;--- 最重要（双子の妹・274回登場） ---\r\n\t\t\t\tCASE 47\r\n\t\t\t\t\t;双葉みなづき (妹への呼びかけは「みなちゃん」)\r\n\t\t\t\t\tRESULTS \'= @"みなちゃん"'
)

# (B) Minaduki (47): みづき -> お姉ちゃん
text = text.replace(
    '\t\tCASE 47\r\n\t\t\t;双葉みなづき (3-A / オカルト研究部・前生徒会書記)\r\n\t\t\tSELECTCASE AI\r\n\t\t\t\t;--- 最重要（双子の姉） ---\r\n\t\t\t\tCASE 46\r\n\t\t\t\t\t;双葉みづき (双子の姉・124回登場・姉だけ呼び捨て)\r\n\t\t\t\t\tRESULTS \'= @"みづき"',
    '\t\tCASE 47\r\n\t\t\t;双葉みなづき (3-A / オカルト研究部・前生徒会書記)\r\n\t\t\tSELECTCASE AI\r\n\t\t\t\t;--- 最重要（双子の姉） ---\r\n\t\t\t\tCASE 46\r\n\t\t\t\t\t;双葉みづき (姉への呼びかけは「お姉ちゃん」)\r\n\t\t\t\t\tRESULTS \'= @"お姉ちゃん"'
)

# (C) Kasumi (51): Update CASE 51 with 双子屋さん etc.
old_case51 = """\t\tCASE 51
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
""".replace('\n', '\r\n').replace('\r\r\n', '\r\n')

new_case51 = """\t\tCASE 51
			;御影かすみ (3-A / 料理研究部部長)
			SELECTCASE AI
				;--- 双子（象徴的呼称） ---
				CASE 46
					;双葉みづき (双子屋さん)
					RESULTS '= @"双子屋さん"
				CASE 47
					;双葉みなづき (双子屋さん)
					RESULTS '= @"双子屋さん"
				;--- 特別な後輩（ごく稀な愛称） ---
				CASE 23
					;鶯木こはる (普段はこはる屋さん、重大な場面でのみ「こはるちゃん」)
					RESULTS '= @"こはる屋さん"
			ENDSELECT
""".replace('\n', '\r\n').replace('\r\r\n', '\r\n')

assert old_case51 in text, "old_case51 not found!"
text = text.replace(old_case51, new_case51)

# (D) Yako (52): トミコ -> トミ子
text = text.replace(
    'RESULTS \'= @"トミコ"',
    'RESULTS \'= @"トミ子"'
)

# Encode to cp932
b_final = text.encode('cp932')

with open(erb_path, 'wb') as f:
    f.write(b_final)

print("ERB updated successfully with accurate vocatives!")
