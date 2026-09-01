from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_11_氷野くるみ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR11_COM7_before_rand3_20260828" / TARGET.name


OLD = """;--- COM7 何もしない ---
IF SELECTCOM == 7
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「えへへ、今日はなにもしないんですか？　先輩とこうしてるだけで、しあわせです♪」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「ん～、お休みですね。じゃあ、おしゃべりでもしましょ、先輩♪」
\tENDIF
ENDIF
"""

NEW = """;--- COM7 何もしない ---
IF SELECTCOM == 7
\tA = RAND:3
\tIF TALENT:TARGET:153
\t\tIF A == 0
\t\t\tPRINTFORMW 「えへへ、今日はなにもしないんですか？　先輩とこうしてるだけで、しあわせです♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「何もしない時間も大事ですよ～。先輩のとなり、ぽかぽかして……お野菜さんみたいに根っこが生えちゃいそうです♪」
\t\tELSE
\t\t\tPRINTFORMW 「先輩と一緒なら、穴掘りも料理もお休みです～♪　……でも、手だけはつないでいてくださいね？」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ん～、お休みですね。じゃあ、おしゃべりでもしましょ、先輩♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ん～？　先輩、今日は穴掘りもお料理もお休みですか～？　たまには、こうしてのんびりするのもいいですね♪」
\t\tELSE
\t\t\tPRINTFORMW 「わたし、すぐ動きたくなっちゃうんですけど……先輩のとなりなら、もう少しだけ休んでいきます～♪」
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
        raise SystemExit("COM7の置換元ブロックが複数あります。中断しました。")
    if old not in text:
        if new in text:
            print("変更済み: COM7")
            return
        raise SystemExit("CHAR11 COM7の想定された置換元ブロックが見つかりません。中断しました。")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    updated = text.replace(old, new, 1)
    TARGET.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("更新: CHAR11 COM7を恋人/通常それぞれRAND:3化")
    print(f"バックアップ: {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
