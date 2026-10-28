from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_11_氷野くるみ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR11_COM9_before_rand3_20260828" / TARGET.name


OLD = """;--- COM9 アナル舐め ---
IF SELECTCOM == 9
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「ふぇっ、後ろを舐めるなんて……っ。んっ、汚いのに、ぞくぞくします……♪」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「ひゃうっ、舌が後ろに……っ。やぁん、そんなとこ～……っ♪」
\tENDIF
ENDIF
"""

NEW = """;--- COM9 アナル舐め ---
IF SELECTCOM == 9
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ、後ろを舐めるなんて……っ。んっ、汚いのに、ぞくぞくします……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぇぇ……先輩の舌が、こんな後ろまで……。ぞくぞくして、足に力が入りません～……♪」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃううんっ、そこ、そんなに丁寧に舐めないでください～っ！　……恥ずかしいのに、もっとって思っちゃいます……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ひゃうっ、舌が後ろに……っ。やぁん、そんなとこ～……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぇっ、先輩、後ろはまだ慣れてないです～っ。舌が触れるたび、びっくりしちゃいますよぉ……」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃうっ、そんなところまで舐めるんですか～っ!?　お、お野菜さんにも見せられないです……でも、逃げられません～っ♪」
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
        raise SystemExit("COM9の置換元ブロックが複数あります。中断しました。")
    if old not in text:
        if new in text:
            print("変更済み: COM9")
            return
        raise SystemExit("CHAR11 COM9の想定された置換元ブロックが見つかりません。中断しました。")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    updated = text.replace(old, new, 1)
    TARGET.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("更新: CHAR11 COM9を恋人/通常それぞれRAND:3化")
    print(f"バックアップ: {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
