# -*- coding: utf-8 -*-
import sys, re

# AITE_YOBI_相手呼称.ERB の読み込み（バイナリモード）
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

text = raw.decode('cp932')

# 1. 第1階層の確認と置換
# CASE 26, 33, 46 -> 26 を分離
# CASE 24, 59, 61, 63 -> 24 を分離
# CASE 25 を 苗字+さん に追加

print("Checking Tier 1 targets...")
assert "CASE 26, 33, 46" in text
assert "CASE 24, 59, 61, 63" in text
assert "CASE 35, 43, 44, 45, 47, 48, 49, 52, 54, 55, 57, 60, 62, 65, 67, 68, 69" in text

print("Tier 1 targets verified!")

# 2. 第2階層の確認
# CASE 24 ... CASE 25 ... CASE 27 の範囲を特定
case24_pos = text.find("\t\tCASE 24\r\n\t\t\t;三波なつみ")
if case24_pos == -1:
    # コメントが文字化けしている可能性があるので正規表現で探す
    m = re.search(r'(\t\tCASE 24\r\n.*?\t\tCASE 27\r\n)', text, re.DOTALL)
    if m:
        print("Found Case 24-25 block via regex!")
        print(m.group(1)[:200])
    else:
        print("Could not find Case 24-25 block!")
else:
    print("Found Case 24 pos directly!")
