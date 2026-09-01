from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_11_氷野くるみ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR11_COM4_before_rand3_20260828" / TARGET.name


OLD = """;--- COM4 フェラする ---
;  ▼【視点】キャラ受け＝プレイヤーがふたなりキャラのペニスをくわえる逆フェラ（キャラはされる側）。通常フェラCOM31と混同するな
;  ※ふたなりパートナーのペニスをプレイヤーがくわえるコマンド
;  ※（プレイヤーが奉仕する側）
IF SELECTCOM == 4
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「ふぇっ、わたしのを先輩のお口で……っ。んっ、もったいないのに、気持ちいい……♪」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「ひゃうっ、咥えちゃだめです先輩～っ。んっ、出ちゃう、お口に出ちゃう……っ♪」
\tENDIF
ENDIF
"""

NEW = """;--- COM4 フェラする ---
;  ▼【視点】キャラ受け＝プレイヤーがふたなりキャラのペニスをくわえる逆フェラ（キャラはされる側）。通常フェラCOM31と混同するな
;  ※ふたなりパートナーのペニスをプレイヤーがくわえるコマンド
;  ※（プレイヤーが奉仕する側）
IF SELECTCOM == 4
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ、わたしのを先輩のお口で……っ。んっ、もったいないのに、気持ちいい……♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「えへへ……先輩のお口、あったかいですね～。わたしのほうが、料理みたいにとろけちゃいそうです……♪」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃうっ、そんなに丁寧にされたら、もう我慢できません～っ。先輩のお口に、ぜんぶ……♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ひゃうっ、咥えちゃだめです先輩～っ。んっ、出ちゃう、お口に出ちゃう……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふぇ、ふぇぇ……先輩、そんなに見上げないでください～っ。お口でされると、力が抜けちゃいますよぉ……」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃううんっ、だめ、だめですってば～っ！　でも、逃げたらもったいないですし……そのまま、お願いします……♪」
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
        raise SystemExit("COM4の置換元ブロックが複数あります。中断しました。")
    if old not in text:
        if new in text:
            print("変更済み: COM4")
            return
        raise SystemExit("CHAR11 COM4の想定された置換元ブロックが見つかりません。中断しました。")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    updated = text.replace(old, new, 1)
    TARGET.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("更新: CHAR11 COM4を恋人/通常それぞれRAND:3化")
    print(f"バックアップ: {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
