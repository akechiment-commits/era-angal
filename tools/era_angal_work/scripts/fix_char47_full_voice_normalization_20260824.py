from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR47_before_full_voice_audit_20260824" / TARGET.name


def normalize_dialogue_line(line: str) -> str:
    if "PRINTFORM" not in line:
        return line

    # 原作でほとんど使われない自己呼称を、原作の一人称へ戻す。
    replacements = [
        ("お姉さんの", "わたしの"),
        ("お姉さんが", "わたしが"),
        ("お姉さんに", "わたしに"),
        ("お姉さんを", "わたしを"),
        ("お姉さんは", "わたしは"),
        ("お姉さんも", "わたしも"),
        ("お姉さん、", "わたし、"),
        ("お姉さん。", "わたし。"),
        ("お姉さんだ", "わたしだ"),
        ("お姉さん", "わたし"),
    ]
    for old, new in replacements:
        line = line.replace(old, new)

    # 原作に少数しかない「よぉ」系の間延びを、意味を変えずに通常の終助詞へ戻す。
    line = line.replace("よぉ～", "よ")
    line = line.replace("よぉ……", "よ……")
    line = line.replace("よぉ", "よ")
    return line


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    lines = [normalize_dialogue_line(line) for line in text.splitlines()]
    output = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(output.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
