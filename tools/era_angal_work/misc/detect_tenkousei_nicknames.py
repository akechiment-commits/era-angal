#!/usr/bin/env python3
"""
転校生あだ名検出スクリプト
各キャラの分析.txtから人名・呼称リストを読み、
既知キャラ名・一般呼称に該当しないものを「転校生のあだ名候補」として出力する。
"""

import re
import sys
import os
from pathlib import Path

# 71キャラのフルネーム対応表（引き継ぎ書より）
CHAR_NAMES = {
    "かなえ": "三善かなえ", "ゆき": "北川ゆき", "ちよ": "小野ちよ", "きこ": "早川きこ",
    "あすか": "桃智あすか", "あいか": "藍乃あいか", "ちあき": "高原ちあき", "みさき": "丸子みさき",
    "るか": "月永るか", "ゆゆ": "木之下ゆゆ", "くるみ": "氷野くるみ", "いちか": "神樹いちか",
    "つばさ": "羽森つばさ", "ことり": "花音ことり", "やえ": "長町やえ", "いさみ": "大虎いさみ",
    "あずさ": "小鳩あずさ", "ひめの": "熊沢ひめの", "みけ": "猫塚みけ", "しずく": "藤猪しずく",
    "すみれ": "雉子すみれ", "いかり": "鯱いかり", "こはる": "鶯木こはる", "なつみ": "三波なつみ",
    "つゆり": "八朔つゆり", "さあや": "堀田さあや", "ゆり": "夏野ゆり", "こよい": "星海こよい",
    "なな": "春風なな", "ゆう": "長居ゆう", "まりあ": "夢路まりあ", "まい": "安条まい",
    "るな": "柊るな", "かいり": "桐島かいり", "かな": "梅園かな", "ちか": "遠見ちか",
    "レンレン": "龍泉寺レンレン", "クー": "クー・カロア", "もも": "冴木もも", "はやて": "夜霧はやて",
    "ともこ": "悠木ともこ", "むつみ": "榊むつみ", "みどり": "砂賀みどり", "ひよの": "笹芽ひよの",
    "れいか": "円城寺れいか", "みづき": "双葉みづき", "みなづき": "双葉みなづき",
    "みつる": "四方みつる", "ぼたん": "小松ぼたん", "ぎん": "山條ぎん", "かすみ": "御影かすみ",
    "やこ": "湖南やこ", "まり": "花丘まり", "あやめ": "久坂あやめ", "さくら": "伊藤さくら",
    "ひかる": "八壁ひかる", "サン": "岩戸サン", "るり": "天宮るり", "うしお": "水嶌うしお",
    "かえで": "瀬川かえで", "ひまり": "鶴海ひまり", "すず": "黒森すず", "ちづる": "八雲ちづる",
    "しおん": "峰山しおん", "そら": "時国そら", "セイラ": "曽根セイラ", "ましろ": "日滝ましろ",
    "ふみ": "深鳥ふみ", "はじめ": "神樹はじめ", "ほとり": "神無月ほとり", "ひびき": "棗ひびき",
    "レオナルド": "レオナルド",  # 動物だが登場キャラ
}

# 全キャラ名のバリエーション生成
def build_known_names():
    known = set()
    for short, full in CHAR_NAMES.items():
        known.add(short)
        known.add(full)
        # 苗字・名前を分離して追加
        parts = full.replace("・", "")
        for p in [short]:
            # ちゃん/さん/くん/先輩/様/部長/さま 等のバリエーション
            for suffix in ["ちゃん", "さん", "くん", "先輩", "様", "部長", "副部長",
                           "さま", "殿", "氏", "嬢", "姫", "っち", "にゃん", "ちん"]:
                known.add(p + suffix)
        # フルネームからの苗字
        if len(full) > len(short):
            family = full.replace(short, "").strip()
            if family:
                known.add(family)
                for suffix in ["さん", "先輩", "ちゃん", "くん", "様", "部長"]:
                    known.add(family + suffix)
    
    # 既知の転校生あだ名（引き継ぎ書から。検出テスト時はコメントアウト可能）
    known_tenkousei = {
        "転校生", "転校生くん", "転校生さん",
        "転校生の先輩", "転校生先輩", "転校生のひと",
        # 以下は判明済みの転校生あだ名。新規検出時はコメントアウトして再実行
        # "ジョンくん", "ダーリン", "下僕くん",
        # "お兄ちゃん先輩", "弟くん", "ヘルプマン", "パパ",
    }
    
    # 一般的な呼称（キャラでも転校生でもない）
    general = {
        "お父さん", "お母さん", "お兄さん", "お兄ちゃん", "お姉さん", "お姉ちゃん",
        "お姫様", "王子様", "お嬢", "お嬢様", "先輩", "後輩", "先生",
        "お客さん", "店員さん", "巫女さん", "妖精さん", "植物さん", "お花さん",
        "甘えん坊さん", "がんばり屋さん", "うっかり屋さん", "困ったちゃん",
        "堕天使さん", "お疲れさん", "お集まりの皆さん", "おふたりさん",
        "ケーキ屋さん", "和菓子屋さん", "店長さん", "メイドさん", "ネコさん",
        "たくさん", "こんなにたくさん",
        "次期部長", "文化部部長", "陸上部副部長", "陸上部部長", "生徒会長",
        "生徒会長さん", "バレー部の先輩", "二年生の先輩", "うちの先輩",
        "誰かさん", "彼氏くん", "ねえさん",
    }
    
    # キャラ間の既知あだ名（テンプレート検出漏れの原因になるもの）
    known_char_nicknames = {
        # みづき↔みなづき
        "みなちゃん", "みづちゃん",
        # みつる→サン
        "お岩ちゃん",
        # むつみのあだ名群（キャラ向け）
        "アニキ", "アネゴ", "ピヨちゃん", "スナちゃん", "カロちゃん",
        "アンちゃん", "サエちゃん", "ヨッシー", "ぴこちゃん",
        # まりあ→かな
        "梅ちゃん",
        # みけ→さあや/かな
        "堀田先輩", "梅園先輩",
        # みさき→かいり
        "お嬢", "マルちゃん",
        # まりあ→ぼたん
        "こまっちコーチ",
        # まりあ→あすか
        "モモッチさん",
        # まりあ→ゆり
        "なっちゃん様",
        # ほとり→こよい
        "星ちゃん",
        # ほとり→しおん
        "峰山ちゃん",
        # まり→しおん
        "しおんさん",
        # その他の既知あだ名
        "サチエちゃん", "サチエさん",  # 猫の名前
        "レンティヌス様",  # まりあの宗教的呼称
        "このライオンさん", "ライオンさん",  # レオナルド
        "Missブシドー",
        "むぅちゃん",  # むつみの自称/呼ばれ名
        "双子屋さん",  # みづき・みなづきの通称
        "くんくん",  # 犬の鳴き声等
        "古代君",  # みづきが使うあだ名（キャラ向け）
    }
    
    # 「〜のXXX」「でXXX」等の部分一致ノイズパターン
    noise_prefixes = [
        "でも", "さすが", "ごめんね", "やっぱり", "ちょっと", "んですか",
        "んなさい", "あたしは", "わたくしは", "あっしは", "あっしが", "あっしの",
        "あたし", "わたしは", "わたしも", "わたしと", "たしは", "たしも",
        "僕が", "僕は", "それは", "でも", "しには", "つみに",
        "何で", "と", "は", "の", "に", "で", "が", "を", "も",
        "日は", "れるのは", "ど怖いよ", "そこの男子の",
        "のかかる", "よくも", "でおまえ",
    ]
    
    return known, known_tenkousei, general, noise_prefixes, known_char_nicknames


