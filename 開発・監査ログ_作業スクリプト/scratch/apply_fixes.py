# -*- coding: utf-8 -*-
import glob

# 1. Update ERB/SOURCE_ソース計算・口上呼び出し.ERB
f_source = glob.glob('ERB/*SOURCE*')[0]
with open(f_source, 'r', encoding='cp932') as fp:
    src_lines = fp.readlines()

for i, line in enumerate(src_lines):
    if line.strip() == 'A = UP:0 + UP:1 + UP:2 + UP:17':
        print(f"Found line in SOURCE: line {i+1}")
        src_lines[i] = '\tA = UP:0 + UP:1 + UP:2 + UP:14\r\n'
    elif line.strip() == 'SIF UP:24 > 1000':
        src_lines[i] = '\tSIF UP:18 > 1000\r\n'
    elif line.strip() == 'A += UP:24 / 1000':
        src_lines[i] = '\t\tA += UP:18 / 1000\r\n'

with open(f_source, 'wb') as fp:
    fp.write("".join(src_lines).replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
print("Updated SOURCE.ERB")

# 2. Update ERB/EVENT_M_調教メッセージ.ERB
f_event_m = glob.glob('ERB/*EVENT_M*')[1]
with open(f_event_m, 'r', encoding='cp932') as fp:
    m_lines = fp.readlines()

for i, line in enumerate(m_lines):
    line_no = i + 1
    if 580 <= line_no <= 612:
        if 'ゆっくりと胸のふくらみを撫でた…' in line:
            print(f"Fixing line {line_no}: ゆっくりと胸のふくらみ")
            m_lines[i] = line.replace('ゆっくりと胸のふくらみを撫でた…', '胸のふくらみを、ゆっくりと撫でた…')
        elif '手のひらで、そっと胸を包んだ…' in line:
            print(f"Fixing line {line_no}: 手のひらで、そっと胸を包んだ")
            m_lines[i] = line.replace('手のひらで、そっと胸を包んだ…', '胸を、手のひらでそっと包み込んだ…')
        elif '先端をかすめるように撫でると、くすぐったそうに肩をすくめた…' in line:
            print(f"Fixing line {line_no}: 先端をかすめるように")
            m_lines[i] = line.replace('先端をかすめるように撫でると、くすぐったそうに肩をすくめた…', '胸の先端をかすめるように撫でると、くすぐったそうに肩をすくめた…')
        elif 'やわらかな胸を包み込むように揉むと、くすぐったそうに身じろぎした…' in line:
            print(f"Fixing line {line_no}: やわらかな胸を包み込む")
            m_lines[i] = line.replace('やわらかな胸を包み込むように揉むと、くすぐったそうに身じろぎした…', '胸を包み込むように揉むと、くすぐったそうに身じろぎした…')
        elif 'やわらかな胸をそっと包み込んだ…' in line:
            print(f"Fixing line {line_no}: やわらかな胸をそっと包み込んだ")
            m_lines[i] = line.replace('やわらかな胸をそっと包み込んだ…', '胸をそっと包み込んだ…')

with open(f_event_m, 'wb') as fp:
    fp.write("".join(m_lines).replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
print("Updated EVENT_M.ERB")
