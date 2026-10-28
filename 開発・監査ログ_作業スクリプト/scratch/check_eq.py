# -*- coding: utf-8 -*-
import os, re

files = []
for root, dirs, files_in_dir in os.walk('ERB'):
    for f in files_in_dir:
        if f.endswith(('.ERB', '.erb')):
            files.append(os.path.join(root, f))

# Look for IF or SIF or ELSEIF where an assignment '=' is used instead of '==' or '>=' or '<=' or '!='
single_eq = []
pattern = re.compile(r'^\s*(?:IF|SIF|ELSEIF)\s+.*?[^=!<>+\-*/%&|^]=[^=].*$', re.IGNORECASE)

for path in files:
    with open(path, 'r', encoding='cp932', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            code = line.split(';')[0].strip()
            if not code: continue
            if pattern.match(code):
                # double check it is not == or != etc.
                # strip string literals
                code_no_str = re.sub(r'"[^"]*"', '""', code)
                # check for single '=' not surrounded by other symbols
                m = re.search(r'[^=!<>+\-*/%&|^]=[^=]', code_no_str)
                if m:
                    single_eq.append((path, i, code))

print(f"Single '=' in conditions: {len(single_eq)}")
with open('scratch_single_eq.txt', 'w', encoding='utf-8') as out:
    for p, i, c in single_eq[:50]:
        out.write(f"{p}:{i} -> {c}\n")
