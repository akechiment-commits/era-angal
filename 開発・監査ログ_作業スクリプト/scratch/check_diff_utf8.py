# -*- coding: utf-8 -*-
import glob

f_source = glob.glob('ERB/*SOURCE*')[0]
f_event_m = glob.glob('ERB/*EVENT_M*')[1]

with open('scratch_diff_check.txt', 'w', encoding='utf-8') as out:
    out.write("=== SOURCE.ERB (803-810) ===\n")
    with open(f_source, 'r', encoding='cp932') as fp:
        lines = fp.readlines()
        for i in range(802, 810):
            out.write(f"{i+1}: {lines[i]}")

    out.write("\n=== EVENT_M.ERB (583-611) ===\n")
    with open(f_event_m, 'r', encoding='cp932') as fp:
        lines = fp.readlines()
        for i in range(582, 611):
            out.write(f"{i+1}: {lines[i]}")
