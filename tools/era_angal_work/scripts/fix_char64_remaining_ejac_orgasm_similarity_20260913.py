"""CHAR64しおんの射精・絶頂群に残った2組の近似を追加調整する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_64_峰山しおん_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR64_before_remaining_ejac_orgasm_similarity_fix_20260913"
BACKUP = BACKUP_DIR / TARGET.name

REPLACEMENTS = {
    5503: (
        "「ぁ、…ふっ、はぁ、…乳首も、お尻も、…もう、どこから声が出ているのか……」",
        "「ぁ、…ふっ、はぁ、…もう、胸もお尻も、君の手を探してしまう……っ」",
    ),
    5604: (
        "「ぁ、…はぁ、お腹の奥に、君のものは、なかなかの存在感だね、まったく」",
        "「ぁ、…はぁ、もう返事をする余裕もないね、まったく」",
    ),
    5610: (
        "「あぁ、…はぁ、お腹の奥に、君のものは、ヘラクレスの逸物並みじゃないか、少年」",
        "「あぁ、…はぁ、腰が勝手に跳ねるじゃないか、少年。こんな反応まで見せるとは、私も参ったよ」",
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
