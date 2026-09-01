"""CHAR61 COM196の追加分岐で、装着者を女性助手として明示する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB" / "CHAR" / "CHAR_61_鶴海ひまり_COM.ERB"
OLD = "「えっ、なにっ、その道具を私に!?　ふぁ、急に来るなあ、会長命令だぞおっ」"
NEW = "「えっ、なにっ、%LOCALS%の道具を私に!?　ふぁ、急に来るなあ、会長命令だぞおっ」"
OLD_META = NEW
NEW_META = "「えっ、なにっ、%LOCALS%の道具を私に!?　ふぁ、急に来るなあ、会長の声を聞けおっ」"


def main() -> None:
    raw = COM_PATH.read_bytes().decode("cp932")
    if NEW_META in raw:
        print("COM196の視点補修は適用済みです。")
        return
    if raw.count(NEW) == 1:
        COM_PATH.write_bytes(raw.replace(OLD_META, NEW_META).encode("cp932"))
        print("CHAR61 COM196の解説調メタ表現を反応表現に補正しました。")
        return
    if raw.count(OLD) != 1:
        raise RuntimeError(f"COM196補修対象の一致数が1ではありません: {raw.count(OLD)}")
    COM_PATH.write_bytes(raw.replace(OLD, NEW).encode("cp932"))
    print("CHAR61 COM196の装着者表現を女性助手に補正しました。")


if __name__ == "__main__":
    main()
