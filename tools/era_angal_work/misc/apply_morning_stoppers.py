# -*- coding: utf-8 -*-
import sys, os, re

filepath = 'ERB/EVENT_MORNING_朝のイベント.ERB'
with open(filepath, 'rb') as f:
    text = f.read().decode('cp932')

# Helper to do regex substitution within a specific function
def sub_in_func(text, func_name, pattern, replacement, expected_count=1):
    m = re.search(r'(@' + re.escape(func_name) + r'\b[\s\S]*?)(?=\r?\n@[A-Za-z0-9_]|\Z)', text)
    if not m:
        raise Exception(f'Function {func_name} not found!')
    func_text = m.group(1)
    matches = list(re.finditer(pattern, func_text))
    if len(matches) != expected_count:
        raise Exception(f'In {func_name}, expected {expected_count} matches for {pattern}, found {len(matches)}!')
    new_func_text = re.sub(pattern, replacement, func_text)
    return text[:m.start(1)] + new_func_text + text[m.end(1):]

# 1. PI
text = sub_in_func(text, 'EVENT_NEWDAY_PI',
    r'A\s*=\s*2\s*\+\s*\(ABL:6\s*/\s*6\)\s*\+\s*\(ABL:11\s*/\s*4\)',
    'A = 2 + (MIN(ABL:6, 10) / 6) + (MIN(ABL:11, 10) / 4) + SQRT(MAX(ABL:6 - 10, 0)) + SQRT(MAX(ABL:11 - 10, 0))', 1)

pi_stopper = (
    '\t;ソフトキャップ補正（朝の行為回数ストッパー）\r\n'
    '\tIF TALENT:76 || TALENT:85\t; 【淫乱】または【恋慕】\r\n'
    '\t\tIF A > 8\r\n'
    '\t\t\tA = 8 + SQRT((A - 8) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 12\r\n'
    '\t\t\tA = 12\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 5\r\n'
    '\t\t\tA = 5 + SQRT((A - 5) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 8\r\n'
    '\t\t\tA = 8\r\n'
    '\tENDIF\r\n'
    '\tA:1 = A'
)
text = sub_in_func(text, 'EVENT_NEWDAY_PI',
    r'A:1\s*=\s*A\r?\n\t*SIF A >= 64\r?\n\t*A = 64',
    pi_stopper, 1)

# 2. SEX (2 branches)
text = sub_in_func(text, 'EVENT_NEWDAY_SEX',
    r'A\s*=\s*3\s*\+\s*\(ABL:1\s*/\s*6\)\s*\+\s*\(ABL:6\s*/\s*6\)',
    'A = 3 + (MIN(ABL:1, 10) / 6) + (MIN(ABL:6, 10) / 6) + SQRT(MAX(ABL:1 - 10, 0)) + SQRT(MAX(ABL:6 - 10, 0))', 2)

sex_stopper = (
    '\t\t;ソフトキャップ補正（朝の行為回数ストッパー）\r\n'
    '\t\tIF TALENT:76 || TALENT:85\t; 【淫乱】または【恋慕】\r\n'
    '\t\t\tIF A > 8\r\n'
    '\t\t\t\tA = 8 + SQRT((A - 8) * 2)\r\n'
    '\t\t\tENDIF\r\n'
    '\t\t\tSIF A > 12\r\n'
    '\t\t\t\tA = 12\r\n'
    '\t\tELSE\r\n'
    '\t\t\tIF A > 5\r\n'
    '\t\t\t\tA = 5 + SQRT((A - 5) * 2)\r\n'
    '\t\t\tENDIF\r\n'
    '\t\t\tSIF A > 8\r\n'
    '\t\t\t\tA = 8\r\n'
    '\t\tENDIF\r\n'
    '\t\tA:1 = A'
)
text = sub_in_func(text, 'EVENT_NEWDAY_SEX',
    r'A:1\s*=\s*A\r?\n\t*SIF A >= 9\r?\n\t*A = 9',
    sex_stopper, 2)

# 3. YOME (2 branches)
text = sub_in_func(text, 'EVENT_NEWDAY_YOME',
    r'A\s*=\s*2\s*\+\s*\(ABL:6\s*/\s*6\)\s*\+\s*\(ABL:7\s*/\s*6\)',
    'A = 2 + (MIN(ABL:6, 10) / 6) + (MIN(ABL:7, 10) / 6) + SQRT(MAX(ABL:6 - 10, 0)) + SQRT(MAX(ABL:7 - 10, 0))', 2)

