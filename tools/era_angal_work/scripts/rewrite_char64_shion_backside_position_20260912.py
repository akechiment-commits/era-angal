"""CHAR64しおんの後背方向説明を、反応中心へ限定的に調整する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_64_峰山しおん_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR64_before_backside_position_rewrite_20260912"
BACKUP = BACKUP_DIR / TARGET.name

REPLACEMENTS = {
    1199: (
        "「ん、ふぅ……後ろからだと、君の顔が見えないのが、すこし寂しいのだがね」",
        "「ん、ふぅ……君の顔が見えないのが、すこし寂しいのだがね」",
    ),
    1207: (
        "「ん、ふぅ……後ろからか、…まぁ、悪くない」",
        "「ん、ふぅ……見えないぶん、声だけが近くなるのだね。…まぁ、悪くない」",
    ),
    2240: (
        "「後ろから、…これでは私はただの被写体だね。ドガの踊り子の絵のように」",
        "「ん……これでは私はただの被写体だね。ドガの踊り子の絵のように、動けないまま見られている気分だ」",
    ),
    2244: (
        "「後ろからか、…悪くない選択だ。視線の暴力から逃れられる、ある意味では恵みだ」",
        "「ん、…視線の暴力から逃れられるのは、ある意味では恵みだね。声を抑えられるうちに、もう少し近くへ」",
    ),
    2248: (
        "「後ろからは、…私の表情が読まれない。能面のような匿名性が確保されるね」",
        "「ん……私の表情が読まれないのは助かるね。能面を被ったまま、こんな声まで隠せると思ったのだが」",
    ),
    3140: (
        "「後ろから、そちらに、というのは、…君の好みは把握しかねるね。グロテスクの図像学から拾ってきたかね」",
        "「その好みには驚いたよ。…君の探究心はグロテスクの図像学から拾ってきたのかね」",
    ),
    3142: (
        "「背中から来るとは、君も思い切ったね。見えないぶん、余計に敏感になるよ」",
        "「君も思い切ったね。見えないぶん、余計に敏感になるよ」",
    ),
    3150: (
        "「そこを、後ろから、…君の探究心には敬意を表そう。コロンブスもこうして新大陸を見つけたのだろう」",
        "「そこまで探究するとは、…君の好奇心には敬意を表そう。見えないぶん、想像まで膨らむね」",
    ),
    3152: (
        "「後ろからでは様子が見えないね。合図をしたら、すぐ止めたまえ」",
        "「様子が見えないね。合図をしたら、すぐ止めたまえ」",
    ),
    2828: (
        "「ふぅ、…後ろから%LOCALS%を貫くというのは、…私には支配者気分だね。古代ローマの将軍の凱旋気分というか」",
        "「ふぅ、…%LOCALS%の熱をここまで近くに感じるとは、…私には支配者気分だね。古代ローマの将軍の凱旋気分というか」",
    ),
    2832: (
        "「私が後ろから%LOCALS%に挿れるこの構図、…少年、しっかり堪能したまえ。歴史的逆転の場面だよ」",
        "「私が%LOCALS%の息を乱すこの感触、…少年、しっかり堪能したまえ。歴史的逆転の場面だよ」",
    ),
    2838: (
        "「%LOCALS%の背を眺めながら動くのは、…なかなかの観察席だ。ドガの後姿の踊り子を描く画家の視点さ」",
        "「%LOCALS%の息の乱れを感じながら動くのは、…なかなかの観察席だ。ドガの後姿の踊り子を描く画家の視点さ」",
    ),
    2840: (
        "「私から%LOCALS%を後ろから抱える構図は、…文学的に倒錯的だ。レオナルドの解剖図より珍しい構図だね」",
        "「私と%LOCALS%がこんなふうに重なるとは、…文学的に倒錯的だ。レオナルドの解剖図より珍しい光景だね」",
    ),
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    if BACKUP.exists():
        raise RuntimeError(f"backup already exists: {BACKUP}")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)

    for line_number, (old, new) in REPLACEMENTS.items():
        index = line_number - 1
        line = lines[index]
        if line.count(old) != 1:
            raise RuntimeError(f"line {line_number}: expected one old phrase, got {line.count(old)}")
        lines[index] = line.replace(old, new, 1)

    updated = "".join(lines)
    TARGET.write_bytes(updated.encode("cp932"))
    print(f"updated {TARGET}")
    print(f"backup {BACKUP}")
    print(f"changed_physical_lines {len(REPLACEMENTS)}")


if __name__ == "__main__":
    main()
