# -*- coding: utf-8 -*-
"""
独自コマンド口上を効果タイプに合わせて並べ替える。

ウフフ COM280-284:
  280 バランス本番 / 281 快楽特化 / 282 背徳・露出 / 283 情愛本番 / 284 激しめ本番
純愛 COM410-414:
  410 甘々デート / 411 スキンシップ / 412 褒め・承認 / 413 癒し / 414 ディープキス

処理:
  1. CHAR_*_COM.ERB の IF SELECTCOM == NNN ... ELSEIF 連鎖をパース
  2. 場面ラベル＋本文からスコア付けし、各型に1場面を割り当て
  3. 口上ブロックを新順で書き戻し
  4. CSV の CSTR,80-89 も同じ順に並べ替え
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

UFUFU_TYPES = [
    (280, "バランス本番"),
    (281, "快楽特化"),
    (282, "背徳・露出"),
    (283, "情愛本番"),
    (284, "激しめ本番"),
]
PURE_TYPES = [
    (410, "甘々デート"),
    (411, "スキンシップ"),
    (412, "褒め・承認"),
    (413, "癒し"),
    (414, "ディープキス"),
]


def score_ufufu(scene: str, body: str) -> dict[int, float]:
    """Return scores for COM 280-284."""
    t = scene + "\n" + body
    s = {280: 0.0, 281: 0.0, 282: 0.0, 283: 0.0, 284: 0.0}

    # --- 282 背徳・露出 ---
    for kw, w in [
        ("最後列", 8), ("映画館", 6), ("誰か来", 5), ("見つか", 5), ("バレ", 5),
        ("声、我慢", 5), ("声を我慢", 5), ("屋上", 5), ("用具", 5), ("倉庫", 5),
        ("更衣室", 6), ("シャワー", 3), ("監視", 6), ("見回り", 5), ("サボ", 4),
        ("校舎裏", 5), ("旧校舎", 5), ("掃除用具", 5), ("飼育", 4), ("地下", 4),
        ("ステージ袖", 5), ("放送室", 5), ("機材", 4), ("準備室", 4), ("保健室", 4),
        ("カーテン", 3), ("部室", 2), ("誰もい", 2), ("鍵", 3), ("密会", 3),
        ("罰ゲーム", 2), ("授業中", 4), ("昼休み", 3), ("夜の", 2), ("人目", 4),
        ("はしたな", 3), ("いけない", 3), ("公共", 4), ("プール", 3), ("道場", 2),
        ("楽器庫", 4), ("楽屋", 4), ("衣装部屋", 3), ("本殿", 4), ("社務所", 3),
        ("筐体", 4), ("茂み", 4), ("畑", 2), ("温室", 2), ("防音", 2),
    ]:
        if kw in t:
            s[282] += w
    if "部屋" in scene and any(k in t for k in ("誰か", "バレ", "見つか", "妹が帰")):
        s[282] += 2

    # --- 281 快楽特化 ---
    for kw, w in [
        ("温泉", 8), ("湯上り", 8), ("火照", 7), ("汗", 6), ("汗だく", 8),
        ("シャワー", 7), ("ベッド", 5), ("ごろごろ", 5), ("メイド", 6),
        ("クリーム", 8), ("生クリーム", 8), ("衣装", 4), ("ユニ", 6), ("チア", 6),
        ("ロケ", 4), ("抱き枕", 6), ("夜更かし", 4), ("身体が熱", 6),
        ("感じて", 2), ("乱れる", 2), ("たっぷり", 2),
        ("ダイエット", 2), ("戯れ", 5), ("ゴスロリ", 4), ("猫耳", 5),
        ("ひみつ", 1), ("モニタ", 2),
    ]:
        if kw in t:
            s[281] += w

    # --- 283 情愛本番 ---
    for kw, w in [
        ("部屋", 5), ("実家", 5), ("旅館", 4), ("二人の部屋", 7), ("お部屋", 6),
        ("妹のいない", 6), ("ベッドで", 4), ("添い", 5), ("抱き合", 4),
        ("恋人", 2), ("特別", 2), ("愛して", 3), ("幸せ", 2), ("並んで", 2),
        ("ちゃんと", 1), ("二人きり", 2), ("おうち", 4), ("夜の忍び", 3),
        ("実家の部屋", 6), ("なつみの部屋", 5), ("しずくの部屋", 5),
        ("るかの部屋", 5), ("みさきの部屋", 5), ("ゆゆのお部屋", 5),
        ("つゆりの部屋", 5), ("アクセサリーの部屋", 3), ("鉱石の並ぶ部屋", 3),
    ]:
        if kw in t:
            s[283] += w
    # 部屋系は情愛寄りだが、明らかに露出・秘密基地なら減点
    if re.search(r"(屋上|倉庫|用具|保健室|準備室|放送|楽屋|ステージ)", scene):
        s[283] -= 3
    if "部屋" in scene and not re.search(r"(倉庫|準備|用具|放送|機材|衣装)", scene):
        s[283] += 3

    # --- 284 激しめ本番 ---
    for kw, w in [
        ("罰", 8), ("罠", 7), ("1on1", 7), ("道場", 6), ("柔道", 6),
        ("稽古", 5), ("力比べ", 6), ("激", 4), ("乱暴", 5), ("強引", 5),
        ("背後から", 6), ("押さえ", 5), ("組み伏せ", 6), ("指導中", 5),
        ("料理指導", 6), ("運動", 4), ("特訓", 4), ("格闘", 6),
        ("夜の忍び込み", 6), ("甘い罠", 5), ("ダイエット運動", 6),
        ("見回り", 2), ("サボり", 2),
    ]:
        if kw in t:
            s[284] += w
    if any(k in scene for k in ("体育館", "道場", "コート", "プール", "柔道", "罰")):
        s[284] += 3

    # --- 280 バランス（汎用二人きり・基準）---
    for kw, w in [
        ("部室", 3), ("音楽室", 3), ("美術室", 3), ("家庭科", 3), ("秘密", 2),
        ("二人", 1), ("放課後", 2), ("空き教室", 3), ("部の", 2),
        ("プレハブ", 2), ("アトリエ", 2), ("スタジオ", 2), ("防音", 2),
    ]:
        if kw in t:
            s[280] += w
    # どれにも寄らない場面の受け皿
    s[280] += 1.5

    return s


def score_pure(scene: str, body: str) -> dict[int, float]:
    """Return scores for COM 410-414."""
    t = scene + "\n" + body
    s = {410: 0.0, 411: 0.0, 412: 0.0, 413: 0.0, 414: 0.0}

    # --- 410 甘々デート ---
    for kw, w in [
        ("デート", 8), ("遊園地", 9), ("祭り", 7), ("縁日", 7), ("屋台", 5),
        ("花見", 6), ("夜桜", 5), ("旅行", 6), ("小旅行", 6), ("初デート", 9),
        ("映画", 5), ("水族館", 6), ("動物園", 6), ("公園", 3), ("ピクニック", 6),
        ("ライブ", 2), ("花火", 5), ("クリスマス", 4), ("初詣", 6), ("七夕", 4),
        ("モール", 5), ("ショッピング", 5), ("めぐり", 4), ("巡", 2),
        ("お出かけ", 5), ("貸切", 3), ("テーマパーク", 6), ("クレープ", 5),
        ("食べ歩き", 5), ("屋さん", 3), ("ゲームセンター", 4),
    ]:
        if kw in t:
            s[410] += w

    # --- 411 スキンシップ ---
    for kw, w in [
        ("手つなぎ", 7), ("手を繋", 7), ("あーん", 7), ("散歩", 5), ("日向", 5),
        ("ひなた", 5), ("こたつ", 6), ("ぬくぬく", 6), ("水やり", 5), ("ふれあい", 6),
        ("添い寝", 5), ("膝", 3), ("だっこ", 4), ("肩", 2), ("マッサージ", 4),
        ("頭を撫", 4), ("寄り添", 4), ("並んで歩", 4), ("キャッチボール", 3),
        ("犬の散歩", 5), ("猫", 3), ("小動物", 4), ("芋掘り", 3), ("世話", 3),
        ("手合わせ", 2), ("一緒に", 1),
    ]:
        if kw in t:
            s[411] += w

    # --- 412 褒め・承認 ---
    for kw, w in [
        ("応援", 8), ("ライブ", 5), ("演奏", 6), ("特訓", 7), ("試合", 7),
        ("手合わせ", 6), ("レッスン", 6), ("ステージ", 6), ("ファン", 7),
        ("生徒会長", 6), ("合奏", 8), ("歌", 3), ("練習", 4), ("披露", 5),
        ("感想", 5), ("褒めて", 6), ("上手", 3), ("実力", 3), ("勝ち", 3),
        ("大会", 6), ("力比べ", 5), ("実況", 5), ("プレゼン", 5),
        ("一日生徒会長", 7), ("専属", 5), ("主演", 5), ("プログラム", 4),
        ("協力プレイ", 3), ("ファッションショー", 4),
    ]:
        if kw in t:
            s[412] += w
    # 手料理・チョコ・弁当は「感想を聞かせて／腕により」＝承認寄り
    if any(k in scene for k in ("手料理", "手作りチョコ", "チョコ", "弁当", "カレー", "お菓子作り")):
        s[412] += 5
        s[413] += 2
        s[414] += 1

    # --- 413 癒し ---
    for kw, w in [
        ("帰り道", 6), ("カフェ", 5), ("甘え", 6), ("のんびり", 6), ("日向ぼっこ", 6),
        ("ひなたぼっこ", 6), ("こたつ", 4), ("お昼寝", 5), ("ぼーっ", 4),
        ("落ち着く", 4), ("満たさ", 3), ("しあわせ", 3), ("夕暮れ", 3),
        ("夕焼け", 3), ("お墓", 4), ("星空", 3), ("天体", 3), ("プラネタリウム", 3),
        ("ラーメン", 2), ("食べ放題", 2), ("ファミレス", 3), ("パーラー", 3),
        ("ぬいぐるみ", 3), ("おとぎ話", 3), ("語らい", 4), ("窓越し", 3),
        ("休日", 3), ("だらだら", 5), ("グッズ", 2),
    ]:
        if kw in t:
            s[413] += w

    # --- 414 ディープキス（親密・ロマンチック近接）---
    for kw, w in [
        ("キス", 10), ("唇", 6), ("口づけ", 8), ("夜桜", 5), ("夜の", 3),
        ("特別な", 3), ("二人きり", 2), ("密着", 4), ("抱き", 3),
        ("告白", 5), ("愛して", 5), ("隣にいて", 5),
        ("クリスマス", 4), ("花火の帰り", 4), ("夕暮れの帰り道", 4),
        ("秘密のポエム", 6), ("きみへの", 5), ("きみの物語", 5),
        ("歌詞を聴かせ", 5), ("短冊", 3), ("ミサンガ", 4), ("ポエム", 5),
        ("詩集", 4), ("夜風", 3),
    ]:
        if kw in t:
            s[414] += w
    # ロマンチック夜・贈り物
    if any(k in scene for k in ("夜桜", "ポエム", "詩", "短冊", "ミサンガ", "プログラム")):
        s[414] += 4
    if any(k in scene for k in ("夜", "夕", "星", "花火", "クリスマス")):
        s[414] += 2

    s[410] += 0.5  # わずかな受け皿（甘々に寄せすぎない）
    return s


def assign_best(items: list[dict], score_fn, type_ids: list[int]) -> list[int]:
    """
    items: [{scene, body, old_com, content}, ...]
    総スコア最大の割当（5! = 120 を全探索）で type_ids 順の item index を返す。
    """
    n = len(items)
    assert n == len(type_ids)
    scores = [score_fn(it["scene"], it["body"]) for it in items]
    # matrix[item][type_pos]
    mat = [[scores[i].get(type_ids[j], 0.0) for j in range(n)] for i in range(n)]

    best_perm = list(range(n))  # type_pos -> item_index via inverse...
    best_score = -1e18

    # perm: type_pos -> item_index
    def rec(type_pos: int, used: set[int], acc: float, cur: list[int]):
        nonlocal best_perm, best_score
        if type_pos == n:
            if acc > best_score:
                best_score = acc
                best_perm = cur[:]
            return
        for i in range(n):
            if i in used:
                continue
            used.add(i)
            cur.append(i)
            rec(type_pos + 1, used, acc + mat[i][type_pos], cur)
            cur.pop()
            used.remove(i)

    rec(0, set(), 0.0, [])
    return best_perm


def extract_scene(content: str) -> str:
    m = re.search(r"場面[:：]\s*([^\n）\)]+)", content)
    if m:
        return m.group(1).strip()
    return ""


def parse_elseif_chain(block: str, coms: list[int]) -> list[dict] | None:
    """
    Parse:
      IF SELECTCOM == 280
      ...
      ELSEIF SELECTCOM == 281
      ...
      ELSEIF SELECTCOM == 284
      ...
      ENDIF
    Returns list of dicts with content (inner, without IF/ELSEIF/ENDIF lines).
    """
    # Normalize newlines
    block = block.replace("\r\n", "\n").replace("\r", "\n")
    # Must start with IF SELECTCOM == first
    first = coms[0]
    if not re.match(rf"IF SELECTCOM == {first}\b", block):
        # try flexible whitespace
        if not re.search(rf"^IF SELECTCOM == {first}\b", block, re.M):
            return None

    parts = []
    # Split by IF/ELSEIF SELECTCOM == N
    pattern = r"(?:^|\n)((?:ELSE)?IF) SELECTCOM == (\d+)\n"
    matches = list(re.finditer(pattern, block))
    if len(matches) != len(coms):
        return None

    found_coms = [int(m.group(2)) for m in matches]
    if found_coms != coms:
        return None

    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        chunk = block[start:end]
        # 先頭改行を落とす
        if chunk.startswith("\n"):
            chunk = chunk[1:]
        chunk = chunk.rstrip("\n")
        # 最終分岐のみ、チェイン閉じの ENDIF（通常インデント無し）を1つ外す
        # 分岐内の \tENDIF（TALENT 等）は絶対に消さない
        if i == len(matches) - 1:
            lines = chunk.split("\n")
            while lines and lines[-1].strip() == "":
                lines.pop()
            if lines and lines[-1].strip() == "ENDIF":
                # チェイン閉じは無インデント、内側はタブ付き、の想定
                # どちらでも「最後の ENDIF 1つ」がチェイン閉じ
                lines.pop()
            chunk = "\n".join(lines)
        parts.append(
            {
                "old_com": found_coms[i],
                "content": chunk,
                "scene": extract_scene(chunk),
                "body": chunk,
            }
        )
    return parts


def build_elseif_chain(coms: list[int], contents: list[str]) -> str:
    lines = []
    for i, (com, content) in enumerate(zip(coms, contents)):
        if i == 0:
            lines.append(f"IF SELECTCOM == {com}")
        else:
            lines.append(f"ELSEIF SELECTCOM == {com}")
        # content should not have leading IF
        c = content
        if c and not c.endswith("\n"):
            lines.append(c)
        else:
            lines.append(c.rstrip("\n"))
    lines.append("ENDIF")
    return "\n".join(lines)


def find_chain_span(text: str, coms: list[int]) -> tuple[int, int] | None:
    """Find start of IF SELECTCOM == first through matching final ENDIF of chain."""
    first = coms[0]
    m = re.search(rf"^IF SELECTCOM == {first}\b", text, re.M)
    if not m:
        return None
    start = m.start()
    # From start, find the chain's closing ENDIF: after last ELSEIF SELECTCOM == last
    last = coms[-1]
    m_last = re.search(rf"^ELSEIF SELECTCOM == {last}\b", text[start:], re.M)
    if not m_last:
        return None
    pos = start + m_last.end()
    # Find ENDIF that closes the chain - scan with depth for IF/ENDIF
    # Simpler: from after last branch header, find first ENDIF that is at the chain level.
    # Nested IF TALENT etc. exist inside branches - need depth counting from chain start.
    depth = 0
    lines = text[start:].split("\n")
    offset = start
    end_offset = None
    for line in lines:
        # ERB: IF で+1、ENDIF で-1。ELSEIF/ELSE は同一深度（ネストしない）
        stripped = line.strip()
        if stripped.startswith("ELSEIF") or stripped == "ELSE" or stripped.startswith("ELSE "):
            pass
        elif re.match(r"^IF\b", stripped):
            depth += 1
        elif stripped == "ENDIF":
            depth -= 1
            if depth == 0:
                end_offset = offset + len(line)
                break
        offset += len(line) + 1  # + newline
    if end_offset is None:
        return None
    return start, end_offset


def reorder_file_text(text: str) -> tuple[str, list[str]]:
    """Returns (new_text, log_lines)."""
    logs = []
    original = text
    text_n = text.replace("\r\n", "\n").replace("\r", "\n")

    for label, coms, score_fn in [
        ("ウフフ", [280, 281, 282, 283, 284], score_ufufu),
        ("純愛", [410, 411, 412, 413, 414], score_pure),
    ]:
        span = find_chain_span(text_n, coms)
        if not span:
            logs.append(f"  [{label}] chain not found")
            continue
        start, end = span
        block = text_n[start:end]
        # strip trailing newline from block for parse; keep ENDIF in block
        parts = parse_elseif_chain(block, coms)
        if not parts:
            logs.append(f"  [{label}] parse failed")
            continue

        order_idx = assign_best(parts, score_fn, coms)
        new_contents = [parts[i]["content"] for i in order_idx]
        old_scenes = [parts[i]["scene"] for i in range(5)]
        new_scenes = [parts[i]["scene"] for i in order_idx]

        if order_idx == list(range(5)):
            logs.append(f"  [{label}] no change: {old_scenes}")
        else:
            logs.append(f"  [{label}] {old_scenes}")
            logs.append(f"       -> {new_scenes}")
            for tid, i in zip(coms, order_idx):
                logs.append(f"       COM{tid} <= was COM{parts[i]['old_com']}: {parts[i]['scene']}")

        new_block = build_elseif_chain(coms, new_contents)
        text_n = text_n[:start] + new_block + text_n[end:]

    return text_n, logs


def load_csv_cstr(path: Path) -> dict[int, str]:
    t = path.read_bytes().decode("cp932")
    out = {}
    for line in t.splitlines():
        m = re.match(r"CSTR,(8[0-9]),(.*)$", line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def write_csv_cstr(path: Path, cstr_map: dict[int, str]) -> None:
    raw = path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    lines = raw.split("\n")
    new_lines = []
    for line in lines:
        m = re.match(r"CSTR,(8[0-9]),(.*)$", line)
        if m:
            k = int(m.group(1))
            if k in cstr_map:
                new_lines.append(f"CSTR,{k},{cstr_map[k]}")
                continue
        new_lines.append(line)
    text = "\n".join(new_lines)
    if not text.endswith("\n"):
        text += "\n"
    path.write_bytes(text.replace("\n", "\r\n").encode("cp932"))


def char_no_from_com_path(p: Path) -> int | None:
    m = re.match(r"CHAR_(\d+)_", p.name)
    return int(m.group(1)) if m else None


def find_csv_for_no(no: int) -> Path | None:
    # Chara1_... or Chara01 not used; pattern Chara{n}_ or Chara{n}.
    candidates = list(Path("CSV").glob(f"Chara{no}_*.csv"))
    if not candidates:
        candidates = list(Path("CSV").glob(f"Chara{no}.csv"))
    return candidates[0] if candidates else None


def extract_scenes_from_text(text: str, coms: list[int]) -> list[str]:
    text_n = text.replace("\r\n", "\n")
    span = find_chain_span(text_n, coms)
    if not span:
        return []
    parts = parse_elseif_chain(text_n[span[0]:span[1]], coms)
    if not parts:
        return []
    return [p["scene"] for p in parts]


def main():
    dry = "--dry-run" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = [int(x) for x in a.split("=", 1)[1].split(",")]

    com_files = sorted(Path("ERB/CHAR").glob("CHAR_*_COM.ERB"))
    report = []
    changed = 0

    for p in com_files:
        no = char_no_from_com_path(p)
        if no is None:
            continue
        if only and no not in only:
            continue
        if no == 0:
            continue

        raw = p.read_bytes().decode("cp932")
        new_text, logs = reorder_file_text(raw)
        report.append(f"=== CHAR_{no:02d} {p.name} ===")
        report.extend(logs)

        # Derive new CSTR order from new scenes
        ufufu_scenes = extract_scenes_from_text(new_text, [280, 281, 282, 283, 284])
        pure_scenes = extract_scenes_from_text(new_text, [410, 411, 412, 413, 414])

        csv_path = find_csv_for_no(no)
        if csv_path and len(ufufu_scenes) == 5 and len(pure_scenes) == 5:
            old_cstr = load_csv_cstr(csv_path)
            # Map old CSTR values by scene name matching when possible
            # Prefer using scene labels from ERB as new CSTR text (already the display names)
            # But CSV may have slightly different wording - match by reordering existing CSTR values
            old_u = [old_cstr.get(80 + i, "") for i in range(5)]
            old_p = [old_cstr.get(85 + i, "") for i in range(5)]

            # From original file, get old scene order and compute permutation
            old_ufufu = extract_scenes_from_text(raw, [280, 281, 282, 283, 284])
            old_pure = extract_scenes_from_text(raw, [410, 411, 412, 413, 414])

            def permute_cstr(old_names, old_scenes, new_scenes):
                """Reorder old_names (CSV) following scene reorder old_scenes->new_scenes."""
                if len(old_names) != 5 or len(old_scenes) != 5:
                    return old_names
                # index of each new scene in old_scenes
                result = []
                used = set()
                for ns in new_scenes:
                    found = None
                    for i, os_ in enumerate(old_scenes):
                        if i in used:
                            continue
                        if os_ == ns or (os_ and ns and (os_ in ns or ns in os_)):
                            found = i
                            break
                    if found is None:
                        # fallback: try match CSV name to scene
                        for i, on in enumerate(old_names):
                            if i in used:
                                continue
                            if on and ns and (on in ns or ns in on or on == ns):
                                found = i
                                break
                    if found is None:
                        for i in range(5):
                            if i not in used:
                                found = i
                                break
                    used.add(found)
                    result.append(old_names[found])
                return result

            new_u = permute_cstr(old_u, old_ufufu, ufufu_scenes)
            new_p = permute_cstr(old_p, old_pure, pure_scenes)
            # If CSV names are empty, use scene labels
            new_u = [n if n else s for n, s in zip(new_u, ufufu_scenes)]
            new_p = [n if n else s for n, s in zip(new_p, pure_scenes)]

            new_cstr = dict(old_cstr)
            for i, name in enumerate(new_u):
                new_cstr[80 + i] = name
            for i, name in enumerate(new_p):
                new_cstr[85 + i] = name

            if not dry:
                if new_text != raw.replace("\r\n", "\n").replace("\r", "\n"):
                    p.write_bytes(new_text.replace("\n", "\r\n").encode("cp932"))
                    changed += 1
                if new_u != old_u or new_p != old_p:
                    write_csv_cstr(csv_path, new_cstr)
                    report.append(f"  [CSV] {csv_path.name}")
                    report.append(f"       U: {old_u} -> {new_u}")
                    report.append(f"       P: {old_p} -> {new_p}")
            else:
                report.append(f"  [CSV dry] U: {old_u} -> {new_u}")
                report.append(f"       P: {old_p} -> {new_p}")
        else:
            if not dry and new_text != raw.replace("\r\n", "\n").replace("\r", "\n"):
                p.write_bytes(new_text.replace("\n", "\r\n").encode("cp932"))
                changed += 1
            report.append(f"  [CSV] skip (path={csv_path}, scenes u={ufufu_scenes} p={pure_scenes})")

    out = Path("tools/_reorder_unique_com_report.txt")
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"done dry={dry} changed_erb={changed}")
    print(f"report: {out}")
    # print summary count
    no_change = sum(1 for line in report if "no change" in line)
    print(f"no-change blocks: {no_change}")


if __name__ == "__main__":
    main()
