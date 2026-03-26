#!/usr/bin/env python3
"""
キャラクタープロンプト生成スクリプト（フル版）
プロファイル・人間関係・固有名詞・セリフサンプルを統合して
新しいClaudeセッションに貼り付けるだけで会話できるプロンプトを生成する

使い方:
  python make_character_prompt.py ひまり
  python make_character_prompt.py ひまり --samples 100
"""

import argparse
import csv
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

SCENARIO_DIR = Path("scenarios")
PROFILES_FILE = Path("character_profiles.json")
CHAR_DATA_CSV = Path("character_data.csv")


def load_char_data_csv() -> dict[str, dict]:
    """character_data.csv からプロフィールを読み込む"""
    if not CHAR_DATA_CSV.exists():
        return {}
    profiles = {}
    with open(CHAR_DATA_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if name:
                profiles[name] = {k: v.strip() for k, v in row.items()
                                  if v and v.strip() and k != "name"}
    return profiles


# ===== データ読み込み =====

def load_all_lines() -> dict[str, list[str]]:
    """全キャラの全セリフを読み込む"""
    char_lines: dict[str, list[str]] = defaultdict(list)
    char_files: dict[str, set[str]] = defaultdict(set)  # キャラ→登場ファイル名

    for txt in sorted(SCENARIO_DIR.glob("*.txt")):
        try:
            content = txt.read_text(encoding="utf-8")
        except Exception:
            continue
        for line in content.splitlines():
            m = re.match(r"^【(.+?)】(.+)$", line)
            if m:
                name = m.group(1).strip()
                text = m.group(2).strip()
                char_lines[name].append(text)
                char_files[name].add(txt.stem)

    return dict(char_lines), dict(char_files)


def load_profile(name: str) -> dict | None:
    if not PROFILES_FILE.exists():
        return None
    with open(PROFILES_FILE, encoding="utf-8") as f:
        profiles = json.load(f)
    for p in profiles:
        if p["name"] == name:
            return p
    return None


# ===== 人間関係抽出 =====

def extract_relationships(name: str,
                          target_lines: list[str],
                          all_char_names: list[str],
                          char_files: dict[str, set[str]]) -> list[dict]:
    """
    対象キャラのセリフ内で言及される他キャラを抽出
    + 同じシナリオファイルに登場する共演キャラを集計
    """
    mentions = Counter()
    co_appear = Counter()

    target_files = char_files.get(name, set())

    all_text = " ".join(target_lines)
    for other in all_char_names:
        if other == name or len(other) < 2:
            continue
        # セリフ内での言及回数
        cnt = all_text.count(other)
        if cnt > 0:
            mentions[other] = cnt
        # 同じファイルへの共演回数
        co = len(target_files & char_files.get(other, set()))
        if co > 0:
            co_appear[other] = co

    # 言及が多い上位10 + 共演が多い上位10 をマージ
    result = {}
    for other, cnt in mentions.most_common(10):
        result[other] = {"mention": cnt, "co_appear": co_appear.get(other, 0)}
    for other, cnt in co_appear.most_common(10):
        if other not in result:
            result[other] = {"mention": mentions.get(other, 0), "co_appear": cnt}

    # スコアでソート（言及×2 + 共演）
    ranked = sorted(result.items(),
                    key=lambda x: x[1]["mention"] * 2 + x[1]["co_appear"],
                    reverse=True)
    return [{"name": k, **v} for k, v in ranked[:12]]


# ===== 固有名詞抽出 =====

def extract_proper_nouns(lines: list[str]) -> list[str]:
    """
    セリフから固有名詞候補を抽出
    - カタカナ2文字以上の語
    - 鍵括弧内で繰り返し出現する語
    - 「〜学院」「〜部」「〜委員会」などの固有表現
    """
    all_text = " ".join(lines)

    nouns = Counter()

    # カタカナ語（2文字以上）
    for m in re.finditer(r"[ァ-ヶーｦ-ﾟ]{2,}", all_text):
        w = m.group(0)
        if len(w) >= 2:
            nouns[w] += 1

    # 鍵括弧内のテキスト（2文字以上）
    for m in re.finditer(r"[「『]([^」』]{2,8})[」』]", all_text):
        w = m.group(1)
        if not re.search(r"[、。！？]", w):
            nouns[w] += 1

    # 「〜学院」「〜部」「〜委員会」「〜祭」
    for pattern in [r"[\w]{2,6}学院", r"[\w]{1,4}部", r"[\w]{2,6}委員会",
                    r"[\w]{2,4}祭", r"[\w]{2,4}クラブ"]:
        for m in re.finditer(pattern, all_text):
            nouns[m.group(0)] += 1

    # 頻度2以上、かつ明らかな一般語を除外
    stopwords = {"それ", "これ", "あれ", "もの", "こと", "みんな", "ところ",
                 "でも", "から", "けど", "って", "ため", "とき", "ここ",
                 "ちょっと", "ほんと", "ほんとに", "やっぱ", "やっぱり",
                 "ありがとう", "ごめん", "すごい", "かわいい"}

    results = [w for w, cnt in nouns.most_common(30)
               if cnt >= 2 and w not in stopwords and len(w) >= 2]
    return results[:20]


# ===== サンプリング =====

def sample_lines(lines: list[str], n: int) -> list[str]:
    if len(lines) <= n:
        return lines
    short  = [l for l in lines if len(l) <= 20]
    medium = [l for l in lines if 21 <= len(l) <= 50]
    long_  = [l for l in lines if len(l) > 50]
    each = n // 3
    result = (
        random.sample(short,  min(each, len(short)))  +
        random.sample(medium, min(each, len(medium))) +
        random.sample(long_,  min(each, len(long_)))
    )
    if len(result) < n:
        rest = [l for l in lines if l not in set(result)]
        result += random.sample(rest, min(n - len(result), len(rest)))
    return result


# ===== プロンプト組み立て =====

def make_prompt(name: str,
                lines: list[str],
                profile: dict | None,
                char_data: dict | None,
                relationships: list[dict],
                proper_nouns: list[str],
                samples: int) -> str:

    sampled = sample_lines(lines, samples)
    lines_text = "\n".join(f"・{l}" for l in sampled)

    # ゲーム内プロフィールセクション（CSV入力データ）
    char_data_section = ""
    if char_data:
        labels = {
            "height": "身長", "weight": "体重", "three_sizes": "スリーサイズ",
            "birthday": "誕生日", "blood_type": "血液型",
            "club": "部活", "committee": "委員会",
            "class": "クラス", "grade": "学年",
            "fav_color": "好きな色", "family": "家族構成", "hobbies": "趣味",
            "intro": "紹介文", "old_intro": "旧紹介文",
        }
        items = []
        for key, label in labels.items():
            val = char_data.get(key, "")
            if val:
                items.append(f"- {label}: {val}")
        if items:
            char_data_section = f"""
【{name}のゲーム内プロフィール】
{chr(10).join(items)}
"""

    # 話し方プロファイルセクション
    profile_section = ""
    if profile:
        fp = profile.get("main_first_person", "不明")
        endings = ", ".join(profile.get("top_endings", [])[:6])
        words = ", ".join(profile.get("top_words", [])[:10])
        tone = profile.get("tone", "不明")
        profile_section = f"""
【{name}の話し方・性格】
- 一人称: {fp}
- よく使う語尾: {endings}
- 頻出ワード: {words}
- トーン: {tone}
- セリフ総数: {profile.get('total_lines', len(lines))}行
"""

    # 人間関係セクション
    rel_section = ""
    if relationships:
        rel_lines = []
        for r in relationships:
            desc = f"言及{r['mention']}回 / 共演{r['co_appear']}話"
            rel_lines.append(f"- {r['name']}（{desc}）")
        rel_section = f"""
【{name}の人間関係（ゲーム内での言及・共演回数）】
{chr(10).join(rel_lines)}
"""

    # 固有名詞セクション
    noun_section = ""
    if proper_nouns:
        noun_section = f"""
【{name}のセリフに出てくる固有名詞・キーワード】
{', '.join(proper_nouns)}
"""

    return f"""あなたはあんさんぶるガールズ!!のキャラクター「{name}」です。
以下の情報をもとに{name}として会話してください。
{char_data_section}{profile_section}{rel_section}{noun_section}
【{name}の実際のゲーム内セリフ（{len(sampled)}件）】
{lines_text}

【ロールプレイのルール】
- 常に{name}として話す。説明・注釈・メタ発言は不要
- 上記セリフの口調・一人称・語尾を忠実に守る
- 人間関係の情報を踏まえて自然に振る舞う
- どんな話題でも{name}の視点・性格で答える

準備ができたら「{name}です。よろしく！」のように一言だけ{name}らしく挨拶してください。"""


# ===== メイン =====

def main():
    parser = argparse.ArgumentParser(description="キャラクタープロンプト生成（フル版）")
    parser.add_argument("name", help="キャラ名")
    parser.add_argument("--samples", "-n", type=int, default=80,
                        help="サンプルセリフ数（デフォルト80）")
    args = parser.parse_args()

    print(f"データ読み込み中...")
    all_lines, char_files = load_all_lines()

    target_lines = all_lines.get(args.name)
    if not target_lines:
        print(f"エラー: 「{args.name}」のセリフが見つかりません")
        return

    print(f"「{args.name}」: {len(target_lines)}行")

    profile = load_profile(args.name)
    if profile:
        print(f"話し方プロファイル読み込み完了")
    else:
        print(f"話し方プロファイルなし（analyze_characters.py を実行すると精度が上がります）")

    all_char_data = load_char_data_csv()
    char_data = all_char_data.get(args.name)
    if char_data:
        print(f"ゲーム内プロフィール読み込み完了（{len(char_data)}項目）")
    else:
        print(f"ゲーム内プロフィールなし（manage_profiles.py --init でCSVを作成して入力できます）")

    print(f"人間関係を抽出中...")
    all_char_names = list(all_lines.keys())
    relationships = extract_relationships(args.name, target_lines, all_char_names, char_files)
    print(f"関連キャラ: {len(relationships)}人")

    print(f"固有名詞を抽出中...")
    proper_nouns = extract_proper_nouns(target_lines)
    print(f"固有名詞: {len(proper_nouns)}件")

    prompt = make_prompt(args.name, target_lines, profile, char_data,
                         relationships, proper_nouns, args.samples)

    out_file = Path(f"prompt_{args.name}.txt")
    out_file.write_text(prompt, encoding="utf-8")

    print(f"\n→ {out_file} 保存完了")
    print(f"   文字数: {len(prompt):,}文字")
    print(f"\n使い方: claude.ai で新しい会話を開いて {out_file} の内容を貼り付けてください")


if __name__ == "__main__":
    main()
