"""CHAR68 COM17の装着・恋人RAND枝に残った同文を差し替える。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_68_深鳥ふみ_COM.ERB"
OLD = "「ん、く、ぁっ……！　勝手に跳ねて、止まらない……っ。こんなあたしを一面に載せていいのは、あんただけよ♪」"
NEW = "「ひぁっ……！　深く来るたび、頭が真っ白になる……っ。原稿も取材も、今だけは忘れさせてよ……あんたのせいなんだから♪」"


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    if text.count(OLD) != 1:
        raise RuntimeError(f"expected one occurrence, got {text.count(OLD)}")
    TARGET.write_bytes(text.replace(OLD, NEW, 1).encode("cp932"))
    print(f"rewrote COM17 RAND branch in {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
