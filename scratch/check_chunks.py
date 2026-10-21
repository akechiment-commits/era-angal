# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932', errors='strict') as f:
    lines = f.readlines()

def check_match(start_line, end_line, name):
    print(f"--- {name} (lines {start_line}-{end_line}) ---")
    chunk = "".join(lines[start_line-1:end_line])
    print(repr(chunk[:100]))

check_match(201, 216, "Part A")
check_match(575, 578, "Part B")
check_match(582, 586, "Part C")
check_match(625, 628, "Part D")
check_match(1149, 1264, "Part E")
