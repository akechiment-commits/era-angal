from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    replacements = {
        '「。良い子だね、転校生くん」': '「良い子だね、転校生くん」',
        '「。あぁ、やっぱり落ちつくなぁ」': '「あぁ、やっぱり落ちつくなぁ」',
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise SystemExit(f"artifact not found exactly once: {old}")
        text = text.replace(old, new, 1)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
