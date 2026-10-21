import pathlib
import re

ROOT = pathlib.Path('.')
char_dir = ROOT / 'ERB' / 'CHAR'

broken_quotes = []

for p in char_dir.glob('CHAR_*.ERB'):
    text = p.read_bytes().decode('cp932')
    lines = text.splitlines()
    in_quote = False
    quote_start_line = 0
    
    for idx, line in enumerate(lines, 1):
        clean = line.split(';')[0].strip()
        if not clean:
            continue
        if clean.startswith('@'):
            if in_quote:
                broken_quotes.append((p.name, quote_start_line, 'Unclosed quote before new function', lines[quote_start_line-1]))
                in_quote = False
            continue
            
        # Count 「 and 」 in PRINT statements
        if re.match(r'^PRINTFORM[A-Z]*\s+', clean):
            # Check quotes in print body
            txt = re.sub(r'^PRINTFORM[A-Z]*\s+', '', clean)
            c_open = txt.count('「')
            c_close = txt.count('」')
            
            if in_quote:
                if c_close > c_open:
                    in_quote = False
                elif c_close == c_open and c_open > 0:
                    # closed and opened again
                    in_quote = True
            else:
                if c_open > c_close:
                    in_quote = True
                    quote_start_line = idx
                elif c_close > c_open:
                    broken_quotes.append((p.name, idx, 'Close quote without open quote', clean))

    if in_quote:
        broken_quotes.append((p.name, quote_start_line, 'Unclosed quote at EOF', lines[quote_start_line-1]))

print(f'Total broken dialogue quotes: {len(broken_quotes)}')
for name, idx, reason, line in broken_quotes[:30]:
    print(f'  {name}:{idx} [{reason}] -> {line}')
