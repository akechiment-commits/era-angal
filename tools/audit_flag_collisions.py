from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ERB = ROOT / "ERB"


@dataclass(frozen=True)
class Allocation:
    start: int
    end: int
    owner: str


ALLOCATIONS = [
    Allocation(31, 40, "録画データ（原作予約）"),
    Allocation(50, 56, "採取人数・クイズ記録（原作予約）"),
    Allocation(101, 199, "キャラ別KOJO_NEXT_PLAY存在判定（原作予約）"),
    Allocation(401, 499, "キャラ別尻子玉入手（原作予約）"),
    Allocation(601, 699, "キャラ別母乳本数（原作予約）"),
    Allocation(801, 899, "キャラ別黄金水本数（原作予約）"),
    Allocation(999, 1098, "キャラ選択可否（原作予約）"),
    Allocation(1101, 1199, "キャラ別離別回数（原作予約）"),
    Allocation(1201, 1299, "キャラ別卵所持数（原作予約）"),
    Allocation(1401, 1499, "キャラ別写真所持数（原作予約）"),
    Allocation(1601, 1699, "キャラ別愛液所持数（原作予約）"),
    Allocation(1801, 1899, "キャラ別下着所持数（原作予約）"),
    Allocation(2000, 2199, "調合レシピ記録"),
    Allocation(3001, 4884, "カード所持枚数"),
    Allocation(5000, 5015, "実績・イベント表示ビット"),
    Allocation(5020, 5021, "実績SP強化"),
    Allocation(5040, 5041, "射精統計・実績SP"),
    Allocation(5101, 5172, "カード実績一時集計A"),
    Allocation(5201, 5272, "カード実績一時集計B"),
    Allocation(5301, 5372, "カード実績一時集計C"),
    Allocation(5401, 5472, "カード実績一時集計D"),
    Allocation(5800, 5872, "キャラ別累計射精量"),
    Allocation(6000, 6099, "主人公アクセサリ"),
    Allocation(15000, 15004, "ガチャ通貨"),
    Allocation(15005, 15006, "学校行事"),
    Allocation(15007, 15007, "ログインボーナス"),
    Allocation(15010, 15015, "イベント別エリア"),
    Allocation(15020, 15025, "イベント別月内報酬受取数"),
    Allocation(15030, 15031, "子ども手当・子宝図鑑"),
    Allocation(15040, 15041, "学校行事一時TARGET"),
    Allocation(15050, 15055, "イベントボード共有進行状態"),
    Allocation(15060, 15065, "学校行事記録"),
    Allocation(15070, 15071, "イベントプレイヤーレベル・経験値"),
    Allocation(15099, 15099, "フラグ移行バージョン"),
    Allocation(15100, 15200, "調合素材発見状態"),
    Allocation(16000, 16002, "調教セッション集計"),
    Allocation(16010, 16509, "調教セッション使用コマンド"),
]


LEGACY_ALLOWED = Path("ERB/FLAG_MIGRATION_フラグ領域移行.ERB")
STATIC_FLAG = re.compile(r"(?<![A-Z])FLAG:(\d+)\b")


def read_erb(path: Path) -> str:
    raw = path.read_bytes()
    return raw.decode("cp932")


def check_allocations() -> list[str]:
    errors: list[str] = []
    ordered = sorted(ALLOCATIONS, key=lambda item: (item.start, item.end))
    for left, right in zip(ordered, ordered[1:]):
        if right.start <= left.end:
            errors.append(
                f"割当重複: {left.start}-{left.end} {left.owner} / "
                f"{right.start}-{right.end} {right.owner}"
            )
    return errors


def check_sources() -> list[str]:
    errors: list[str] = []
    forbidden_fragments = {
        "FLAG:(98 + COUNT)": "旧イベント別エリア領域",
        "FLAG:(104 + COUNT)": "廃止済みイベントマイルストーン領域",
        "FLAG:(120 + COUNT)": "旧イベント報酬領域",
        "FLAG:(127 + COUNT)": "廃止済みイベント累計PT領域",
        "FLAG:(500 + SELECTCOM)": "旧コマンド多様性領域",
        "FLAG:(500 + LOCAL:0)": "旧コマンド多様性領域",
        "FLAG:(3000+LOCAL)": "カードと重なる旧素材領域",
        "FLAG:(3000+(LOCAL:2))": "カードと重なる旧素材領域",
        "FLAG:(2100+A)": "カードと重なる旧素材領域",
    }
    for path in ERB.rglob("*.ERB"):
        rel = path.relative_to(ROOT)
        try:
            text = read_erb(path)
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: 文字コードエラー: {exc}")
            continue
        if rel == LEGACY_ALLOWED:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            code = line.split(";", 1)[0]
            for match in STATIC_FLAG.finditer(code):
                value = int(match.group(1))
                if 31 <= value <= 40:
                    errors.append(f"{rel}:{line_no}: 原作予約FLAG:{value}を直接使用")
                if 50 <= value <= 56:
                    errors.append(f"{rel}:{line_no}: 原作予約FLAG:{value}を直接使用")
                if 101 <= value <= 199:
                    errors.append(f"{rel}:{line_no}: 原作予約FLAG:{value}を直接使用")
                if 400 <= value <= 402:
                    errors.append(f"{rel}:{line_no}: 原作予約近傍の作業FLAG:{value}を使用")
            for fragment, label in forbidden_fragments.items():
                if fragment in code:
                    errors.append(f"{rel}:{line_no}: {label}: {fragment}")
    return errors


def main() -> int:
    errors = check_allocations() + check_sources()
    if errors:
        print("FLAG監査: NG")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"FLAG監査: OK（{len(ALLOCATIONS)}領域、ERB {len(list(ERB.rglob('*.ERB')))}ファイル）")
    print("- FLAG:101～199への追加システム書き込みなし")
    print("- カード所持3001～4884と素材発見フラグの重複なし")
    print("- 調教一時領域と永続カウンタ401～999の重複なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
