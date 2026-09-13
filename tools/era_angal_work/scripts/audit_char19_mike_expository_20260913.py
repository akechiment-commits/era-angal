"""CHAR19猫塚みけの性的口上を、説明調・接続状態の反復として監査する。"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAR_PATH = ROOT / "ERB" / "CHAR" / "CHAR_19_猫塚みけ_COM.ERB"
SOURCE_PATH = ROOT / "tools" / "output" / "みけ.txt"
HEADER_RE = re.compile(r";---\s*COM(\d+)\s*(.*?)\s*---")
SEX_LABEL_RE = re.compile(r"^@CHAR_(?:VIRGIN|FIRST_KISS|UNDRESS|EJAC|ORGASM)_19\b")
SEX_RE = re.compile(
    r"性交|セックス|正常位|後背位|騎乗位|対面座位|背面座位|アナル|フェラ|クンニ|"
    r"自慰|手淫|キス|愛撫|絶頂|射精|着衣|挿入|中出し|精液|口内|乳房|乳首|"
    r"指入れ|玩具|オナニー|潮吹き|顔面騎乗|貝合わせ|シックスナイン|乳揉み|"
    r"バイブ|ローター|ニプル|搾乳|オナホール|クスコ|ペニバン|パイズリ|足コキ|"
    r"口移し|精飲|張形|処女|風呂|シャワー"
)
POSITION_RE = re.compile(
    r"正常位|後背位|騎乗位|対面座位|背面座位|振り向いて|繋がって|つながって|"
    r"繋がる|つながる|後ろから|前から|上から|下から|背中から|向かい合って|"
    r"背面で|正面から"
)
META_RE = re.compile(
    r"説明|実況|手順|観察|観測|データ|情報量|処理|難易度|生理現象|実験|"
    r"行為者|攻める側|挿入する側|見る側|受け手|主導権|命令|うまくできてる|"
    r"ちゃんとできてる|できてる？|できてるか"
)
CAT_RE = re.compile(r"うにゃ|にゃ|ごろ|ふにゃ|にゃふふ|にゃあ|猫|ねこ")
REACTION_RE = re.compile(
    r"ん|あ|っ|声|息|熱|痛|気持|感じ|恥|震|濡|漏れ|喘|怖|泣|"
    r"ゆっくり|もっと|お願い|して|しないで|離れないで|好き|止まって|止めて|"
    r"かわい|可愛|だいすき|ごろごろ|すりすり"
)
BARE_UNYA_RE = re.compile(r"うにゃ(?![あ～〜っんーぁ])")
TERMS = (
    "あたし", "うにゃ", "にゃ", "ごろ", "先輩", "転校生", "つながって", "繋がって",
    "後ろから", "正常位", "後背位", "説明", "実況", "観察", "命令", "うまく", "ちゃんと",
    "攻める側", "実験", "採点", "主導権", "私", "わたし", "俺", "おまえ", "あんた",
)


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932")


def collect() -> tuple[list[dict[str, object]], Counter[str], list[str]]:
    text = read_cp932(CHAR_PATH)
    rows: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    sexual_speeches: list[str] = []
    current_com: int | None = None
    current_title = ""
    current_label = ""
    current_sex = False
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("@"):
            current_label = stripped
            current_com = None
            current_title = ""
            current_sex = bool(SEX_LABEL_RE.match(current_label))
        match = HEADER_RE.search(line)
        if match:
            current_com = int(match.group(1))
            current_title = match.group(2)
            current_sex = bool(SEX_RE.search(current_title)) or bool(SEX_LABEL_RE.match(current_label))
        if not current_sex or "PRINTFORM" not in line:
            continue
        speech = line.split("PRINTFORM", 1)[1].strip()
        sexual_speeches.append(speech)
        score = 0
        flags: list[str] = []
        if POSITION_RE.search(speech):
            score += 3
            flags.append("position")
        if META_RE.search(speech):
            score += 4
            flags.append("meta")
        if re.match(r"[\t ]*PRINTFORM\w*\s*[「『]?\s*(?:後ろ|前|上|下|背中|向かい|振り向|繋が|つなが)", line):
            score += 2
            flags.append("opening_position")
        if CAT_RE.search(speech):
            flags.append("cat_marker")
        if REACTION_RE.search(speech):
            flags.append("reaction")
        if score >= 3:
            rows.append({
                "line": lineno,
                "com": current_com or -1,
                "label": current_label,
                "title": current_title,
                "speech": speech,
                "score": score,
                "flags": ",".join(flags),
            })
    return rows, counts, sexual_speeches


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    rows, _, sexual_speeches = collect()
    current = read_cp932(CHAR_PATH)
    source = SOURCE_PATH.read_text(encoding="utf-8")
    print("CHAR19_MIKE_EXPOSITORY_AUDIT")
    print(f"SEXUAL_PRINTFORM={len(sexual_speeches)}")
    print(f"EXPOSITORY_CANDIDATES={len(rows)}")
    print(f"CANDIDATE_RATIO={len(rows) / len(sexual_speeches):.4f}")
    current_all = read_cp932(CHAR_PATH)
    bare_all = [line for line in current_all.splitlines() if "PRINTFORM" in line and BARE_UNYA_RE.search(line)]
    bare_sexual = [speech for speech in sexual_speeches if BARE_UNYA_RE.search(speech)]
    print(f"BARE_UNYA_ROWS_ALL_PRINTFORM={len(bare_all)}")
    print(f"BARE_UNYA_ROWS_SEXUAL={len(bare_sexual)}")
    print(f"BARE_UNYA_COMMA_ALL={sum('うにゃ、' in line for line in bare_all)}")
    print(f"BARE_UNYA_COMMA_SEXUAL={sum('うにゃ、' in speech for speech in bare_sexual)}")
    print("CURRENT_TERM_COUNTS_ALL_FILE")
    for term in TERMS:
        print(f"{term}\t{current.count(term)}")
    print("CURRENT_TERM_ROW_COUNTS_SEXUAL")
    for term in TERMS:
        print(f"{term}\t{sum(term in speech for speech in sexual_speeches)}")
    print("SOURCE_TERM_COUNTS")
    for term in TERMS:
        print(f"{term}\t{source.count(term)}")
    print("CANDIDATES_BY_CONTEXT")
    context_counts = Counter(f"{row['label']} / COM{row['com']}" for row in rows)
    for context, amount in sorted(context_counts.items()):
        print(f"{context}\t{amount}")
    print("CANDIDATE_LINES")
    for row in rows:
        print(f"{row['line']}\t{row['label']} / COM{row['com']}\tscore={row['score']}\tflags={row['flags']}\t{row['speech']}")


if __name__ == "__main__":
    main()
