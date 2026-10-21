# -*- coding: utf-8 -*-
import os

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

sif_issues = []

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            code = line.split(';')[0].strip()
            if code.upper().startswith('SIF'):
                # Check next non-empty, non-comment line
                # In Emuera: SIF affects the NEXT executable statement.
                # If there are empty lines or comment lines in between,
                # the programmer might not realize SIF affects a distant line!
                # Even worse: what if the next executable statement is an IF, REPEAT, FOR, SIF, ELSE, ELSEIF, ENDIF?
                found_next = False
                for j in range(i + 1, min(len(lines), i + 10)):
                    next_code = lines[j].split(';')[0].strip()
                    if next_code:
                        first_word = next_code.split()[0].upper()
                        if first_word in ['IF', 'SIF', 'REPEAT', 'FOR', 'WHILE', 'DO', 'ELSE', 'ELSEIF', 'ENDIF', 'REND', 'NEXT', 'WEND', 'LOOP']:
                            sif_issues.append((path, i + 1, j + 1, line.strip(), lines[j].strip()))
                        break

print(f"SIF followed by block statement: {len(sif_issues)}")
with open('scratch_sif_issues.txt', 'w', encoding='utf-8') as out:
    for p, l1, l2, c1, c2 in sif_issues:
        out.write(f"{p}:{l1} (line {l2}) ->\n  SIF:   {c1}\n  BLOCK: {c2}\n\n")
