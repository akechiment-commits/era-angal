import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Definitive Hero call table for all 72 characters
hero_call_table = {
    1: "転校生さん",      # 三善かなえ
    2: "先輩",            # 北川ゆき
    3: "先輩",            # 小野ちよ
    4: "先輩",            # 早川きこ
    5: "せんぱい",        # 桃智あすか
    6: "先輩",            # 藍乃あいか
    7: "お兄ちゃん先輩",  # 高原ちあき
    8: "先輩",            # 丸子みさき
    9: "先輩",            # 月永るか
    10: "おに～さん",     # 木之下ゆゆ
    11: "先輩",           # 氷野くるみ
    12: "先輩",           # 神樹いちか
    13: "転校生殿",       # 羽森つばさ
    14: "転校生しゃん",   # 花音ことり
    15: "おに～さん",     # 長町やえ
    16: "先輩",           # 大虎いさみ
    17: "先輩",           # 小鳩あずさ
    18: "先輩",           # 熊沢ひめの
    19: "先輩",           # 猫塚みけ
    20: "先輩",           # 藤猪しずく
    21: "先輩",           # 雉子すみれ
    22: "先輩",           # 鯱いかり
    23: "お兄ちゃん先輩", # 鶯木こはる
    24: "転校生くん",     # 三波なつみ
    25: "転校生くん",     # 八朔つゆり
    26: "あんた",         # 堀田さあや
    27: "転校生",         # 夏野ゆり
    28: "転校生くん",     # 星海こよい
    29: "転校生くん",     # 春風なな
    30: "ダーリン",       # 長居ゆう
    31: "転校生さん",     # 夢路まりあ
    32: "あんた",         # 安条まい
    33: "転校生",         # 柊るな
    34: "転校生くん",     # 桐島かいり
    35: "転校生",         # 梅園かな
    36: "ヘルプマン",     # 遠見ちか
    37: "転校生",         # 龍泉寺レンレン
    38: "転校生",         # クー・カロア
    39: "転校生",         # 冴木もも
    40: "転校生くん",     # 夜霧はやて
    41: "転校生さん",     # 悠木ともこ
    42: "転校生",         # 榊むつみ
    43: "転校生くん",     # 砂賀みどり
    44: "転校生さん",     # 笹芽ひよの
    45: "転校生くん",     # 円城寺れいか
    46: "転校生",         # 双葉みづき
    47: "転校生くん",     # 双葉みなづき
    48: "転校生くん",     # 四方みつる
    49: "転校生くん",     # 小松ぼたん
    50: "転校生くん",     # 山條ぎん
    51: "転校生さん",     # 御影かすみ
    52: "アンタ",         # 湖南やこ
    53: "転校生さん",     # 花丘まり
    54: "転校生くん",     # 久坂あやめ
    55: "転校生さん",     # 伊藤さくら
    56: "転校生",         # 八壁ひかる
    57: "転校生くん",     # 岩戸サン
    58: "転校生くん",     # 天宮るり
    59: "転校生くん",     # 水嶌うしお
    60: "転校生",         # 瀬川かえで
    61: "転校生くん",     # 鶴海ひまり
    62: "キミ",           # 黒森すず
    63: "転校生くん",     # 八雲ちづる
    64: "少年",           # 峰山しおん
    65: "転校生さん",     # 時国そら
    66: "転校生ちゃん",   # 曽根セイラ
    67: "転校生くん",     # 日滝ましろ
    68: "転校生",         # 深鳥ふみ
    69: "転校生くん",     # 神樹はじめ
    70: "転校生くん",     # 神無月ほとり
    71: "転校生くん",     # 棗ひびき
    72: "あんた",         # あんず
}

# 1. Read ERB
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

text = raw.decode('cp932')

# (A) Fix GET_CHARA_GRADE: add CASE 0 -> RETURNF 2
target_grade = "@GET_CHARA_GRADE, ARG\r\n#FUNCTION\r\nSELECTCASE ARG\r\n\t; 1年生"
repl_grade = "@GET_CHARA_GRADE, ARG\r\n#FUNCTION\r\nSELECTCASE ARG\r\n\t; 主人公 (ID 0: 転校生・2年生扱い)\r\n\tCASE 0\r\n\t\tRETURNF 2\r\n\t; 1年生"
assert target_grade in text, "target_grade not found"
text = text.replace(target_grade, repl_grade, 1)

