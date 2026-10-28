# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932') as f:
    lines = f.readlines()

# Verify markers at target line ranges
assert 'ITEMSALES:86 = 0' in lines[201], f"Line 202 is {lines[201]}"
assert 'ITEMSALES:87 = 0' in lines[208], f"Line 209 is {lines[208]}"
assert 'SIF BOUGHT == 86' in lines[574], f"Line 575 is {lines[574]}"
assert 'IF BOUGHT == 86 || BOUGHT == 87' in lines[581], f"Line 582 is {lines[581]}"
assert 'SIF BOUGHT == 86 && COUNT != TARGET' in lines[624], f"Line 625 is {lines[624]}"
assert 'IF BOUGHT == 86' in lines[1149], f"Line 1150 is {lines[1149]}"
assert 'IF BOUGHT == 87' in lines[1208], f"Line 1209 is {lines[1208]}"

print("All assertion markers verified successfully!")
