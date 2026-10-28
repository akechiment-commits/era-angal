"""CHAR16 COM301会話に混入した部長向け台詞を状況に合う文へ直す。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_16_大虎いさみ_COM.ERB"
SOURCE = ROOT / "tools/output/いさみ.txt"
BACKUP = ROOT / "tools/backups/CHAR16_before_com301_context_20260831/CHAR_16_大虎いさみ_COM.ERB"

OLD = 'PRINTFORMW 「お、押忍！　すごいっすね部長！　さすがです、部長～♪」'
NEW = 'PRINTFORMW 「同じクラスなのに、こうやって話す機会って、ほとんどなかったっすね。これからは、もっと話しましょうよ♪」'


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    if not source.startswith("# いさみ（全1346件）"):
        raise RuntimeError("いさみ.txt の原作見出しを確認できません")
    if "同じクラスなのにこうやって話す機会って、ほとんどなかったね？" not in source:
        raise RuntimeError("会話用の原作表現を確認できません")

    raw = TARGET.read_bytes().decode("cp932")
    count = raw.count(OLD)
    if count == 0:
        print("変更なし（対象台詞はすでに除去済み）")
        return 0
    if count != 1:
        raise RuntimeError(f"対象台詞が想定外の件数: {count}")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_bytes(raw.replace(OLD, NEW).encode("cp932"))
    print("COM301の部長向け台詞を会話向けの台詞へ修正")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
