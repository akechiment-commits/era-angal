# -*- coding: utf-8 -*-
import glob, re
from collections import Counter

def main():
    files = glob.glob('tools/scenarios/*.txt')
    print(f'Total scenario files: {len(files)}')

    # Nickname endings or patterns in Himari's speech
    # Himari uses: 〜りん, 〜っち, 〜ちゃん, 〜くん, 〜先輩, 〜坊, etc.
    # Let's search all Himari lines for direct address forms
    himari_calls = Counter()

    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            for line in fp:
                if line.startswith('【ひまり】') or line.startswith('【鶴海ひまり】'):
                    quotes = re.findall(r'「(.*?)」', line)
                    for q in quotes:
                        # Matches potential nicknames
                        # e.g., words followed by punctuation: 「ミッチー！」「ユッキー、」「下僕くん、」
                        m_list = re.findall(r'([一-龠ぁ-んァ-ヶー]{2,8}(?:ちゃん|くん|先輩|っち|りん|坊|たん|っぺ|氏|殿)?)[、！!]', q)
                        for m in m_list:
                            himari_calls[m] += 1

    with open('tools/era_angal_work/himari_scenarios_all_calls.txt', 'w', encoding='utf-8') as out:
        for k, v in himari_calls.most_common(200):
            out.write(f'{k}: {v}\n')

    print('Wrote himari_scenarios_all_calls.txt successfully!')

if __name__ == '__main__':
    main()