text = sub_in_func(text, 'EVENT_NEWDAY_YOME',
    r'A:1\s*=\s*A\r?\n\t*SIF A >= 9\r?\n\t*A = 9',
    sex_stopper, 1)

yome_branch2_stopper = (
    '\t\t;ソフトキャップ補正（朝の行為回数ストッパー）\r\n'
    '\t\tIF TALENT:76 || TALENT:85\t; 【淫乱】または【恋慕】\r\n'
    '\t\t\tSIF A > 6\r\n'
    '\t\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\t\tSIF A > 9\r\n'
    '\t\t\t\tA = 9\r\n'
    '\t\t\tSIF B > 6\r\n'
    '\t\t\t\tB = 6 + SQRT((B - 6) * 2)\r\n'
    '\t\t\tSIF B > 9\r\n'
    '\t\t\t\tB = 9\r\n'
    '\t\tELSE\r\n'
    '\t\t\tSIF A > 4\r\n'
    '\t\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\t\tSIF A > 6\r\n'
    '\t\t\t\tA = 6\r\n'
    '\t\t\tSIF B > 4\r\n'
    '\t\t\t\tB = 4 + SQRT((B - 4) * 2)\r\n'
    '\t\t\tSIF B > 6\r\n'
    '\t\t\t\tB = 6\r\n'
    '\t\tENDIF\r\n'
    '\t\tIF A > 0 || B > 0\r\n'
    '\t\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_YOME',
    r'\t\tIF A > 0 \|\| B > 0\r?\n\t\t\tDRAWLINE',
    yome_branch2_stopper, 1)

# 4. KISS
text = sub_in_func(text, 'EVENT_NEWDAY_KISS',
    r'A\s*=\s*\(ABL:6\s*/\s*6\)\s*\+\s*\(ABL:0\s*/\s*6\)',
    'A = (MIN(ABL:6, 10) / 6) + (MIN(ABL:0, 10) / 6) + SQRT(MAX(ABL:6 - 10, 0)) + SQRT(MAX(ABL:0 - 10, 0))', 1)

kiss_stopper = (
    '\t;ソフトキャップ補正（朝のキス回数ストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89 || TALENT:155\t; 【親愛】【相愛】【キス魔】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_KISS',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    kiss_stopper, 1)

# 5. FEMALE (2 branches)
text = sub_in_func(text, 'EVENT_NEWDAY_FEMALE',
    r'B\s*=\s*3\s*\+\s*\(ABL:1\s*/\s*6\)\s*\+\s*\(ABL:15\s*/\s*3\)',
    'B = 3 + (MIN(ABL:1, 10) / 6) + (MIN(ABL:15, 10) / 3) + SQRT(MAX(ABL:1 - 10, 0)) + SQRT(MAX(ABL:15 - 10, 0))', 2)

female_stopper = (
    '\t\t;ソフトキャップ補正（朝の行為回数ストッパー）\r\n'
    '\t\tIF TALENT:76 || TALENT:83\t; 【淫乱】または【サド】\r\n'
    '\t\t\tIF B > 8\r\n'
    '\t\t\t\tB = 8 + SQRT((B - 8) * 2)\r\n'
    '\t\t\tENDIF\r\n'
    '\t\t\tSIF B > 12\r\n'
    '\t\t\t\tB = 12\r\n'
    '\t\tELSE\r\n'
    '\t\t\tIF B > 5\r\n'
    '\t\t\t\tB = 5 + SQRT((B - 5) * 2)\r\n'
    '\t\t\tENDIF\r\n'
    '\t\t\tSIF B > 8\r\n'
    '\t\t\t\tB = 8\r\n'
    '\t\tENDIF\r\n'
    '\t\tIF B > 0\r\n'
    '\t\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_FEMALE',
    r'\t\tIF B > 0\r?\n\t\t\tDRAWLINE',
    female_stopper, 2)

# 6. F (2 branches)
text = sub_in_func(text, 'EVENT_NEWDAY_F',
    r'A\s*=\s*3\s*\+\s*\(ABL:11\s*/\s*2\)',
    'A = 3 + (MIN(ABL:11, 10) / 2) + SQRT(MAX(ABL:11 - 10, 0))', 1)
