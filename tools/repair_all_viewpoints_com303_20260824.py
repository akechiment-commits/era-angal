from pathlib import Path
import shutil


ROOT = Path(r"C:\Users\guile\era-angal")
CHAR_DIR = ROOT / "ERB" / "CHAR"
BACKUP_DIR = ROOT / "tools" / "backups" / "ALL_VIEWPOINT_before_COM303_20260824"

REPLACEMENTS = {
    "CHAR_01_三善かなえ_COM.ERB": [
        ('「仕方ありませんねぇ、私が支えてあげましょう……ひゃあ!?」',
         '「仕方ありませんねぇ、転校生さんに支えてもらいましょう……ひゃあ!?」'),
    ],
    "CHAR_04_早川きこ_COM.ERB": [
        ('「あたしが温もりをあげよう、ぎゅうぎゅうっ♪」',
         '「先輩の温もり、ぎゅうぎゅうに感じちゃうっ♪」'),
    ],
    "CHAR_09_月永るか_COM.ERB": [
        ('「ぼ、ぼくがっ、ぼくが抱きしめて『ぬくもり』を……くしゅんっ☆」',
         '「せ、先輩に抱きしめられて『ぬくもり』を……くしゅんっ☆」'),
    ],
    "CHAR_43_砂賀みどり_COM.ERB": [
        ('「ほら、わたしが拭いてあげる。このタオル、天然素材１００％なんだよ～♪」',
         '「ほら、転校生くんが拭いてくれる。このタオル、天然素材１００％なんだよ～♪」'),
    ],
    "CHAR_71_棗ひびき_COM.ERB": [
        ('「ふふ、甘えん坊っちね。ういうい、うちがぎゅ～ってしてあげるっち♪」',
         '「ふふ、甘えん坊っちね。ういうい、うちもぎゅ～ってしてもらうっち♪」'),
        ('「がんばり屋さんの転校生くんを、うちがたっぷり癒やしてあげるっち……♪」',
         '「がんばり屋さんの転校生くんに、うちもたっぷり癒やしてもらうっち……♪」'),
    ],
}


def main() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for filename, pairs in REPLACEMENTS.items():
        target = CHAR_DIR / filename
        backup = BACKUP_DIR / filename
        if not backup.exists():
            shutil.copy2(target, backup)
        text = target.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
        for old, new in pairs:
            if text.count(old) != 1:
                raise RuntimeError(f"{filename}: replacement count for {old!r} is {text.count(old)}")
            text = text.replace(old, new, 1)
        target.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
        print(f"updated {filename}: {len(pairs)}")


if __name__ == "__main__":
    main()
