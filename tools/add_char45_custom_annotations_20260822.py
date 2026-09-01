from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"

ANNOTATIONS = {
    "IF SELECTCOM == 281": ";--- COM281 兄不在の夜のお誘い ---",
    "IF SELECTCOM == 282": ";--- COM282 薔薇風呂 ---",
    "IF SELECTCOM == 283": ";--- COM283 朝まで腕の中 ---",
    "IF SELECTCOM == 284": ";--- COM284 甘える夜 ---",
    "IF SELECTCOM == 411": ";--- COM411 閉園後の観覧車 ---",
    "IF SELECTCOM == 412": ";--- COM412 メリーゴーランド ---",
    "IF SELECTCOM == 413": ";--- COM413 貸切パレード ---",
    "IF SELECTCOM == 414": ";--- COM414 二人だけの花火 ---",
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
    print("restored CHAR45 custom command annotations")

if __name__ == "__main__":
    main()

