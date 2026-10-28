"""CHAR64 峰山しおんの性交系説明調・文学比喩密度を監査する。"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAR_PATH = ROOT / "ERB" / "CHAR" / "CHAR_64_峰山しおん_COM.ERB"
SOURCE_PATH = ROOT / "tools" / "output" / "しおん.txt"
HEADER_RE = re.compile(r";---\s*COM(\d+)\s*(.*?)\s*---")
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
    r"行為者|攻める側|挿入する側|見る側|受け手|主導権"
)
SEX_LABEL_RE = re.compile(r"^@CHAR_(?:VIRGIN|FIRST_KISS|UNDRESS|EJAC|ORGASM)_64\b")
LITERARY_RE = re.compile(
    r"文学|物語|読者|傑作|作品|小説|詩|章|頁|ページ|筋書き|序章|終章|"
    r"台本|戯曲|ドラマ|モチーフ|比喩|一節|登場人物|舞台|幕"
)
REACTION_RE = re.compile(
    r"ん|あ|っ|声|息|熱|痛|気持|感じ|恥|震|濡|漏れ|喘|快|"
    r"ゆっくり|もっと|お願い|して|しないで|離れないで|好き|怖|苦し|"
    r"止まって|止めて|かわい|可愛|だいすき|震え|崩れ"
)
TERMS = (
    "ふむ", "ほほう", "失敬", "重畳", "たまえ", "少年", "転校生くん", "色男",
    "文学", "物語", "観察", "観測", "説明", "実況", "データ", "情報量", "難易度",
    "処理", "主導権", "繋がって", "つながって", "後ろから", "上から", "下から",
)


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932")


def collect_current() -> tuple[
    list[dict[str, object]], Counter[str], Counter[int], list[str], list[dict[str, object]]
]:
    text = read_cp932(CHAR_PATH)
    rows: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    com_counts: Counter[str] = Counter()
    sexual_speeches: list[str] = []
    sexual_rows: list[dict[str, object]] = []
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
        counts["sexual_printform"] += 1
        sexual_speeches.append(speech)
        sexual_rows.append({
            "line": lineno,
            "com": current_com or -1,
            "label": current_label,
            "speech": speech,
        })
        score = 0
        flags: list[str] = []
        if POSITION_RE.search(speech):
            score += 3
            flags.append("position")
        if META_RE.search(speech):
            score += 4
            flags.append("meta")
        if LITERARY_RE.search(speech):
            flags.append("literary")
        if REACTION_RE.search(speech):
            flags.append("reaction")
        if re.match(r"[\t ]*PRINTFORM\w*\s*[「『]?\s*(?:後ろ|前|上|下|背中|向かい|振り向|繋が|つなが)", line):
            score += 2
            flags.append("opening_position")
        if score >= 3:
            counts["candidate"] += 1
            context = f"{current_label} / COM{current_com or -1}"
            com_counts[context] += 1
            rows.append({
                "line": lineno,
                "com": current_com or -1,
                "label": current_label,
                "title": current_title,
                "speech": speech,
                "score": score,
                "flags": ",".join(flags),
            })
    return rows, counts, com_counts, sexual_speeches, sexual_rows


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    rows, counts, com_counts, sexual_speeches, sexual_rows = collect_current()
    current = read_cp932(CHAR_PATH)
    source = SOURCE_PATH.read_text(encoding="utf-8")
    source_rows = source.splitlines()
    source_dialogue_rows = [line for line in source_rows if re.match(r"^\[\d+\]", line)]
    sexual_text_all = "\n".join(sexual_speeches)
    sexual_text = "\n".join(str(row["speech"]) for row in rows)

    print("CHAR64_SHION_EXPOSITORY_AUDIT")
    print(f"CURRENT_FILE={CHAR_PATH}")
    print(f"SOURCE_FILE={SOURCE_PATH}")
    print(f"SEXUAL_PRINTFORM={counts['sexual_printform']}")
    print(f"EXPOSITORY_CANDIDATES={counts['candidate']}")
    ratio = counts["candidate"] / counts["sexual_printform"] if counts["sexual_printform"] else 0
    print(f"CANDIDATE_RATIO={ratio:.4f}")
    print("\nCURRENT_TERM_COUNTS_IN_ALL_FILE")
    for term in TERMS:
        print(f"{term}\t{current.count(term)}")
    print("\nCURRENT_TERM_ROW_COUNTS_IN_SEXUAL")
    for term in TERMS:
        print(f"{term}\t{sum(term in speech for speech in sexual_speeches)}")
    print("\nCURRENT_TERM_OCCURRENCES_IN_SEXUAL")
    for term in TERMS:
        print(f"{term}\t{sexual_text_all.count(term)}")
    print("\nLITERARY_ROWS_IN_SEXUAL_BY_CONTEXT")
    literary_rows = [row for row in sexual_rows if LITERARY_RE.search(str(row["speech"]))]
    literary_com_counts = Counter(
        f"{row['label']} / COM{row['com']}" for row in literary_rows
    )
    print(f"rows={len(literary_rows)} occurrences={sum(str(row['speech']).count('文学') for row in literary_rows)}")
    for context, amount in sorted(literary_com_counts.items()):
        print(f"{context}\t{amount}")
    print("LITERARY_ROW_SAMPLES")
    for row in literary_rows[:40]:
        print(f"{row['line']}\t{row['label']} / COM{row['com']}\t{row['speech']}")
    print("\nCURRENT_TERM_COUNTS_IN_CANDIDATES")
    for term in TERMS:
        print(f"{term}\t{sexual_text.count(term)}")
    print("\nSOURCE_TERM_COUNTS")
    for term in TERMS:
        print(f"{term}\t{source.count(term)}")
    print("\nSOURCE_PROFILE_ROWS")
    source_literary = [line for line in source_dialogue_rows if LITERARY_RE.search(line)]
    print(f"lines={len(source_dialogue_rows)} literary_rows={len(source_literary)}")
    for term in ("少年", "たまえ", "文学", "物語", "観察", "観測"):
        print(f"{term}\t{sum(term in line for line in source_dialogue_rows)}")
    print("\nCANDIDATES_BY_COM")
    for context, amount in sorted(com_counts.items()):
        print(f"{context}\t{amount}")
    print("\nCANDIDATE_LINES")
    for row in rows:
        print(
            f"{row['line']}\tCOM{row['com']}\tscore={row['score']}\tflags={row['flags']}\t"
            f"{row['label']} / COM{row['com']}\t{row['speech']}"
        )


if __name__ == "__main__":
    main()
