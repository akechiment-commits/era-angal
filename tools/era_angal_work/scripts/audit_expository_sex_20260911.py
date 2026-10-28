"""全CHARの性交・性的口上から、行為説明に寄った文を抽出する。"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAR_DIR = ROOT / "ERB" / "CHAR"
HEADER_RE = re.compile(r";---\s*COM(\d+)\s*(.*?)\s*---")
SEX_RE = re.compile(
    r"正常位|後背位|騎乗位|対面座位|背面座位|性交|セックス|アナル|フェラ|クンニ|"
    r"自慰|手淫|キス|愛撫|絶頂|射精|着衣|挿入|中出し|精液|口内|乳房|乳首|"
    r"指入れ|玩具|オナニー|潮吹き|顔面騎乗"
)
POSITION_RE = re.compile(
    r"正常位|後背位|騎乗位|対面座位|背面座位|振り向いて|繋がって|つながって|"
    r"繋がる|つながる|後ろから|前から|上から|下から|背中から|向かい合って|"
    r"背面で|正面から"
)
META_RE = re.compile(
    r"説明|実況|手順|観察|観測|データ|情報量|処理|難易度|生理現象|実験|"
    r"行為者|攻める側|挿入する側|見る側|受け手"
)
REACTION_RE = re.compile(
    r"ん|あ|っ|声|息|熱|痛|気持|感じ|恥|震|濡|漏れ|ゆっくり|もっと|"
    r"お願い|して|しないで|離れないで|好き|怖|苦し|止まって|止めて|"
    r"かわい|可愛|だいすき|好き"
)


def main() -> None:
    per_char: dict[str, dict[str, object]] = {}
    all_rows: list[tuple[int, str, int, str, str, int]] = []
    for path in sorted(CHAR_DIR.glob("CHAR_*_COM.ERB")):
        text = path.read_bytes().decode("cp932")
        current_com = None
        current_title = ""
        current_sex = False
        total = 0
        suspect = 0
        rows: list[tuple[int, int, str, int]] = []
        for lineno, line in enumerate(text.splitlines(), 1):
            match = HEADER_RE.search(line)
            if match:
                current_com = int(match.group(1))
                current_title = match.group(2)
                current_sex = bool(SEX_RE.search(current_title))
            if not current_sex or "PRINTFORM" not in line:
                continue
            total += 1
            speech = line.split("PRINTFORM", 1)[1]
            score = 0
            if POSITION_RE.search(speech):
                score += 3
            if META_RE.search(speech):
                score += 4
            if re.match(r"[\t ]*PRINTFORM\w*\s*[「『]?\s*(?:後ろ|前|上|下|背中|向かい|振り向|繋が|つなが)", line):
                score += 2
            if score >= 3:
                suspect += 1
                rows.append((lineno, current_com or -1, speech.strip(), score))
                all_rows.append((score, path.name, lineno, current_title, speech.strip(), total))
        if total:
            per_char[path.name] = {"total": total, "suspect": suspect, "rows": rows}

    ranked = sorted(
        ((int(v["suspect"]) / int(v["total"]), name, v) for name, v in per_char.items()),
        reverse=True,
    )
    print("CHAR SEXUAL_EXPOSITORY_AUDIT")
    print("name\\tsexual_printform\\tsuspect\\tratio")
    for ratio, name, value in ranked:
        print(f"{name}\\t{value['total']}\\t{value['suspect']}\\t{ratio:.3f}")
    print("\\nTOP_SUSPECT_LINES")
    for score, name, lineno, title, speech, _ in sorted(all_rows, reverse=True)[:240]:
        print(f"{score}\\t{name}:{lineno}\\tCOM_TITLE={title}\\t{speech}")


if __name__ == "__main__":
    main()
