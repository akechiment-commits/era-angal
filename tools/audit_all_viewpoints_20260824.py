#!/usr/bin/env python3
"""全CHARの行為方向を本文候補まで横断抽出する視点監査。

機械的な語句一致は、PLAYERが「縛られる」正しい口上まで誤検出する。
このスクリプトは自動修正せず、COMF・手順書の方向表に反する可能性がある行だけを
行番号付きで出す。出力は必ず本文と注釈を目視してから修正する。
"""

from __future__ import annotations

import re
from pathlib import Path

from audit_koujo_integrity import char_files, extract_blocks, read_cp932


ACTOR_COMMANDS = {90, 130, 131, 132, 204, 316, 318}
RECEIVER_COMMANDS = {43, 44, 45, 110, 302, 303, 306, 307, 311, 312}

FIRST_PERSON = re.compile(r"(?:わたし|私|あたし|俺|ぼく|僕|うち|ウチ|あたい|おいら|ゆゆ|みけ|るり|うしお)")
PASSIVE = re.compile(r"(?:目隠しされ|目隠しをされ|縛られ|拘束され|口枷され|口枷をされ|口を塞がれ|愛撫され|撫でられ|撫でてもら|梳かされ|梳いてもら|梳かしてもら|入れられ)")
RECEIVER_ACTIVE = re.compile(r"(?:目隠しする|目を隠す|縛る|拘束する|口枷する|口を塞ぐ|撫でてあげる|撫でる|梳く|梳かしてあげる|梳かす)")
GIFT_ACTIVE = re.compile(r"(?:プレゼントする|贈る|渡す|あげる|用意する|作ってあげる)")
RECEIVING = re.compile(r"(?:ありがとう|ありがと|もら|受け取|くれた|贈り物|プレゼント)")
ACTOR_RECEIVE_FORMS = {
    316: re.compile(r"(?:梳かれる|梳かしてもら|梳いてもら|梳いてくれる)"),
    318: re.compile(r"(?:撫でられる|撫でてもら|撫でてくれる)"),
}
RECEIVER_HAIR_ACTIVE = re.compile(
    r"(?:わたし|私|あたし|俺|ぼく|僕|うち|ウチ|あたい|おいら)(?:が|は)[^。！？\n]{0,25}(?:髪|櫛)[^。！？\n]{0,12}梳(?:く|かす|いてあげ|かしてあげ)"
    r"|(?:あなた|きみ|君|おまえ|転校生くん|先輩|男の子|人)の髪[^。！？\n]{0,12}梳(?:く|かす|いてあげ|かしてあげ)"
)
RECEIVER_HEAD_ACTIVE = re.compile(
    r"(?:わたし|私|あたし|俺|ぼく|僕|うち|ウチ|あたい|おいら)(?:が|は)[^。！？\n]{0,20}撫で(?:る|てあげ)"
    r"|(?:あなた|きみ|君|おまえ|恋人)の頭[^。！？\n]{0,12}撫で(?:る|てあげ)"
)


def prints(block) -> list[tuple[int, str]]:
    return [
        (index + 1, line.strip())
        for index, line in enumerate(block.lines, block.start)
        if "PRINTFORM" in line and not line.lstrip().startswith(";")
    ]


def main() -> None:
    print("# 全CHAR視点候補監査 2026-08-24")
    for path in char_files():
        blocks = extract_blocks(read_cp932(path))
        for number in sorted(ACTOR_COMMANDS | RECEIVER_COMMANDS):
            block = blocks.get(number)
            if not block:
                continue
            for line_number, line in prints(block):
                if number in ACTOR_COMMANDS and FIRST_PERSON.search(line) and PASSIVE.search(line):
                    print(f"ACTOR_PASSIVE\t{path.name}\tCOM{number}\t{line_number}\t{line}")
                if number in ACTOR_RECEIVE_FORMS and ACTOR_RECEIVE_FORMS[number].search(line):
                    print(f"ACTOR_RECEIVE_FORM\t{path.name}\tCOM{number}\t{line_number}\t{line}")
                if number in {306, 307} and RECEIVER_HAIR_ACTIVE.search(line):
                    print(f"RECEIVER_HAIR_ACTIVE\t{path.name}\tCOM{number}\t{line_number}\t{line}")
                elif number == 312 and RECEIVER_HEAD_ACTIVE.search(line):
                    print(f"RECEIVER_HEAD_ACTIVE\t{path.name}\tCOM{number}\t{line_number}\t{line}")
                elif number in RECEIVER_COMMANDS and number not in {306, 307, 312} and RECEIVER_ACTIVE.search(line):
                    print(f"RECEIVER_ACTIVE\t{path.name}\tCOM{number}\t{line_number}\t{line}")
                if number == 302 and GIFT_ACTIVE.search(line) and not RECEIVING.search(line):
                    print(f"GIFT_ACTIVE\t{path.name}\tCOM302\t{line_number}\t{line}")


if __name__ == "__main__":
    main()
