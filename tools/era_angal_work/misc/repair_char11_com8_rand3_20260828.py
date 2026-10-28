from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_11_氷野くるみ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR11_COM8_before_rand3_20260828" / TARGET.name


OLD = """;--- COM8 指挿入れ ---
IF SELECTCOM == 8
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「ん、んっ……先輩の指、中で動いて……。気持ちよくて、とろけちゃう……♪」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「ひゃうっ、指、奥まで……っ。んっ、ぐちゅぐちゅ言ってる～……っ♪」
\tENDIF
ENDIF
"""

NEW = """;--- COM8 指挿入れ ---
IF SELECTCOM == 8
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\tIF A == 0
\t\t\tPRINTFORMW 「ん、んっ……先輩の指、中で動いて……。気持ちよくて、とろけちゃう……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あっ、指が触れるたび、奥がきゅっとしちゃいます～……。先輩、ゆっくりでお願いします♪」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃうっ、そんなところまで届いちゃうんですか～っ？　わたし、もう声を抑えられません……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ひゃうっ、指、奥まで……っ。んっ、ぐちゅぐちゅ言ってる～……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぇっ、指を入れるんですか先輩～っ。まだ心の準備が……あっ、ゆっくりなら……」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃううんっ、奥を刺激しないでください～っ！　……でも、気持ちいいから、止めないでください……♪」
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
        raise SystemExit("COM8の置換元ブロックが複数あります。中断しました。")
    if old not in text:
        if new in text:
            print("変更済み: COM8")
            return
        raise SystemExit("CHAR11 COM8の想定された置換元ブロックが見つかりません。中断しました。")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    updated = text.replace(old, new, 1)
    TARGET.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("更新: CHAR11 COM8を恋人/通常それぞれRAND:3化")
    print(f"バックアップ: {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
