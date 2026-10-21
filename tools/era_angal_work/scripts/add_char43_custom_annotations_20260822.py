from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_43_砂賀みどり_COM.ERB"

ANNOTATIONS = {
    "ELSEIF SELECTCOM == 411": ";--- COM411 温室で一緒に水やり ---",
    "ELSEIF SELECTCOM == 412": ";--- COM412 植物園めぐり ---",
    "ELSEIF SELECTCOM == 413": ";--- COM413 日向ぼっこピクニック ---",
    "ELSEIF SELECTCOM == 414": ";--- COM414 みどりのかき氷 ---",
}

def main() -> None:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    if ";--- COM410-414 独自純愛 ---" not in text:
        anchor = "IF SELECTCOM == 410\n"
        if text.count(anchor) != 1:
            raise SystemExit("COM410 anchor is not unique")
        text = text.replace(anchor, ";--- COM410-414 独自純愛 ---\n" + anchor, 1)
    for selector, annotation in ANNOTATIONS.items():
        if annotation in text:
            continue
        anchor = selector + "\n"
        if text.count(anchor) != 1:
            raise SystemExit(f"selector is not unique: {selector}")
        text = text.replace(anchor, annotation + "\n" + anchor, 1)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("restored CHAR43 COM410-414 annotations")

if __name__ == "__main__":
    main()
