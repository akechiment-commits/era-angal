"""現行CHAR68から今回の4行だけを逆変換し、監査前バックアップを作る。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_68_深鳥ふみ_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR68_before_personality_overlap_audit_20260908/CHAR_68_深鳥ふみ_COM.ERB"

REPLACEMENTS = {
    "「ふふ、目を閉じてなさい。見えないなら、あたしの声が手がかりよ……逃げちゃだめだからね♪」":
        "「ふふ、あんたの目を隠すわ。見えないぶん、あたしの声だけ追いなさい♪」",
    "「ふん、そんなところまで熱くするなんて……っ。これは大スクープよ……って、言えるわけないでしょ……っ」":
        "「そんなにされたら……っ。ふん、あたしも、もう……っ」",
    "「ふん……っ、こんな姿を記事にされたら廃刊ものよ。……あんた、笑ったら承知しないからね」":
        "「ふん……っ。あんたの変態。……だ、誰にも言わないでよね……っ」",
    "「はぁ……っ、こんな記事にできない姿……。あんた、目を逸らさないでよね。……特別に見せてるんだから」":
        "「はぁ……っ、恥ずかしい……。でも、あんたが望むなら……ん、特別よ……っ」",
    "「ひぁっ……！　深く来るたび、頭が真っ白になる……っ。原稿も取材も、今だけは忘れさせてよ……あんたのせいなんだから♪」":
        "「ん、く、ぁっ……！　勝手に跳ねて、止まらない……っ。こんなあたしを一面に載せていいのは、あんただけよ♪」",
}


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    for current, original in REPLACEMENTS.items():
        if text.count(current) != 1:
            raise RuntimeError(f"expected one current line, got {text.count(current)}: {current!r}")
        text = text.replace(current, original, 1)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(text.encode("cp932"))
    print(f"wrote reconstructed pre-edit backup: {BACKUP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
