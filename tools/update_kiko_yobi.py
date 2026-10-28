# -*- coding: utf-8 -*-
import glob

fpath = glob.glob('ERB/*AITE_YOBI*.ERB')[0]
with open(fpath, 'r', encoding='cp932') as fp:
    lines = fp.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 1. (1) 既定ルールに CASE 4 を追加（CASE 3の直後）
    if 'CASE 3\n' in line or 'CASE 3\r\n' in line:
        new_lines.append(line)
        i += 1
        while i < len(lines):
            new_lines.append(lines[i])
            if 'ENDIF' in lines[i]:
                # CASE 4 を挿入
                new_lines.append('\t\tCASE 4\n')
                new_lines.append('\t\t\t;早川きこ: 3年は「苗字+先輩」、2年・1年は「苗字+さん」\n')
                new_lines.append('\t\t\tIF GET_CHARA_GRADE(AI) == 3\n')
                new_lines.append('\t\t\t\tRESULTS \'= @"%SUR%先輩"\n')
                new_lines.append('\t\t\tELSE\n')
                new_lines.append('\t\t\t\tRESULTS \'= @"%SUR%さん"\n')
                new_lines.append('\t\t\tENDIF\n')
                i += 1
                break
            i += 1
        continue
    
    # 2. (2) L164周辺の CASE 4 ブロック（重複混入していた部分）を綺麗に置き換え
    if line.strip() == 'CASE 4' and i > 40:
        new_lines.append('\t\tCASE 4\n')
        new_lines.append('\t\t\t;早川きこ (特別呼称)\n')
        new_lines.append('\t\t\tSELECTCASE AI\n')
        new_lines.append('\t\t\t\tCASE 1\n')
        new_lines.append('\t\t\t\t\t;三善かなえ (親友)\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"みよちゃん"\n')
        new_lines.append('\t\t\t\tCASE 2\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"ゆきちゃん"\n')
        new_lines.append('\t\t\t\tCASE 3\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"ちよちゃん"\n')
        new_lines.append('\t\t\t\tCASE 5\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"あすかちゃん"\n')
        new_lines.append('\t\t\t\tCASE 7\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"ちあきちゃん"\n')
        new_lines.append('\t\t\t\tCASE 8\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"みさきちゃん"\n')
        new_lines.append('\t\t\t\tCASE 11\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"くるみちゃん"\n')
        new_lines.append('\t\t\t\tCASE 12\n')
        new_lines.append('\t\t\t\t\t;神樹いちか (オカ研仲間・3年だがちゃん付け)\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"いちかちゃん"\n')
        new_lines.append('\t\t\t\tCASE 14\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"ことりちゃん"\n')
        new_lines.append('\t\t\t\tCASE 20\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"しずくちゃん"\n')
        new_lines.append('\t\t\t\tCASE 27\n')
        new_lines.append('\t\t\t\t\t;夏野ゆり (吹奏楽部長)\n')
        new_lines.append('\t\t\t\t\tRESULTS \'= @"なっちゃん先輩"\n')
        new_lines.append('\t\t\tENDSELECT\n')
        
        # 重複ブロックの終わり（次の CASE 5 など）までスキップ
        i += 1
        while i < len(lines):
            # 次のトップレベル CASE (CASE 5 など) に達したら停止
            if lines[i].startswith('\t\tCASE ') and lines[i].strip() != 'CASE 1' and lines[i].strip() != 'CASE 4':
                break
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

normalized_text = ''.join(new_lines).replace('\r\n', '\n').replace('\n', '\r\n')

with open(fpath, 'wb') as fp:
    fp.write(normalized_text.encode('cp932'))

print('Updated AITE_YOBI successfully for Kiko!')
