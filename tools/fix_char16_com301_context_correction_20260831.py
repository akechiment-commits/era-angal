"""CHAR16 COM301へ誤って入れた別場面の台詞を、転校生向け原作表現へ戻す。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_16_大虎いさみ_COM.ERB"
SOURCE = ROOT / "tools/output/いさみ.txt"
BACKUP = ROOT / "tools/backups/CHAR16_before_com301_context_correction_20260831/CHAR_16_大虎いさみ_COM.ERB"

OLD = 'PRINTFORMW 「同じクラスなのに、こうやって話す機会って、ほとんどなかったっすね。これからは、もっと話しましょうよ♪」'
NEW = 'PRINTFORMW 「すみません、愚痴ばかりになっちゃいましたね。ところで、転校生の先輩って好きなゲームとかありますか？」'


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    if not source.startswith("# いさみ（全1346件）"):
        raise RuntimeError("いさみ.txt の原作見出しを確認できません")
    if "すみません、愚痴ばかりになっちゃいましたね。ところで、転校生の先輩って好きなゲームとかありますか？" not in source:
        raise RuntimeError("転校生向けの会話原作表現を確認できません")

    raw = TARGET.read_bytes().decode("cp932")
    count = raw.count(OLD)
    if count == 0:
        if NEW in raw:
            print("変更なし（正しい会話台詞へ修正済み）")
            return 0
        raise RuntimeError("COM301の誤差し替え台詞を確認できません")
    if count != 1:
        raise RuntimeError(f"誤差し替え台詞が想定外の件数: {count}")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_bytes(raw.replace(OLD, NEW).encode("cp932"))
    print("COM301を転校生向け原作会話へ再修正")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
