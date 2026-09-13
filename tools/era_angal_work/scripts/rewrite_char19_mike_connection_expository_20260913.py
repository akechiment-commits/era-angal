"""CHAR19みけの接続状態説明を、猫らしい身体感覚と甘えへ限定的に直す。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_19_猫塚みけ_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR19_before_connection_expository_rewrite_20260913"
BACKUP = BACKUP_DIR / TARGET.name

REPLACEMENTS = {
    1468: (
        "「ん～っ、%LOCALS%とつながってる……。うにゃあ、こんな所なのに、あったかい……えへへ、いっぱい動くね♪」",
        "「ん～っ、%LOCALS%の熱が、ずっと離れない……。うにゃあ、こんな所なのに、あったかい……えへへ、いっぱい動くね♪」",
    ),
    2060: (
        "「あっ、あっ……抱きついたまま、つながって……。うにゃ、先輩とぴったりくっついて、好き……♪」",
        "「あっ、あっ……抱きついたまま、先輩の熱に包まれて……。うにゃ、ぴったりくっついて、好き……♪」",
    ),
    2080: (
        "「んっ、後ろから抱っこされて、つながって……。うにゃあ、先輩の腕の中、安心する……♪」",
        "「んっ、後ろから抱っこされて……。うにゃあ、先輩の腕、ぎゅってしててほしい……♪」",
    ),
    2393: (
        "「ちゅ……あっ。うにゃ、振り向いてキスすると、よけいつながってる感じ……好き……♪」",
        "「ちゅ……あっ。うにゃ、振り向いてキスすると、先輩の息まで近くなる感じ……好き……♪」",
    ),
    2415: (
        "「ん……ちゅ、あっ。先輩の顔、目の前で……。うにゃ、キスしながらつながるの、好き……♪」",
        "「ん……ちゅ、あっ。先輩の顔、目の前で……。うにゃ、キスしながら息が重なるの、好き……♪」",
    ),
    2909: (
        "「んっ、抱きあって、お尻でつながって……。うにゃあ、先輩とぴったり、しあわせ……♪」",
        "「んっ、抱きあって……。うにゃあ、先輩の体温がお尻まで響いて、しあわせ……♪」",
    ),
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    if BACKUP.exists():
        raise RuntimeError(f"backup already exists: {BACKUP}")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    for line_number, (old, new) in REPLACEMENTS.items():
        line = lines[line_number - 1]
        if line.count(old) != 1:
            raise RuntimeError(f"line {line_number}: expected one old phrase, got {line.count(old)}")
        lines[line_number - 1] = line.replace(old, new, 1)
    TARGET.write_bytes("".join(lines).encode("cp932"))
    print(f"updated {TARGET}")
    print(f"backup {BACKUP}")
    print(f"changed_physical_lines {len(REPLACEMENTS)}")


if __name__ == "__main__":
    main()
