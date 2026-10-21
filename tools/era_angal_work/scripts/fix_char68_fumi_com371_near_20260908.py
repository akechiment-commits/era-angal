"""CHAR68 COM371の近似定型を新聞部長の羞恥表現へ差し替える。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_68_深鳥ふみ_COM.ERB"
OLD = "「はぁ……っ、恥ずかしい……。でも、あんたが望むなら……ん、特別よ……っ」"
NEW = "「はぁ……っ、こんな記事にできない姿……。あんた、目を逸らさないでよね。……特別に見せてるんだから」"


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    if text.count(OLD) != 1:
        raise RuntimeError(f"expected one occurrence, got {text.count(OLD)}")
    TARGET.write_bytes(text.replace(OLD, NEW, 1).replace("\n", "\r\n").encode("cp932"))
    print(f"rewrote COM371 line in {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
