#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix SHOP.ERB shop-toggle number: [120] conflicts with 部活動.
Use [115] instead (COUNT==12 slot is currently CONTINUE/unused).
"""
import re

with open('ERB/SHOP.ERB', 'rb') as f:
    text = f.read().decode('cp932')

# 1) Replace COUNT==12 CONTINUE with shop toggle button
old = "\tELSEIF COUNT == 12\r\n\t\tCONTINUE"
new = (
    "\tELSEIF COUNT == 12\r\n"
    "\t\tIF FLAG:70 == 1\r\n"
    "\t\t\tPRINTLC [115] - ショップを閉じる  \r\n"
    "\t\tELSE\r\n"
    "\t\t\tPRINTLC [115] - ショップ          \r\n"
    "\t\tENDIF"
)
if old in text:
    text = text.replace(old, new)
    print("Fixed COUNT==12 shop button")
else:
    old_lf = old.replace('\r\n', '\n')
    new_lf = new.replace('\r\n', '\n')
    if old_lf in text:
        text = text.replace(old_lf, new_lf)
        print("Fixed COUNT==12 shop button (LF)")
    else:
        print("ERROR: COUNT==12 CONTINUE not found")
        print(repr(text[5600:6000]))

# 2) Replace RESULT==120 shop handler with RESULT==115
old = (
    ";ショップ表示切替\r\n"
    "ELSEIF RESULT == 120\r\n"
    "\tIF FLAG:70 == 1\r\n"
    "\t\tFLAG:70 = 0\r\n"
    "\tELSE\r\n"
    "\t\tFLAG:70 = 1\r\n"
    "\tENDIF\r\n"
    "\tBEGIN SHOP\r\n"
    "\tRETURN 1\r\n"
)
new = (
    ";ショップ表示切替\r\n"
    "ELSEIF RESULT == 115\r\n"
    "\tIF FLAG:70 == 1\r\n"
    "\t\tFLAG:70 = 0\r\n"
    "\tELSE\r\n"
    "\t\tFLAG:70 = 1\r\n"
    "\tENDIF\r\n"
    "\tBEGIN SHOP\r\n"
    "\tRETURN 1\r\n"
)
if old in text:
    text = text.replace(old, new)
    print("Fixed RESULT==115 handler")
else:
    old_lf = old.replace('\r\n', '\n')
    new_lf = new.replace('\r\n', '\n')
    if old_lf in text:
        text = text.replace(old_lf, new_lf)
        print("Fixed RESULT==115 handler (LF)")
    else:
        # Try regex
        text = re.sub(r';ショップ表示切替\r?\nELSEIF RESULT == 120\r?\n',
                      ';ショップ表示切替\r\nELSEIF RESULT == 115\r\n', text)
        print("Fixed RESULT via regex")

with open('ERB/SHOP.ERB', 'wb') as f:
    f.write(text.encode('cp932'))
print("SHOP.ERB updated")
