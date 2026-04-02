"""
キャラ関係性分析スクリプト（上級版）

原作シナリオから会話の流れを読み、誰に対してどう喋っているかを分析する。
出力はコンパクトな要約形式（200〜400行程度）。

使い方:
    python analyze_relations.py <シナリオフォルダ> <キャラ名>

例:
    python analyze_relations.py "C:/Users/guile/era-angal/tools/scenarios" あいか

出力:
    同じフォルダに「キャラ名_関係性分析.txt」を生成
"""

import os
import re
import sys
from collections import defaultdict, Counter

# --- 感情判定（かなえ分析で使ったものより拡張） ---
EMOTION_PATTERNS = {
    "照れ・動揺": [
        re.compile(r"[あわうえ]っ"), re.compile(r"[すはべばそ]、[すはべばそ]"),
        re.compile(r"えへへ"), re.compile(r"ふあ"), re.compile(r"ひゃ"),
        re.compile(r"えっ[、！]"), re.compile(r"う[うー]"), re.compile(r"……[♪☆]"),
    ],
    "ツン・突き放し": [
        re.compile(r"べ、別に"), re.compile(r"関係ない"), re.compile(r"知りません"),
        re.compile(r"勝手に"), re.compile(r"お気遣いなく"), re.compile(r"そういうのじゃ"),
        re.compile(r"余計なお世話"), re.compile(r"ほっといて"),
    ],
    "好意・甘え": [
        re.compile(r"好き"), re.compile(r"大好き"), re.compile(r"守り"),
        re.compile(r"一緒に"), re.compile(r"ありがと"), re.compile(r"嬉し"),
        re.compile(r"甘やか"), re.compile(r"い～こ"), re.compile(r"ごろごろ"),
        re.compile(r"♪$"),
    ],
    "心配・世話焼き": [
        re.compile(r"大丈夫"), re.compile(r"心配"), re.compile(r"気をつけ"),
        re.compile(r"無理し"), re.compile(r"怪我"), re.compile(r"風邪"),
        re.compile(r"ごめんね"),
    ],
    "怒り・苛立ち": [
        re.compile(r"腹立"), re.compile(r"許さ"), re.compile(r"いい加減"),
        re.compile(r"ひどい"), re.compile(r"ふざけ"), re.compile(r"くせに"),
        re.compile(r"のくせ"),
    ],
    "悲しみ・不安": [
        re.compile(r"怖[いく]"), re.compile(r"嫌[だな]"), re.compile(r"不安"),
        re.compile(r"寂し"), re.compile(r"泣[いき]"), re.compile(r"逃げ"),
        re.compile(r"つらい"), re.compile(r"苦し"),
    ],
    "笑い・余裕": [
        re.compile(r"ふふ"), re.compile(r"あはは"), re.compile(r"おや[？?]"),
        re.compile(r"ふぅむ"), re.compile(r"なるほど"),
    ],
    "敬意・信頼": [
        re.compile(r"さすが"), re.compile(r"尊敬"), re.compile(r"頼もし"),
        re.compile(r"立派"), re.compile(r"すごい"), re.compile(r"感謝"),
        re.compile(r"任せ"),
    ],
}


def detect_emotions(text):
    """セリフの感情を判定（複数該当あり）"""
    found = []
    for emotion, patterns in EMOTION_PATTERNS.items():
        for p in patterns:
            if p.search(text):
                found.append(emotion)
                break
    return found


def load_scenarios(scenario_dir):
    """全シナリオを読み込み、(ファイルID, [(名前, セリフ), ...]) のリストで返す"""
    pattern = re.compile(r"^【(.*?)】(.*)$")
    scenarios = {}

    for i in range(1, 10000):
        filepath = os.path.join(scenario_dir, f"{i}.txt")
        if not os.path.exists(filepath):
            continue

        for enc in ("utf-8", "cp932", "utf-8-sig"):
            try:
                with open(filepath, "r", encoding=enc) as f:
                    raw_lines = f.readlines()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            continue

        dialogue_lines = []
        for line in raw_lines:
            line = line.strip().replace("story_user_name", "転校生")
            if not line or line.startswith("==="):
                continue
            m = pattern.match(line)
            if m:
                name = m.group(1).strip()
                text = m.group(2).strip()
                if text:
                    dialogue_lines.append((name, text))

        if dialogue_lines:
            scenarios[i] = dialogue_lines

    return scenarios