text = sub_in_func(text, 'EVENT_NEWDAY_F',
    r'A\s*=\s*3\s*\+\s*\(ABL:12\s*/\s*2\)',
    'A = 3 + (MIN(ABL:12, 10) / 2) + SQRT(MAX(ABL:12 - 10, 0))', 1)

f_stopper = (
    '\t\t;ソフトキャップ補正（朝のフェラ回数ストッパー）\r\n'
    '\t\tIF TALENT:76 || TALENT:85\t; 【淫乱】または【恋慕】\r\n'
    '\t\t\tIF A > 8\r\n'
    '\t\t\t\tA = 8 + SQRT((A - 8) * 2)\r\n'
    '\t\t\tENDIF\r\n'
    '\t\t\tSIF A > 12\r\n'
    '\t\t\t\tA = 12\r\n'
    '\t\tELSE\r\n'
    '\t\t\tIF A > 5\r\n'
    '\t\t\t\tA = 5 + SQRT((A - 5) * 2)\r\n'
    '\t\t\tENDIF\r\n'
    '\t\t\tSIF A > 8\r\n'
    '\t\t\t\tA = 8\r\n'
    '\t\tENDIF\r\n'
    '\t\tIF A > 0\r\n'
    '\t\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_F',
    r'\t\tIF A > 0\r?\n\t\t\tDRAWLINE',
    f_stopper, 2)

# 7. SOINE
text = sub_in_func(text, 'EVENT_NEWDAY_SOINE',
    r'A\s*=\s*4\s*\+\s*\(ABL:0\s*/\s*2\)',
    'A = 4 + (MIN(ABL:0, 10) / 2) + SQRT(MAX(ABL:0 - 10, 0))', 1)

soine_stopper = (
    '\t;ソフトキャップ補正（朝の添い寝ストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89\t; 【親愛】または【相愛】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_SOINE',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    soine_stopper, 1)

# 8. NEGAO
text = sub_in_func(text, 'EVENT_NEWDAY_NEGAO',
    r'B\s*=\s*4\s*\+\s*\(ABL:0\s*/\s*2\)',
    'B = 4 + (MIN(ABL:0, 10) / 2) + SQRT(MAX(ABL:0 - 10, 0))', 1)

negao_stopper = (
    '\t;ソフトキャップ補正（朝の寝顔ストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89\t; 【親愛】または【相愛】\r\n'
    '\t\tIF B > 6\r\n'
    '\t\t\tB = 6 + SQRT((B - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF B > 10\r\n'
    '\t\t\tB = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF B > 4\r\n'
    '\t\t\tB = 4 + SQRT((B - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF B > 7\r\n'
    '\t\t\tB = 7\r\n'
    '\tENDIF\r\n'
    '\tIF B > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_NEGAO',
    r'\tIF B > 0\r?\n\t\tDRAWLINE',
    negao_stopper, 1)

# 9. OTO
text = sub_in_func(text, 'EVENT_NEWDAY_OTO',
    r'B\s*=\s*3\s*\+\s*\(ABL:15\s*/\s*2\)',
    'B = 3 + (MIN(ABL:15, 10) / 2) + SQRT(MAX(ABL:15 - 10, 0))', 1)

oto_stopper = (
    '\t;ソフトキャップ補正（男嫌い寝込み襲いストッパー）\r\n'
    '\tIF TALENT:83\t; 【サド】\r\n'
    '\t\tIF B > 6\r\n'
    '\t\t\tB = 6 + SQRT((B - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF B > 10\r\n'
    '\t\t\tB = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF B > 4\r\n'
    '\t\t\tB = 4 + SQRT((B - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF B > 7\r\n'
    '\t\t\tB = 7\r\n'
    '\tENDIF\r\n'
    '\tIF B > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_OTO',
    r'\tIF B > 0\r?\n\t\tDRAWLINE',
    oto_stopper, 1)

# 10. TE
text = sub_in_func(text, 'EVENT_NEWDAY_TE',
    r'A\s*=\s*1\s*\+\s*\(ABL:0\s*/\s*5\)\s*\+\s*\(ABL:1\s*/\s*5\)',
    'A = 1 + (MIN(ABL:0, 10) / 5) + (MIN(ABL:1, 10) / 5) + SQRT(MAX(ABL:0 - 10, 0)) + SQRT(MAX(ABL:1 - 10, 0))', 1)

te_stopper = (
    '\t;ソフトキャップ補正（朝の手繋ぎストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89\t; 【親愛】または【相愛】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_TE',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    te_stopper, 1)