def parse_analysis_file(filepath):
    """分析ファイルから人名・呼称セクションを抽出"""
    entries = []
    in_section = False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '人名・呼称' in line:
                in_section = True
                continue
            if in_section:
                if line.startswith('---') or (line and not line.startswith(' ') and ':' not in line):
                    break
                m = re.match(r'\s*(.+?):\s*(\d+)回', line)
                if m:
                    name = m.group(1).strip()
                    count = int(m.group(2))
                    entries.append((name, count))
    
    return entries


def is_noise(name, noise_prefixes, known, known_tenkousei, general):
    """ノイズかどうか判定"""
    # 既知キャラ名の一部を含むノイズ（「でも梅園先輩」等）
    for prefix in noise_prefixes:
        if name.startswith(prefix):
            rest = name[len(prefix):]
            if rest in known or rest in known_tenkousei or rest in general:
                return True
    return False


def detect_nicknames(analysis_dir):
    known, known_tenkousei, general, noise_prefixes, known_char_nicknames = build_known_names()
    
    results = {}
    
    for filepath in sorted(Path(analysis_dir).glob("*_分析.txt")):
        char_name = filepath.stem.replace("_分析", "")
        entries = parse_analysis_file(filepath)
        
        suspects = []
        for name, count in entries:
            # 既知の転校生呼称はスキップ
            if name in known_tenkousei:
                continue
            # 既知キャラ名はスキップ
            if name in known:
                continue
            # 一般呼称はスキップ
            if name in general:
                continue
            # キャラ間あだ名はスキップ
            if name in known_char_nicknames:
                continue
            # ノイズパターンはスキップ
            if is_noise(name, noise_prefixes, known, known_tenkousei, general):
                continue
            # 1回だけの呼称はスキップ（ノイズが多い）
            if count <= 2:
                continue
            # 転校生を含む複合呼称はスキップ
            if "転校生" in name:
                continue
            # 「〜の」「〜と」で始まる複合呼称はスキップ
            if name.startswith(("のペコリーヌ", "そして", "ねぇ", "今日の", "おや", "あとで",
                                "何で", "うん", "たしか", "うちの", "このケーキ",
                                "花壇の", "この様", "笹芽ひよの", "長町やえ", "双葉み",
                                "ごめんね", "さすが", "ょっと")):
                continue
            # 自己言及パターンをスキップ
            if char_name in name:
                continue
            
            suspects.append((name, count))
        
        if suspects:
            results[char_name] = suspects
    
    return results


def main():
    if len(sys.argv) > 1:
        analysis_dir = sys.argv[1]
    else:
        # デフォルト: uploadsディレクトリ
        analysis_dir = "/mnt/user-data/uploads"
    
    results = detect_nicknames(analysis_dir)
    
    print("=" * 60)
    print("転校生あだ名候補検出結果")
    print("=" * 60)
    print()
    
    if not results:
        print("候補なし")
        return
    
    for char_name, suspects in sorted(results.items()):
        print(f"■ {char_name}")
        for name, count in suspects:
            print(f"    {name}: {count}回  ← 要確認")
        print()
    
    print("-" * 60)
    print("【判定基準】")
    print("  - 既知71キャラ名・苗字・あだ名に該当しない")
    print("  - 一般呼称（お父さん等）に該当しない")
    print("  - 2回以上出現する")
    print("  - 転校生の固有あだ名の可能性あり → セリフで確認すること")


if __name__ == "__main__":
    main()
