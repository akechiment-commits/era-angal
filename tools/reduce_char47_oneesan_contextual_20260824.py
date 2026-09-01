from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

KEEP_LINES = (
    "わたしのほうがお姉さんだよ？",
    "わたしのほうがお姉さんだよ～……？",
    "わたしのほうが、お姉さんなんだからね？",
    "子供じゃないよ？　お姉さんだよ",
)


def rewrite_line(line: str) -> str:
    if "PRINTFORM" not in line or "お姉さん" not in line:
        return line
    if any(keep in line for keep in KEEP_LINES):
        return line

    # These are semantic rewrites, not blind word substitution: the role word is
    # removed only where it was acting as a repeated self-label.
    replacements = [
        ("お姉さんの威厳が、ぜんぶなくなっちゃう", "みづちゃんに見られたら、一生からかわれちゃう"),
        ("お姉さんの威厳が、台無し", "平気な顔ができない"),
        ("お姉さんの威厳が", "平気なふりができない"),
        ("お、お姉さんの", "わたしの"),
        ("お姉さんの、", "わたしの"),
        ("お姉さんの", "わたしの"),
        ("お姉さんが", "わたしが"),
        ("お姉さんに", "わたしに"),
        ("お姉さんを", "わたしを"),
        ("お姉さんは", "わたしは"),
        ("お姉さんも", "わたしも"),
        ("お姉さん、", "わたし、"),
        ("お姉さん。", "わたし。"),
        ("お姉さんだ", "わたしだ"),
        ("お姉さんなのに", "わたしなのに"),
        ("お姉さん", "わたし"),
    ]
    for old, new in replacements:
        line = line.replace(old, new)

    # Repair sentence shapes exposed by removing the role label.
    line = line.replace("こんなとこでわたしの中いっぱいにして。わたし、", "こんなとこでわたしの中をいっぱいにして。")
    line = line.replace("わたしの身体、", "わたしの身体、")
    line = line.replace("わたしの、", "わたしの")
    line = line.replace("お、わたしの", "わたしの")
    return line


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = [rewrite_line(line) for line in text.splitlines()]
    result = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(result.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
