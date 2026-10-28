"""CHAR20しずくの性的口上について、説明調・科学語・音楽語彙の密度を監査する。"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
CHAR = next((ROOT / "ERB" / "CHAR").glob("CHAR_20_*_COM.ERB"))
SOURCE = ROOT / "tools" / "output" / "しずく.txt"

HEADER_RE = re.compile(r";---\s*COM(\d+)\s*(.*?)\s*---")
SEX_RE = re.compile(
    r"正常位|後背位|騎乗位|対面座位|背面座位|性交|セックス|アナル|フェラ|クンニ|"
    r"自慰|手淫|キス|愛撫|絶頂|射精|着衣|挿入|中出し|精液|口内|乳房|乳首|"
    r"指入れ|玩具|オナニー|潮吹き|顔面騎乗|パイズリ|素股|ローター|媚薬|利尿剤|"
    r"バイブ|クリ|ニプル|搾乳器|オナホール|クスコ|浣腸器|ボールギャグ|口移し|"
    r"拘束|口枷|羞恥プレイ|言葉責め|衣装破り|胸|尻|陰部|素股|乳|貝あわせ|"
    r"足コキ|カメラ|放尿|おむつ|デッサン"
)
POSITION_RE = re.compile(
    r"正常位|後背位|騎乗位|対面座位|背面座位|振り向いて|繋がって|つながって|"
    r"繋がる|つながる|後ろから|前から|上から|下から|背中から|向かい合って|"
    r"背面で|正面から"
)
META_RE = re.compile(
    r"説明|実況|手順|観察|観測|データ|情報量|処理能力|処理でき|処理、|処理が|難易度|生理現象|実験|"
    r"行為者|攻める側|挿入する側|見る側|受け手|分析|実証|構図的"
)


def main() -> None:
    lines = CHAR.read_bytes().decode("cp932").splitlines()
    source = SOURCE.read_bytes().decode("utf-8").splitlines()
    current_com = ""
    current_sex = False
    sexual_lines: list[tuple[int, str, str]] = []
    for line_no, line in enumerate(lines, 1):
        match = HEADER_RE.search(line)
        if match:
            current_com = match.group(1)
            current_sex = bool(SEX_RE.search(match.group(2)))
        if current_sex and "PRINTFORM" in line:
            sexual_lines.append((line_no, current_com, line.split("PRINTFORM", 1)[1].strip()))

    print(f"FILE {CHAR.name}")
    print(f"SEXUAL_PRINTFORM {len(sexual_lines)}")
    keys = (
        "パパ", "先輩", "ん～", "ふぅ", "ドラム", "音楽", "説明", "観察", "データ",
        "情報量", "処理", "難易度", "主導権", "正常位", "後背位", "騎乗位", "対面座位",
        "背面座位", "繋がって", "つながって", "後ろから", "振り向いて", "上から", "下から",
        "正面から", "構図", "モチーフ", "俺", "押忍", "ふむ",
    )
    print("CURRENT_SEXUAL_COUNTS")
    for key in keys:
        print(f"  {key}: {sum(key in text for _, _, text in sexual_lines)}")
    print("SOURCE_ALL_COUNTS")
    for key in keys:
        print(f"  {key}: {sum(key in text for text in source)}")

    suspects = []
    for line_no, com, speech in sexual_lines:
        score = (3 if POSITION_RE.search(speech) else 0) + (4 if META_RE.search(speech) else 0)
        if score >= 3:
            suspects.append((score, line_no, com, speech))
    suspects.sort(key=lambda row: (-row[0], row[1]))
    print(f"EXPOSITORY_CANDIDATES {len(suspects)}")
    for score, line_no, com, speech in suspects:
        print(f"{score}\t{line_no}\tCOM{com}\t{speech}")

    by_com: dict[str, list[str]] = {}
    for _, com, speech in sexual_lines:
        by_com.setdefault(com, []).append(speech)
    print("DENSE_COMS")
    for com, speeches in sorted(by_com.items(), key=lambda item: int(item[0])):
        meta = sum(bool(META_RE.search(speech)) for speech in speeches)
        positional = sum(bool(POSITION_RE.search(speech)) for speech in speeches)
        if meta >= 2 or positional >= 2:
            print(f"  COM{com}: total={len(speeches)} meta={meta} position={positional}")


if __name__ == "__main__":
    main()
