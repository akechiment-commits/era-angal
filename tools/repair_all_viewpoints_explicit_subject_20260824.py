from pathlib import Path
import shutil


ROOT = Path(r"C:\Users\guile\era-angal")
CHAR_DIR = ROOT / "ERB" / "CHAR"
BACKUP_DIR = ROOT / "tools" / "backups" / "ALL_VIEWPOINT_before_explicit_subject_20260824"

REPLACEMENTS = {
    "CHAR_46_双葉みづき_COM.ERB": [
        ('「目隠しされてると不安か？　なら手を出せ。わたしがここにいるって、ちゃんと分からせてやる♪」',
         '「おまえ、目隠しされてると不安か？　なら手を出せ。わたしがここにいるって、ちゃんと分からせてやる♪」'),
    ],
    "CHAR_56_八壁ひかる_COM.ERB": [
        ('「んっ……縛られると、触られる場所へ意識が集まるだろ。俺がゆっくり確かめてやる……っ」',
         '「んっ……おまえ、縛られると、触られる場所へ意識が集まるだろ。俺がゆっくり確かめてやる……っ」'),
    ],
    "CHAR_60_瀬川かえで_COM.ERB": [
        ('「口を塞がれて、目だけで訴えるのね……ふふん、可愛い玩具じゃない♪」',
         '「あんたは口を塞がれて、目だけで訴えるのね……ふふん、可愛い玩具じゃない♪」'),
    ],
    "CHAR_64_峰山しおん_COM.ERB": [
        ('「縛られても平気な顔をするとはね。だが、指先は正直だよ」',
         '「君は縛られても平気な顔をするとはね。だが、指先は正直だよ」'),
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
