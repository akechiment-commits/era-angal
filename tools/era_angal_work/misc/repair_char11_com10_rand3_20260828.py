from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_11_氷野くるみ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR11_COM10_before_rand3_20260828" / TARGET.name


OLD = """;--- COM10 ローター ---
IF SELECTCOM == 10
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「ひゃうっ、ブーンって……っ。んっ、当てられると、腰くだけちゃう……♪」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「あぅ、震えるおもちゃ、ずるい～っ。んっ、勝手にいっちゃう……っ♪」
\tENDIF
ENDIF
"""

NEW = """;--- COM10 ローター ---
IF SELECTCOM == 10
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\tIF A == 0
\t\t\tPRINTFORMW 「ひゃうっ、ブーンって……っ。んっ、当てられると、腰くだけちゃう……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃうっ、そこに当てるんですか～っ？　振動が細かくて、身体の奥までびりびりします……♪」
\t\tELSE
\t\t\tPRINTFORMW 「んんっ、だめです、そんなに続けたら……っ。わたし、力が入らなくなって、先輩にしがみついちゃいます～……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「あぅ、震えるおもちゃ、ずるい～っ。んっ、勝手にいっちゃう……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、あぅ……そのおもちゃ、思ったより強いです～っ。お腹までぶるぶるして、変な感じ……」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃううんっ、先輩、そこに当て続けるんですか～っ？　ぶるぶるで、わたし、まともに立てません～っ♪」
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
        raise SystemExit("COM10の置換元ブロックが複数あります。中断しました。")
    if old not in text:
        if new in text:
            print("変更済み: COM10")
            return
        raise SystemExit("CHAR11 COM10の想定された置換元ブロックが見つかりません。中断しました。")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    updated = text.replace(old, new, 1)
    TARGET.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("更新: CHAR11 COM10を恋人/通常それぞれRAND:3化")
    print(f"バックアップ: {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
