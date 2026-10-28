from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR47_before_contextual_oneesan_20260824" / TARGET.name


# Role-specific lines grounded in the original: Minazuki pushes back against
# being treated as a child, rather than using "big sister" as a filler label.
KEEP_MARKERS = (
    "わたしのほうがお姉さんだよ？",
    "わたしのほうがお姉さんだよ～……？",
    "わたしのほうが、お姉さんなんだからね？",
    "子供じゃないよ？　お姉さんだよ",
    "ちっちゃいけど、お姉さんなんだからね",
    "おねえさんとデート",
    "おねえさんが、君をエスコート",
    "おねえさんが手を引く",
    "おねえさんとデート、楽しい？",
    "おねえさんが案内する",
    "お姉さんになった気分",
    "色気のないおねえさんで",
)


def rewrite_line(line: str) -> str:
    if "PRINTFORM" not in line:
        return line
    if "お姉さん" not in line and "おねえさん" not in line:
        return line
    if any(marker in line for marker in KEEP_MARKERS):
        return line

    # Sentence-level repairs for phrases where a raw subject swap would be
    # unnatural Japanese.
    replacements = (
        ("えへへ、お姉さん、失格だね？", "えへへ、先輩失格だね？"),
        ("お姉さんの威厳が、ぜんぶなくなっちゃう", "みづちゃんに見られたら、一生からかわれちゃう"),
        ("お姉さんの威厳が、台無しだよぉ", "平気な顔ができないよぉ"),
        ("お姉さんの威厳が、", "平気なふりができない"),
        ("お姉さんのわがまま", "わたしのわがまま"),
        ("お姉さんの、わがまま", "わたしのわがまま"),
        ("お姉さんの、特別な秘密", "わたしだけの特別な秘密"),
        ("お姉さんの、はしたないとこ", "わたしのはしたないとこ"),
        ("お姉さんの、ぜんぶ", "わたしのぜんぶ"),
        ("お姉さんの、受け止めて？", "わたしの中で受け止めて？"),
        ("お姉さんの、ちっちゃい胸", "わたしのちっちゃい胸"),
        ("お姉さんの、お役目", "わたしのお役目"),
        ("お姉さんの、初めて", "わたしの初めて"),
        ("お姉さんの初めて", "わたしの初めて"),
        ("お姉さんの身体", "わたしの身体"),
        ("お姉さんの胸", "わたしの胸"),
        ("お姉さんの手", "わたしの手"),
        ("お姉さんのお口", "わたしのお口"),
        ("お姉さんの口", "わたしの口"),
        ("お姉さんのお腹", "わたしのお腹"),
        ("お姉さんの中", "わたしの中"),
        ("お姉さんの顔", "わたしの顔"),
        ("お姉さんの弱いところ", "わたしの弱いところ"),
        ("お姉さんの意地", "わたしの意地"),
        ("お姉さんの余裕", "わたしの余裕"),
        ("お姉さんの仮面", "わたしの仮面"),
        ("お姉さんのはしたないとこ", "わたしのはしたないとこ"),
        ("お姉さんのが", "わたしのが"),
        ("お姉さんの", "わたしの"),
        ("お姉さんが", "わたしが"),
        ("お姉さんを", "わたしを"),
        ("お姉さんに", "わたしに"),
        ("お姉さんは", "わたしは"),
        ("お姉さんも", "わたしも"),
        ("お姉さん、", "わたし、"),
        ("お姉さん。", "わたし。"),
        ("お姉さんだって", "わたしだって"),
        ("お姉さんなのに", "わたしなのに"),
        ("お姉さんだよって", "先輩だよって"),
        ("お姉さんだよ", "わたしだよ"),
        ("お姉さん", "わたし"),
    )
    for old, new in replacements:
        line = line.replace(old, new)

    repairs = (
        ("お、お姉さんの", "わたしの"),
        ("わたしの、", "わたしの"),
        ("こんなとこでわたしの中いっぱいにして。わたし、", "こんなとこでわたしの中をいっぱいにして。"),
        ("わたしを欲ばりにしないで", "わたしを欲ばりにさせないで"),
        ("ちっちゃいわたしだってば", "わたしだって、ちっちゃいけど先輩なんだから"),
        ("ちっちゃいわたしに可愛がられて", "こんな小さいわたしに可愛がられて"),
    )
    for old, new in repairs:
        line = line.replace(old, new)
    return line


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    lines = [rewrite_line(line) for line in text.splitlines()]
    result = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(result.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
