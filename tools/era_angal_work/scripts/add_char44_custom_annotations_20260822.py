from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_44_笹芽ひよの_COM.ERB"

ANNOTATIONS = {
    "IF SELECTCOM == 281": ";--- COM281 締め切り明けの部室 ---",
    "IF SELECTCOM == 282": ";--- COM282 部長不在の部室 ---",
    "IF SELECTCOM == 283": ";--- COM283 暗室 ---",
    "IF SELECTCOM == 284": ";--- COM284 猫マオとソファ ---",
    "IF SELECTCOM == 411": ";--- COM411 フォンダンショコラ ---",
    "IF SELECTCOM == 412": ";--- COM412 窓際のお茶 ---",
    "IF SELECTCOM == 413": ";--- COM413 食べ歩き取材 ---",
    "IF SELECTCOM == 414": ";--- COM414 帰り道 ---",
}

def main() -> None:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    for selector, annotation in ANNOTATIONS.items():
        if annotation in text:
            continue
        anchor = selector + "\n"
        if text.count(anchor) != 1:
            raise SystemExit(f"selector is not unique: {selector}")
        text = text.replace(anchor, annotation + "\n" + anchor, 1)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("restored CHAR44 custom command annotations")

if __name__ == "__main__":
    main()