def analyze_character(scenarios, target_name):
    """特定キャラの関係性を分析"""

    # 誰の直後に喋っているか -> 会話相手
    partner_lines = defaultdict(list)  # 相手名 -> [(対象キャラのセリフ, 感情)]
    # 誰について言及しているか
    mention_emotions = defaultdict(lambda: Counter())  # 言及相手 -> 感情Counter

    # 対象キャラが登場するシナリオだけ処理
    appearing_scenarios = []
    for fid, lines in scenarios.items():
        names_in_scene = set(n for n, t in lines)
        if target_name in names_in_scene:
            appearing_scenarios.append((fid, lines))

    # 全共演キャラをカウント
    coappear = Counter()
    for fid, lines in appearing_scenarios:
        others = set(n for n, t in lines if n != target_name and n != "")
        for o in others:
            coappear[o] += 1

    # 会話相手別の分析
    for fid, lines in appearing_scenarios:
        prev_speaker = ""
        for name, text in lines:
            if name == target_name:
                emotions = detect_emotions(text)
                # 直前の話者を会話相手として記録
                if prev_speaker and prev_speaker != target_name and prev_speaker != "":
                    partner_lines[prev_speaker].append((text, emotions))
                elif prev_speaker == "":
                    # 地の文の後 -> 独白的
                    partner_lines["（独白・地の文後）"].append((text, emotions))

            if name != "":  # 地の文でなければ更新
                prev_speaker = name

    # 相手別の感情分布を集計
    partner_emotion_dist = {}
    partner_samples = {}

    for partner, items in partner_lines.items():
        emotion_counter = Counter()
        emotion_samples = defaultdict(list)

        for text, emotions in items:
            if not emotions:
                emotion_counter["（感情タグなし）"] += 1
            for e in emotions:
                emotion_counter[e] += 1
                if len(emotion_samples[e]) < 2:
                    short = text[:70] + "…" if len(text) > 70 else text
                    emotion_samples[e].append(short)

        partner_emotion_dist[partner] = emotion_counter
        partner_samples[partner] = emotion_samples

    return coappear, partner_lines, partner_emotion_dist, partner_samples


def format_report(target_name, coappear, partner_lines, partner_emotion_dist, partner_samples):
    """分析結果をコンパクトなレポートに整形"""
    out = []
    out.append(f"=== {target_name} 関係性分析 ===\n")

    # --- 共演回数ランキング ---
    out.append("--- 共演シナリオ数（上位20） ---")
    for name, count in coappear.most_common(20):
        out.append(f"  {name}: {count}話")
    out.append("")

    # --- 会話相手別の感情分析（会話量上位15） ---
    out.append("--- 会話相手別分析（応答数上位15） ---")
    out.append("（直前の発言者ごとに、対象キャラがどんな感情で応答しているか）\n")

    sorted_partners = sorted(partner_lines.items(), key=lambda x: -len(x[1]))

    for partner, items in sorted_partners[:15]:
        total = len(items)
        out.append(f"■ {partner}（応答{total}件）")

        # 感情分布
        edist = partner_emotion_dist.get(partner, Counter())
        if edist:
            dist_parts = []
            for emotion, count in edist.most_common():
                pct = count / total * 100
                if pct >= 3:  # 3%未満は省略
                    dist_parts.append(f"{emotion}:{count}件({pct:.0f}%)")
            if dist_parts:
                out.append(f"  感情分布: {' / '.join(dist_parts)}")

        # 感情別サンプル（主要な感情のみ、各2件）
        samples = partner_samples.get(partner, {})
        shown_emotions = set()
        for emotion, count in edist.most_common(4):
            if emotion == "（感情タグなし）":
                continue
            if emotion in samples and samples[emotion]:
                if emotion not in shown_emotions:
                    for s in samples[emotion][:2]:
                        out.append(f"  [{emotion}] {s}")
                    shown_emotions.add(emotion)

        # タグなしのサンプルも数件
        no_tag_samples = [(t, e) for t, e in items if not e]
        if no_tag_samples and len(no_tag_samples) > total * 0.3:
            out.append(f"  [通常応答例]")
            for t, _ in no_tag_samples[:2]:
                short = t[:70] + "…" if len(t) > 70 else t
                out.append(f"    {short}")

        out.append("")

    return "\n".join(out)


def main():
    if len(sys.argv) != 3:
        print("使い方: python analyze_relations.py <シナリオフォルダ> <キャラ名>")
        print('例:     python analyze_relations.py "C:/Users/guile/era-angal/tools/scenarios" あいか')
        sys.exit(1)

    scenario_dir = sys.argv[1]
    target_name = sys.argv[2]

    if not os.path.isdir(scenario_dir):
        print(f"エラー: {scenario_dir} が見つかりません")
        sys.exit(1)

    print(f"シナリオ読み込み中...")
    scenarios = load_scenarios(scenario_dir)
    print(f"  {len(scenarios)}ファイル読み込み完了")

    print(f"{target_name} の関係性を分析中...")
    coappear, partner_lines, partner_emotion_dist, partner_samples = analyze_character(scenarios, target_name)

    report = format_report(target_name, coappear, partner_lines, partner_emotion_dist, partner_samples)

    outpath = os.path.join(os.path.dirname(sys.argv[0]) or ".", f"{target_name}_関係性分析.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n→ 保存: {outpath}")


if __name__ == "__main__":
    main()
