# -*- coding: utf-8 -*-
with open('ERB/SOURCE_ソース計算・口上呼び出し.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

def inspect_func(func_name):
    inside = False
    print(f"=== {func_name} ===")
    for i, line in enumerate(lines, 1):
        if line.startswith('@' + func_name):
            inside = True
        elif inside and line.startswith('@'):
            break
        if inside:
            print(f"{i}: {line.strip()}")

inspect_func('LOVE_JUICE')
inspect_func('ORGASM_CHECK')
inspect_func('CALC_GAUGE')