# (B) Fix 3-C group (64 to 71) CASE 72 overrides:
# In 64: remove CASE 72: 少年
text = re.sub(
    r'(\t\tCASE 64[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず \(原作直接呼びかけ「少年」多数！\)\r?\n\t\t\t\t\tRESULTS \'= @"少年"\r?\n',
    r'\1',
    text
)

# In 65: remove CASE 72: 転校生さん
text = re.sub(
    r'(\t\tCASE 65[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず\r?\n\t\t\t\t\tRESULTS \'= @"転校生さん"\r?\n',
    r'\1',
    text
)

# In 67: remove CASE 72: 転校生くん
text = re.sub(
    r'(\t\tCASE 67[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず \(85回登場！\)\r?\n\t\t\t\t\tRESULTS \'= @"転校生くん"\r?\n',
    r'\1',
    text
)

# In 68: remove CASE 72: 転校生
text = re.sub(
    r'(\t\tCASE 68[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず \(28回登場・呼び捨て\)\r?\n\t\t\t\t\tRESULTS \'= @"転校生"\r?\n',
    r'\1',
    text
)

# In 69: remove CASE 72: 転校生くん
text = re.sub(
    r'(\t\tCASE 69[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず \(98回登場！\)\r?\n\t\t\t\t\tRESULTS \'= @"転校生くん"\r?\n',
    r'\1',
    text
)

# In 70: remove CASE 72: 転校生くん
text = re.sub(
    r'(\t\tCASE 70[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず \(94回登場！\)\r?\n\t\t\t\t\tRESULTS \'= @"転校生くん"\r?\n',
    r'\1',
    text
)

# In 71: remove CASE 72: 転校生くん
text = re.sub(
    r'(\t\tCASE 71[\s\S]*?SELECTCASE AI[\s\S]*?)\t\t\t\t;--- 転校生 ---\r?\n\t\t\t\tCASE 72\r?\n\t\t\t\t\t;あんず \(57回登場！\)\r?\n\t\t\t\t\tRESULTS \'= @"転校生くん"\r?\n',
    r'\1',
    text
)

# In 52 (やこ): CASE 72 should be "アンジー"
text = re.sub(
    r'(\t\tCASE 52[\s\S]*?CASE 72\r?\n\t\t\t\t\t;あんず\r?\n\t\t\t\t\tRESULTS \'= @")あんず(")',
    r'\g<1>アンジー\2',
    text
)

# In 62 (すず): CASE 72 should be "あんずちゃん"
text = re.sub(
    r'(\t\tCASE 62[\s\S]*?CASE 72\r?\n\t\t\t\t\t;あんず[^\r\n]*\r?\n\t\t\t\t\tRESULTS \'= @")アジュー(")',
    r'\g<1>あんずちゃん\2',
    text
)

# In 50 (ぎん): CASE 72 should be "アンジー"
text = re.sub(
    r'(\t\tCASE 50[\s\S]*?CASE 72\r?\n\t\t\t\t\t;あんず\r?\n\t\t\t\t\tRESULTS \'= @")あんずさん(")',
    r'\g<1>アンジー\2',
    text
)

# (C) Now inject CASE 0 (Hero call) into each SP's SELECTCASE AI block (SP 1 to 72)
# Pattern: ^\t\tCASE <sp>\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI\r?\n
for sp in range(1, 73):
    hero_call = hero_call_table[sp]
    sp_header_pattern = rf'(^\t\tCASE {sp}\r?\n\t\t\t;[^\r\n]+\r?\n\t\t\tSELECTCASE AI\r?\n)'
    # check if already has CASE 0
    # injection block
    injection = f"\t\t\t\t;--- 主人公 (転校生) ---\r\n\t\t\t\tCASE 0\r\n\t\t\t\t\tRESULTS '= @\"{hero_call}\"\r\n"
    
    # replace using regex
    def make_repl(inj):
        return lambda m: m.group(1) + inj
    
    new_text, count = re.subn(sp_header_pattern, make_repl(injection), text, count=1, flags=re.MULTILINE)
    assert count == 1, f"Failed to inject CASE 0 into SP {sp}"
    text = new_text

# (D) Verify and write back
new_raw = text.encode('cp932')
assert b'\r\r\n' not in new_raw, "Corrupted CRLF detected"
assert b'\n' not in new_raw.replace(b'\r\n', b''), "Bare LF detected"

with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(new_raw)

print("Successfully injected CASE 0 into all 72 characters and fixed CASE 72 anzu overrides!")
