from pathlib import Path
import shutil


ROOT = Path(r"C:\Users\guile\era-angal")
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_65_時国そら_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR65_before_blindfold_gag_viewpoint_20260824"


def main() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / TARGET.name
    if not backup.exists():
        shutil.copy2(TARGET, backup)

    # 既存のCRLFを二重化しないよう、バックアップを入力にして改行を一度正規化する。
    source = backup if backup.exists() else TARGET
    raw = source.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n").replace("\r", "\n")

    replacements = {
        # COM130: そらがPLAYERに目隠しを付ける。省略主語をPLAYER側に固定する。
        '「目を隠しても、嫌ならすぐ外すよ。まだ、あなたを困らせたいわけじゃない」':
            '「あなたの目を隠しても、嫌ならすぐ外すよ。まだ、あなたを困らせたいわけじゃない」',
        '「見えないと不安だよね……わたしの声を頼りにして」':
            '「あなたはもう見えないね。不安なら……わたしの声を頼りにして」',
        # COM131も省略主語を残さず、拘束されているのがPLAYERだと固定する。
        '「ひゃ……っ。動けないんだね……。苦しかったら、ゆん、ゆん……って返して。わたし、すぐにほどくから……」':
            '「ひゃ……っ。あなた、動けないんだね……。苦しかったら、ゆん、ゆん……って返して。わたし、すぐにほどくから……」',
        '「きつくない？　わたしの手加減で、苦しくなってない？」':
            '「あなた、きつくない？　わたしの手加減で、苦しくなってない？」',
        '「動けなくても、目で分かるね……嫌ならすぐ首を振って」':
            '「あなたは動けなくても、目で分かるね……嫌ならすぐ首を振って」',
        # COM132: そらがPLAYERに口枷を付ける。そら自身が口を塞がれる文にしない。
        '「口を塞ぐと、目だけがよく見えるね……何を言いたいのか、聞かせて♪」':
            '「あなたの口を塞ぐと、目だけがよく見えるね……何を言いたいのか、聞かせて♪」',
        '「声が出ないぶん、指を握ってくれる？　わたしに伝わるように」':
            '「声が出ないあなたは、指を握ってくれる？　わたしに伝わるように」',
    }

    for old, new in replacements.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"replacement count for {old!r}: {count}")
        text = text.replace(old, new, 1)

    # 受け側の既存COMと、攻め側の追加COMを注釈でも明確に分離する。
    annotations = {
        ';--- COM43 アイマスク ---\n':
            ';--- COM43 アイマスク ---\n'
            ';  ▼【視点】キャラ受け＝PLAYERがそらにアイマスクを着ける（そらが目隠しされる側）\n'
            ';  ※COM130（そらがPLAYERに目隠し）と混同しない\n',
        ';--- COM44 縄 ---\n':
            ';--- COM44 縄 ---\n'
            ';  ▼【視点】キャラ受け＝PLAYERがそらを縄で拘束する（そらが拘束される側）\n'
            ';  ※COM131（そらがPLAYERを拘束）と混同しない\n',
        ';--- COM45 ボールギャグ ---\n':
            ';--- COM45 ボールギャグ ---\n'
            ';  ▼【視点】キャラ受け＝PLAYERがそらにボールギャグを装着する（そらが口枷される側）\n'
            ';  ※COM132（そらがPLAYERに口枷）と混同しない\n',
    }
    for old, new in annotations.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"annotation count for {old!r}: {count}")
        text = text.replace(old, new, 1)

    # 既存ファイルの改行規約を保持する。
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"updated: {TARGET}")
    print(f"backup:  {backup}")
    print(f"replacements: {len(replacements)}")
    print("annotations: COM43/44/45")


if __name__ == "__main__":
    main()
