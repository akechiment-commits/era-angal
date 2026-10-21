"""CHAR63 COM194の女性助手呼称を、視点どおり%LOCALS%へ統一する。"""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_63_八雲ちづる_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR63_before_assistant_viewpoint_20260904/CHAR_63_八雲ちづる_COM.ERB"


def main() -> int:
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    start = text.index(";--- COM194")
    end = text.index(";--- COM", start + len(";--- COM194"))
    block = text[start:end]
    count = block.count("きみ")
    if count == 0:
        if "%LOCALS%" not in block:
            raise ValueError("CHAR63 COM194に助手呼称も%LOCALS%もありません")
        print("CHAR63 COM194: 変更なし")
        return 0
    block = block.replace("きみ", "%LOCALS%")
    TARGET.write_bytes((text[:start] + block + text[end:]).replace("\n", "\r\n").encode("cp932"))
    print(f"CHAR63 COM194: 女性助手呼称を%LOCALS%へ {count}件補正")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
