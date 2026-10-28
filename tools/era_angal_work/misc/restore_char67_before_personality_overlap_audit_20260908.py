"""CHAR67の今回編集前状態を、今回の置換だけ逆変換して再構成する。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rewrite_char67_mashiro_orgasm_duplicates_20260908 as orgasm_rewrite


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR67_before_personality_overlap_audit_20260908/CHAR_67_日滝ましろ_COM.ERB"

SHITEN_REPLACEMENTS = {
    'PRINTFORMW 「ひゃっ、こんなに近いのか！？　うう、触れるたびに声が出るぞ……！」':
        'PRINTFORMW 「ひゃっ、女の子同士でこんなに近く！？　うう、触れるたびに声が出るぞ……！」',
    'PRINTFORMW 「わっ、胸を重ねるのか！？　うう、密着すると鼓動まで聞こえるぞ……！」':
        'PRINTFORMW 「わっ、胸を重ねるのか！？　うう、女の子同士でこんなに密着するとは……！」',
}


def main() -> None:
    data = SOURCE.read_text(encoding="cp932")
    for old, new in orgasm_rewrite.REPLACEMENTS.items():
        if data.count(new) != 1:
            raise RuntimeError(f"expected one edited occurrence, found {data.count(new)}: {new}")
        data = data.replace(new, old)
    for old, new in SHITEN_REPLACEMENTS.items():
        if data.count(old) != 1:
            raise RuntimeError(f"expected one viewpoint occurrence, found {data.count(old)}: {old}")
        data = data.replace(old, new)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"reconstructed {BACKUP}")


if __name__ == "__main__":
    main()
