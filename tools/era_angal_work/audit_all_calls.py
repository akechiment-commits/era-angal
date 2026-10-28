# -*- coding: utf-8 -*-
import os, glob, re
from collections import defaultdict

def main():
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        erb_text = f.read()

    # Character names mapping
    chara_info = {
        0: ('主人公', 'あなた'),
        1: ('鶴海ひまり', 'ひまり'), 2: ('花音ことり', 'ことり'), 3: ('羽森つばさ', 'つばさ'),
        4: ('長町やえ', 'やえ'), 5: ('大虎いさみ', 'いさみ'), 6: ('藍乃あいか', 'あいか'),
        7: ('小鳩あずさ', 'あずさ'), 8: ('熊沢ひめの', 'ひめの'), 9: ('月永るか', 'るか'),
        10: ('木之下ゆゆ', 'ゆゆ'), 11: ('猫塚みけ', 'みけ'), 12: ('神樹いちか', 'いちか'),
        13: ('羽森つばさ', 'つばさ'), 14: ('花音ことり', 'ことり'), 15: ('長町やえ', 'やえ'),
        16: ('大虎いさみ', 'いさみ'), 17: ('小鳩あずさ', 'あずさ'), 18: ('熊沢ひめの', 'ひめの'),
        19: ('猫塚みけ', 'みけ'), 20: ('藤猪しずく', 'しずく'), 21: ('雉子すみれ', 'すみれ'),
        22: ('鯱いかり', 'いかり'), 23: ('鶯木こはる', 'こはる'), 24: ('三波なつみ', 'なつみ'),
        25: ('八朔つゆり', 'つゆり'), 26: ('堀田さあや', 'さあや'), 27: ('夏野ゆり', 'ゆり'),
        28: ('星海こよい', 'こよい'), 29: ('春風なな', 'なな'), 30: ('長居ゆう', 'ゆう'),
        31: ('夢路まりあ', 'まりあ'), 32: ('安条まい', 'まい'), 33: ('柊るな', 'るな'),
        34: ('桐島かいり', 'かいり'), 35: ('梅園かな', 'かな'), 36: ('遠見ちか', 'ちか'),
        37: ('龍泉寺レンレン', 'レンレン'), 38: ('クー・カロア', 'カロア'), 39: ('冴木もも', 'もも'),
        40: ('夜霧はやて', 'はやて'), 41: ('悠木ともこ', 'ともこ'), 42: ('榊むつみ', 'むつみ'),
        43: ('砂賀みどり', 'みどり'), 44: ('笹芽ひよの', 'ひよの'), 45: ('円城寺れいか', 'れいか'),
        46: ('双葉みづき', 'みづき'), 47: ('双葉みなづき', 'みなづき'), 48: ('四方みつる', 'みつる'),
        49: ('小松ぼたん', 'ぼたん'), 50: ('山條ぎん', 'ぎん'), 51: ('御影かすみ', 'かすみ'),
        52: ('湖南やこ', 'やこ'), 53: ('花丘まり', 'まり'), 54: ('久坂あやめ', 'あやめ'),
        55: ('伊藤さくら', 'さくら'), 56: ('八壁ひかる', 'ひかる'), 57: ('岩戸サン', 'サン'),
        58: ('天宮るり', 'るり'), 59: ('水嶌うしお', 'うしお'), 60: ('瀬川かえで', 'かえで'),
        61: ('鶴海ひまり', 'ひまり'), 62: ('黒森すず', 'すず'), 63: ('八雲ちづる', 'ちづる'),
        64: ('峰山しおん', 'しおん'), 65: ('時国そら', 'そら'), 66: ('曽根セイラ', 'セイラ'),
        67: ('日滝ましろ', 'ましろ'), 68: ('深鳥ふみ', 'ふみ'), 69: ('神樹はじめ', 'はじめ'),
        70: ('神無月ほとり', 'ほとり'), 71: ('棗ひびき', 'ひびき'), 72: ('あんず', 'あんず')
    }

    # Extract all individual rules: SP -> AI -> call string
    pos2 = erb_text.find(';--- (2) 個別の特殊呼称（上書き）---')
    if pos2 == -1:
        parts = erb_text.split('SELECTCASE SP')
        indiv_text = parts[2]
    else:
        indiv_text = erb_text[pos2:]

    # Parse blocks
    # \t\tCASE (\d+)
    #   SELECTCASE AI
    #     CASE (\d+) ... RESULTS '= @"([^"]+)"
    speaker_blocks = re.findall(r'\t\tCASE (\d+)\s*\n\t\t\t;([^\n]+)\n\t\t\tSELECTCASE AI\n(.*?)\t\t\tENDSELECT', indiv_text, re.DOTALL)
    print(f'Parsed {len(speaker_blocks)} speaker blocks in ERB.')

    all_entries = [] # (sp_id, sp_name, ai_id, ai_name, call_str)
    for sp_id_str, sp_comment, ai_content in speaker_blocks:
        sp_id = int(sp_id_str)
        sp_fname, sp_cname = chara_info.get(sp_id, (f'CHAR_{sp_id}', f'CHAR_{sp_id}'))

        ai_cases = re.findall(r'CASE (\d+)\s*\n\s*(?:;[^\n]*\n\s*)*RESULTS \'= @"([^"]+)"', ai_content)
        for ai_id_str, call_str in ai_cases:
            ai_id = int(ai_id_str)
            ai_fname, ai_cname = chara_info.get(ai_id, (f'TARGET_{ai_id}', f'TARGET_{ai_id}'))
            all_entries.append((sp_id, sp_fname, sp_cname, ai_id, ai_fname, ai_cname, call_str))

    print(f'Total individual call entries: {len(all_entries)}')

    # Load speaker dialogue from tools/output/{chara}.txt
    output_texts = {}
    for sp_id, (fname, cname) in chara_info.items():
        if sp_id == 0: continue
        path = os.path.join('tools', 'output', f'{cname}.txt')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                output_texts[cname] = fp.read()

    # Load all scenarios speaker lines
    scenario_files = glob.glob('tools/scenarios/*.txt')
    scenario_speaker_lines = defaultdict(list)
    for fpath in scenario_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            for line in fp:
                line = line.strip()
                m = re.match(r'【(.*?)】(.*)', line)
                if m:
                    spk, text = m.group(1), m.group(2)
                    scenario_speaker_lines[spk].append(text)

    # Now verify each entry
    results = []
    zero_occurrences = []

    for sp_id, sp_fname, sp_cname, ai_id, ai_fname, ai_cname, call_str in all_entries:
        # Check count in tools/output/{sp_cname}.txt
        out_txt = output_texts.get(sp_cname, '')
        count_out = out_txt.count(call_str)

        # Check count in scenarios for speaker
        scen_lines = scenario_speaker_lines.get(sp_cname, [])
        # also try sp_fname
        if not scen_lines:
            scen_lines = scenario_speaker_lines.get(sp_fname, [])
        count_scen = sum(1 for l in scen_lines if call_str in l)

        total_count = count_out + count_scen

        # If call_str contains variables like %CALLNAME:AI%, skip or evaluate
        if '%' in call_str:
            continue

        results.append((sp_id, sp_fname, ai_id, ai_fname, call_str, count_out, count_scen, total_count))
        if total_count == 0:
            zero_occurrences.append((sp_id, sp_fname, ai_id, ai_fname, call_str))

    print(f'Verified {len(results)} entries.')
    print(f'Zero occurrences found: {len(zero_occurrences)}')

    with open('tools/era_angal_work/audit_all_chara_individual_calls.txt', 'w', encoding='utf-8') as out:
        out.write(f'=== ZERO OCCURRENCE ENTRIES (Suspect / Not in original text) ({len(zero_occurrences)}) ===\n')
        for sp_id, sp_fname, ai_id, ai_fname, call_str in zero_occurrences:
            out.write(f'CHAR_{sp_id} {sp_fname} -> AI_{ai_id} {ai_fname}: "{call_str}" (0 occurrences!)\n')

        out.write('\n=== ALL ENTRIES AUDIT ===\n')
        for sp_id, sp_fname, ai_id, ai_fname, call_str, count_out, count_scen, total_count in results:
            out.write(f'CHAR_{sp_id} {sp_fname} -> AI_{ai_id} {ai_fname}: "{call_str}" (output:{count_out}, scen:{count_scen}, total:{total_count})\n')

    print('Wrote audit_all_chara_individual_calls.txt successfully!')

if __name__ == '__main__':
    main()
