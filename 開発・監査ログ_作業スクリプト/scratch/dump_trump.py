# -*- coding: utf-8 -*-
with open('ERB/COMF/COMF390.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

def show_trump(line_no):
    print(f"=== Around line {line_no} ===")
    for idx in range(line_no - 12, line_no + 8):
        print(f"{idx+1}: {lines[idx].strip()}")

show_trump(3218)
show_trump(4976)
show_trump(6734)
show_trump(8492)
show_trump(10250)
