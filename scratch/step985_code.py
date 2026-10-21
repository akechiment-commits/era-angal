# -*- coding: utf-8 -*-
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    text = f.read().decode('cp932')

# 1. 既定ルールの置換
old_default = """\t\tCASE 1, 2, 3, 4, 6, 8, 9, 12
\t\t\t;1年生標準既定: 上級生(2年・3年)は「苗字+先輩」、同級生(1年)は「苗字+さん」
\t\t\tIF GET_CHARA_GRADE(AI) > 1
\t\t\t\tRESULTS '= @"%SUR%先輩"
\t\t\tELSE
\t\t\t\tRESULTS '= @"%SUR%さん"
\t\t\tENDIF"""

new_default = """\t\tCASE 1, 2, 3, 4, 6, 8, 9, 12, 13
\t\t\t;1年生標準既定: 上級生(2年・3年)は「苗字+先輩」、同級生(1年)は「苗字+さん」
\t\t\tIF GET_CHARA_GRADE(AI) > 1
\t\t\t\tRESULTS '= @"%SUR%先輩"
\t\t\tELSE
\t\t\t\tRESULTS '= @"%SUR%さん"
\t\t\tENDIF"""

text_clean = text.replace('\r\n', '\n')
old_default_clean = old_default.replace('\r\n', '\n')
new_default_clean = new_default.replace('\r\n', '\n')

if old_default_clean in text_clean:
    text_clean = text_clean.replace(old_default_clean, new_default_clean)
    print('Default rules updated.')
else:
    print('Failed to find old default rules.')

# 2. 特別呼称の置換 (CASE 13 と CASE 14)
lines = text_clean.split('\n')

idx_sp_case13 = -1
for i in range(len(lines)):
    if lines[i] == '\t\tCASE 13':
        idx_sp_case13 = i
        break

idx_sp_case15 = -1
for i in range(idx_sp_case13, len(lines)):
    if lines[i] == '\t\tCASE 15':
        idx_sp_case15 = i
        break

print(f'SP CASE 13 starts at line {idx_sp_case13 + 1}, SP CASE 15 starts at line {idx_sp_case15 + 1}')

new_cases_13_14 = """\t\tCASE 13
\t\t\t;羽森つばさ (特別呼称)
\t\t\tSELECTCASE AI
\t\t\t\tCASE 8
\t\t\t\t\tRESULTS '= @"マルちゃん殿"
\t\t\t\tCASE 14
\t\t\t\t\t;花音ことり (唯一無二の相方)
\t\t\t\t\tRESULTS '= @"ことりん"
\t\t\t\tCASE 19
\t\t\t\t\tRESULTS '= @"猫塚殿"
\t\t\t\tCASE 26
\t\t\t\t\tRESULTS '= @"堀田殿"
\t\t\t\tCASE 30
\t\t\t\t\t;長居ゆう (合唱部の先輩)
\t\t\t\t\tRESULTS '= @"長居殿"
\t\t\t\tCASE 34
\t\t\t\t\t;桐島かいり (合唱部の先輩)
\t\t\t\t\tRESULTS '= @"桐島殿"
\t\t\t\tCASE 35
\t\t\t\t\tRESULTS '= @"梅ちゃん殿"
\t\t\t\tCASE 45
\t\t\t\t\tRESULTS '= @"円城寺殿"
\t\t\t\tCASE 57
\t\t\t\t\tRESULTS '= @"岩戸殿"
\t\t\t\tCASE 59
\t\t\t\t\tRESULTS '= @"水嶌殿"
\t\t\tENDSELECT
\t\tCASE 14
\t\t\t;花音ことり (特別呼称)
\t\t\tSELECTCASE AI
\t\t\t\tCASE 13
\t\t\t\t\t;羽森つばさ (唯一無二の相方・名前+しゃん)
\t\t\t\t\tRESULTS '= @"つばさしゃん"
\t\t\t\tCASE 15
\t\t\t\t\tRESULTS '= @"やえしゃん"
\t\t\t\tCASE 24
\t\t\t\t\tRESULTS '= @"なつみしゃん"
\t\t\t\tCASE 29
\t\t\t\t\t;春風なな (チア部部長・名前+しゃん)
\t\t\t\t\tRESULTS '= @"ななしゃん"
\t\t\t\tCASE 67
\t\t\t\t\t;日滝ましろ (チア部応援団長)
\t\t\t\t\tRESULTS '= @"団長しゃん"
\t\t\tENDSELECT"""

lines = lines[:idx_sp_case13] + new_cases_13_14.split('\n') + lines[idx_sp_case15:]
final_text = '\n'.join(lines).replace('\n', '\r\n')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(final_text.encode('cp932'))

print('Successfully updated CASE 13 and CASE 14 in AITE_YOBI.ERB.')
