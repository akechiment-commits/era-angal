from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_11_氷野くるみ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR11_COM18_before_rand3_20260828" / TARGET.name


OLD = """;--- COM18 シャワー ---
IF SELECTCOM == 18
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「えへへ、先輩と一緒にシャワー♪　背中、流してあげますね～☆」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「ん……お湯あったかい。先輩と二人だと、お風呂も楽しいです♪」
\tENDIF
ENDIF
"""

NEW = """;--- COM18 シャワー ---
IF SELECTCOM == 18
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\tIF A == 0
\t\t\tPRINTFORMW 「えへへ、先輩と一緒にシャワー♪　背中、流してあげますね～☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「泡をいっぱいにして、先輩の背中もぴかぴかにしちゃいます～♪　保健委員のお手入れです☆」
\t\tELSE
\t\t\tPRINTFORMW 「先輩、流しっこにしましょうよ～☆　わたし、背中を洗ってもらうのも、洗ってあげるのも好きです♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ん……お湯あったかい。先輩と二人だと、お風呂も楽しいです♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、先輩、そこ熱くないですか～？　わたしが温度を見ますね、保健委員ですから～♪」
\t\tELSE
\t\t\tPRINTFORMW 「シャワーの音って落ちつきますね～。このまま湯気にまぎれて、授業までお休みしちゃいそうです……♪」
\t\tENDIF
\tENDIF
ENDIF
"""


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n")
    old = OLD.rstrip("\n")
    new = NEW.rstrip("\n")
    if text.count(old) > 1:
        raise SystemExit("COM18の置換元ブロックが複数あります。中断しました。")
    if old not in text:
        if new in text:
            print("変更済み: COM18")
            return
        raise SystemExit("CHAR11 COM18の想定された置換元ブロックが見つかりません。中断しました。")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    updated = text.replace(old, new, 1)
    TARGET.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("更新: CHAR11 COM18を恋人/通常それぞれRAND:3化")
    print(f"バックアップ: {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
