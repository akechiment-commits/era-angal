"""CHAR19みけの位置説明の反復を、反応中心へ限定的に分散する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_19_猫塚みけ_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR19_before_position_expository_rewrite_20260913"
BACKUP = BACKUP_DIR / TARGET.name

REPLACEMENTS = {
    1216: (
        "「あっ、んっ……後ろから、ずんずん……っ。うにゃあ、お尻ふりふりしちゃう……やだ、止まらない……」",
        "「あっ、んっ……ずんずん来る……っ。うにゃあ、お尻ふりふりしちゃう……やだ、止まらない……」",
    ),
    1989: (
        "「んっ、あっ……後ろから、深い……っ。うにゃあ、先輩、奥に当たってる……気持ちいい……♪」",
        "「んっ、あっ……深い……っ。うにゃあ、先輩、奥に当たってる……気持ちいい……♪」",
    ),
    2001: (
        "「んん……っ、後ろからだと、声がまんできない……。せ、先輩っ、聞かないで……っ」",
        "「んん……っ、声がまんできない……。せ、先輩っ、聞かないで……っ」",
    ),
    2088: (
        "「にゃあ、後ろから抱えられて……っ。んっ、こ、これも恥ずかしい格好……っ」",
        "「にゃあ、抱えられて……っ。んっ、こ、これも恥ずかしい格好……っ」",
    ),
    2439: (
        "「ん～っ、ちゅ……。後ろから抱きしめられて、キスも……。うにゃあ、しあわせでとろける♪」",
        "「ん～っ、ちゅ……。キスまで重なると……。うにゃあ、しあわせでとろける♪」",
    ),
    2443: (
        "「んっ、ちゅ……。後ろから振り向くの、首いたい……。うにゃ～、でも、嬉しいよぉ……っ」",
        "「んっ、ちゅ……。首いたいくらい顔を近づけて……。うにゃ～、でも、嬉しいよぉ……っ」",
    ),
    2447: (
        "「んむ……っ。後ろから抱えられてキス、子どもみたい……。うにゃ～、でも、好き……っ」",
        "「んむ……っ。抱えられてキス、子どもみたい……。うにゃ～、でも、好き……っ」",
    ),
    2616: (
        "「あっ、んっ……上から動かれると、勝手に感じちゃう……。うにゃっ、こんなの知らない……っ」",
        "「あっ、んっ……動かれると、勝手に感じちゃう……。うにゃっ、こんなの知らない……っ」",
    ),
    2885: (
        "「んっ、後ろから、お尻に……。うにゃあ、けものみたいで、いっぱい感じちゃう……♪」",
        "「んっ、お尻に……。うにゃあ、けものみたいで、いっぱい感じちゃう……♪」",
    ),
    2894: (
        "「にゃあ、後ろからお尻に……っ。こわいけど……んっ、せ、先輩っ、ゆっくりね……っ」",
        "「にゃあ、お尻に……っ。こわいけど……んっ、せ、先輩っ、ゆっくりね……っ」",
    ),
    2933: (
        "「んっ、後ろから抱えられて、お尻に……。うにゃあ、先輩の腕の中で、変になっちゃう……♪」",
        "「んっ、抱えられて、お尻に……。うにゃあ、先輩の腕の中で、変になっちゃう……♪」",
    ),
    2942: (
        "「うにゃあ、後ろから抱えられて、お尻でなんて……っ。んっ、こ、これも恥ずかしい……っ」",
        "「うにゃあ、抱えられて、お尻でなんて……っ。んっ、こ、これも恥ずかしい……っ」",
    ),
}


def main() -> None:
    source = BACKUP if BACKUP.exists() else TARGET
    raw = source.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    if BACKUP.exists() and BACKUP.read_bytes() != raw:
        raise RuntimeError(f"backup exists but is not the untouched source: {BACKUP}")
    for line_number, (old, _new) in REPLACEMENTS.items():
        line = lines[line_number - 1]
        if line.count(old) != 1:
            raise RuntimeError(f"line {line_number}: expected one old phrase, got {line.count(old)}")
    if not BACKUP.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET, BACKUP)
    for line_number, (old, new) in REPLACEMENTS.items():
        line = lines[line_number - 1]
        lines[line_number - 1] = line.replace(old, new, 1)
    TARGET.write_bytes("".join(lines).encode("cp932"))
    print(f"updated {TARGET}")
    print(f"backup {BACKUP}")
    print(f"changed_physical_lines {len(REPLACEMENTS)}")


if __name__ == "__main__":
    main()