# 11. MIMI
text = sub_in_func(text, 'EVENT_NEWDAY_MIMI',
    r'A\s*=\s*\(ABL:0\s*/\s*5\)\s*\+\s*\(ABL:6\s*/\s*5\)',
    'A = (MIN(ABL:0, 10) / 5) + (MIN(ABL:6, 10) / 5) + SQRT(MAX(ABL:0 - 10, 0)) + SQRT(MAX(ABL:6 - 10, 0))', 1)

mimi_stopper = (
    '\t;ソフトキャップ補正（朝の耳元囁きストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89\t; 【親愛】または【相愛】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_MIMI',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    mimi_stopper, 1)

# 12. NORI
text = sub_in_func(text, 'EVENT_NEWDAY_NORI',
    r'A\s*=\s*\(ABL:0\s*/\s*5\)\s*\+\s*\(ABL:1\s*/\s*5\)',
    'A = (MIN(ABL:0, 10) / 5) + (MIN(ABL:1, 10) / 5) + SQRT(MAX(ABL:0 - 10, 0)) + SQRT(MAX(ABL:1 - 10, 0))', 1)

nori_stopper = (
    '\t;ソフトキャップ補正（朝の乗っかりストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89 || TALENT:83\t; 【親愛】【相愛】【サド】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_NORI',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    nori_stopper, 1)

# 13. KUBISUJI
text = sub_in_func(text, 'EVENT_NEWDAY_KUBISUJI',
    r'A\s*=\s*\(ABL:0\s*/\s*5\)\s*\+\s*\(ABL:1\s*/\s*5\)',
    'A = (MIN(ABL:0, 10) / 5) + (MIN(ABL:1, 10) / 5) + SQRT(MAX(ABL:0 - 10, 0)) + SQRT(MAX(ABL:1 - 10, 0))', 1)

kubisuji_stopper = (
    '\t;ソフトキャップ補正（朝の首筋キスストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89 || TALENT:83\t; 【親愛】【相愛】【サド】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_KUBISUJI',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    kubisuji_stopper, 1)

# 14. SURI
text = sub_in_func(text, 'EVENT_NEWDAY_SURI',
    r'A\s*=\s*\(ABL:0\s*/\s*5\)\s*\+\s*\(ABL:1\s*/\s*4\)',
    'A = (MIN(ABL:0, 10) / 5) + (MIN(ABL:1, 10) / 4) + SQRT(MAX(ABL:0 - 10, 0)) + SQRT(MAX(ABL:1 - 10, 0))', 1)

suri_stopper = (
    '\t;ソフトキャップ補正（朝のすりすりストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89 || TALENT:76\t; 【親愛】【相愛】【淫乱】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_SURI',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    suri_stopper, 1)

# 15. ASHIKOSHI
text = sub_in_func(text, 'EVENT_NEWDAY_ASHIKOSHI',
    r'A\s*=\s*\(ABL:0\s*/\s*5\)\s*\+\s*\(ABL:1\s*/\s*4\)',
    'A = (MIN(ABL:0, 10) / 5) + (MIN(ABL:1, 10) / 4) + SQRT(MAX(ABL:0 - 10, 0)) + SQRT(MAX(ABL:1 - 10, 0))', 1)

ashikoshi_stopper = (
    '\t;ソフトキャップ補正（朝の足腰擦り付けストッパー）\r\n'
    '\tIF TALENT:88 || TALENT:89 || TALENT:76 || TALENT:83\t; 【親愛】【相愛】【淫乱】【サド】\r\n'
    '\t\tIF A > 6\r\n'
    '\t\t\tA = 6 + SQRT((A - 6) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 10\r\n'
    '\t\t\tA = 10\r\n'
    '\tELSE\r\n'
    '\t\tIF A > 4\r\n'
    '\t\t\tA = 4 + SQRT((A - 4) * 2)\r\n'
    '\t\tENDIF\r\n'
    '\t\tSIF A > 7\r\n'
    '\t\t\tA = 7\r\n'
    '\tENDIF\r\n'
    '\tIF A > 0\r\n'
    '\t\tDRAWLINE'
)
text = sub_in_func(text, 'EVENT_NEWDAY_ASHIKOSHI',
    r'\tIF A > 0\r?\n\t\tDRAWLINE',
    ashikoshi_stopper, 1)

with open(filepath, 'wb') as f:
    f.write(text.encode('cp932'))

print('Successfully applied all 15 morning event stoppers!')
