"""CHAR15 COM75を、やえが言葉責めを受ける側の反応へ統一する。"""

from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_15_長町やえ_COM.ERB"
SOURCE = ROOT / "tools/output/やえ.txt"
BACKUP = ROOT / "tools/backups/CHAR15_before_com75_recipient_rewrite_20260831/CHAR_15_長町やえ_COM.ERB"


REPLACEMENTS = {
    "「うぅ、そんな恥ずかしいこと言わせないでぇっ……。……あ、あたしのっ、ここがっ、濡れてっ、ますっ……いじわるっ♪」":
        "「うぅ……声が近いと、胸の奥まで熱くなるっ。そんなふうに言われたら、あたし、顔を上げられないよぉ……♪」",
    "「おに～さんの声、近いっ……。言い返したいのに、唇が笑ってるのばれちゃうよぉ♪」":
        "「言葉だけなのに、身体が先に反応してるっ……。おに～さん、顔を見ないで……でも、離れないでっ♪」",
    "「その一言、胸の奥まで入ってきたっ……。いつもの笑顔でごまかせないくらい、あたし、嬉しいよぉ♪」":
        "「その一言が残って、頭の中で何度も響くっ……。あたし、笑ってごまかせないくらい嬉しいよぉ♪」",
    "「やっ、言葉でいじめるのっ……？　うぅ、あたし、おに～さんのっ、えっちなお助けキャラっ、ですっ……恥ずかしいよぉっ！」":
        "「ひゃっ……そんなこと、耳元で言われたら返事できないよぉ……。顔が熱いっ……！」",
    "「耳元の言葉だけで足がすくむっ……。返事したらもっと恥ずかしくなりそうで、声が出せないよぉっ！」":
        "「声を聞くたび、胸がきゅってなるっ……。何もされてないのに、身体が言うこと聞かなくなっちゃうよぉ……！」",
    "「んっ、そんなふうに言われると身体まで熱いっ……。笑ってごまかすの、もう無理だよぉ……！」":
        "「もうやめてって思うのに、次の言葉を待ってる自分もいるっ……。あたし、どうしたらいいのぉ……！」",
}


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    if "# やえ（全1503件）" not in source:
        raise RuntimeError("指定されたやえ原作テキストの見出しを確認できません")

    text = TARGET.read_bytes().decode("cp932")
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET, BACKUP)

    applied = 0
    skipped = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count == 0:
            skipped += 1
            continue
        if count != 1:
            raise RuntimeError(f"COM75置換対象の出現数が不正です: {count}件")
        text = text.replace(old, new)
        applied += count

    TARGET.write_bytes(text.encode("cp932"))
    print(f"原作確認: {SOURCE}（見出し確認済み）")
    print(f"CHAR15 COM75を受け手側へ統一: {applied}件（既改稿・対象外{skipped}件）")


if __name__ == "__main__":
    main()
