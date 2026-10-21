# -*- coding: utf-8 -*-
import glob, re
from collections import Counter

def main():
    files = glob.glob('tools/scenarios/*.txt')

    himari_lines = []
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            for l in fp:
                if l.startswith('【ひまり】') or l.startswith('【鶴海ひまり】'):
                    himari_lines.append(l.strip())

    print(f'Total Himari lines: {len(himari_lines)}')

    # Search for all nicknames ending in りん, っち, ちゃん, 姫, 坊, 助, etc.
    # or katakana/hiragana nicknames in Himari's speech
    nick_candidates = Counter()
    for l in himari_lines:
        quotes = re.findall(r'「(.*?)」', l)
        for q in quotes:
            # Look for Katakana words ending in ッ/ー/ン
            for m in re.findall(r'([ァ-ヶー]{3,8})', q):
                if m not in ['アンサンブル', 'プレゼント', 'アポイントメント', 'フローリング', 'デュエット', 'カラオケ', 'チョコレート', 'クリスマス', 'トラブル', 'アイスクリーム']:
                    nick_candidates[m] += 1
            # Look for words ending in りん, っち, 姫, ちゃん
            for m in re.findall(r'([一-龠ぁ-んァ-ヶー]{2,6}(?:りん|っち|姫))', q):
                nick_candidates[m] += 1

    with open('tools/era_angal_work/himari_nick_candidates.txt', 'w', encoding='utf-8') as out:
        for k, v in nick_candidates.most_common(150):
            out.write(f'{k}: {v}\n')

    print('Wrote himari_nick_candidates.txt')

if __name__ == '__main__':
    main()
