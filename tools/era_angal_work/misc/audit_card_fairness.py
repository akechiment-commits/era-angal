"""Compare character card growth using current ERB data and normal gacha odds.

No save data or game code is modified. Results are exact marginal binomial
expectations (summed per card), not a particular random playthrough.
"""
from collections import Counter, defaultdict
from functools import lru_cache
import json
import math
import random
import statistics
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]


def read(name):
    return (ROOT / 'ERB' / name).read_bytes().decode('cp932').replace('\r', '')


def function(text, name):
    return re.search(r'^@' + name + r'\b.*?\n(.*?)(?=^@|\Z)', text, re.M | re.S)[1]


def cases(text):
    return {int(m[1]): m[2] for m in re.finditer(r'^CASE (\d+)\b[^\n]*\n(.*?)(?=^CASE|^ENDSELECT|\Z)', text, re.M | re.S)}


def globals_in(text):
    return {int(k): int(v) for k, v in re.findall(r'GLOBAL:(\d+) = (\d+)', text)}


card_source = read('CARD_DATA_カードデータ定義.ERB')
event_source = read('EVENT_BOARD_DATA_イベントデータ.ERB')
cards = {}
for cid, block in cases(function(card_source, 'CARD_GET_DATA')).items():
    values = {int(k): int(v) for k, v in re.findall(r'RESULT:(\d+) = (\d+)', block)}
    cards[cid] = dict(id=cid, char=values[1], rarity=values[2], kind=values[3], base=values[4], name=re.search(r'STR:0 = (.*)', block)[1])
assert len(cards) == 1884

names = {}
for path in (ROOT / 'CSV').glob('Chara*.csv'):
    text = path.read_bytes().decode('cp932').replace('\r', '')
    num = re.search(r'^番号,(\d+)', text, re.M)
    name = re.search(r'^名前,([^\n]+)', text, re.M)
    if num and name:
        names[int(num[1])] = name[1]

event_ids = set()
for values in re.findall(r'^CASE ([\d, ]+)', function(event_source, 'EVENT_BOARD_IS_EVENT_CARD'), re.M):
    event_ids.update(int(x) for x in values.split(','))
assert event_ids <= cards.keys()

# Verify the generated pools actually expose the same cards and characters.
pools = defaultdict(list)
for c in cards.values():
    if c['char'] > 0:
        pools[c['char'], c['rarity']].append(c['id'])
for rarity, block in cases(function(card_source, 'CARD_GET_CHARS_FOR_RARITY')).items():
    values = globals_in(block)
    assert values[2000] == 71
    assert {values[2001 + i] for i in range(71)} == set(range(1, 72))
for char, block in cases(function(card_source, 'CARD_GET_CHARPOOL')).items():
    for rarity, inner in cases('\n'.join(line[1:] if line.startswith('\t') else line for line in block.splitlines())).items():
        values = globals_in(inner)
        assert {values[2101 + i] for i in range(values[2100])} == set(pools[char, rarity])
assert len(pools) == 426

RATES = {1: 20, 2: 10, 3: 10, 4: 5, 5: 4, 6: 2}
SPLITS = {1: (0, 0, 0), 2: (10, 10, 10), 3: (20, 10, 10), 4: (20, 20, 10), 5: (25, 20, 15), 6: (25, 20, 20)}
ODDS = {
    'bronze': (0.85, 0.10, 0.0389, 0.01, 0.001, 0.0001),
    'silver': (0.30, 0.4145, 0.22, 0.06, 0.005, 0.0005),
    'gold': (0, 0.50, 0.275, 0.20, 0.02, 0.005),
    'platinum': (0, 0, 0, 0.87, 0.10, 0.03),
    'diamond': (0, 0.11, 0.28, 0.40, 0.15, 0.06),
}


@lru_cache(None)
def score(rarity, kind, base, copies):
    if not copies:
        return (0, 0)
    total = base + (copies - 1) * base // RATES[rarity] + (3 * base if copies >= 12 else 0)
    secondaries = [total * percent // 100 for percent in SPLITS[rarity]]
    amounts = [total - sum(secondaries)] + secondaries
    deck_part = amounts[(3 - kind) % 4]
    return (5 * (total + deck_part), 5 * total)


@lru_cache(None)
def expected_score(rarity, kind, base, draws, probability):
    if probability == 0:
        return (0.0, 0.0)
    # These scenarios have low per-card probabilities; recurrence is stable.
    mass = math.exp(draws * math.log1p(-probability))
    current = neutral = 0.0
    mean = draws * probability
    limit = min(draws, math.ceil(mean + 16 * math.sqrt(mean + 1) + 50))
    probability_sum = 0.0
    for k in range(limit + 1):
        a, b = score(rarity, kind, base, k)
        current += mass * a
        neutral += mass * b
        probability_sum += mass
        if k < draws:
            mass *= (draws - k) / (k + 1) * probability / (1 - probability)
    assert abs(probability_sum - 1) < 1e-9, probability_sum
    return current, neutral


def normal_probabilities(tier):
    result = {}
    for (char, rarity), ids in pools.items():
        weights = {cid: 1 if cid in event_ids else 10 for cid in ids}
        total = sum(weights.values())
        for cid in ids:
            result[cid] = ODDS[tier][rarity - 1] / 71 * weights[cid] / total
    assert abs(sum(result.values()) - 1) < 1e-12
    return result


def expectation(draws, probabilities):
    results = {char: dict(name=names[char], current=0.0, neutral=0.0) for char in range(1, 72)}
    for cid, probability in probabilities.items():
        c = cards[cid]
        if c['char'] == 0:
            continue
        current, neutral = expected_score(c['rarity'], c['kind'], c['base'], draws, probability)
        results[c['char']]['current'] += current
        results[c['char']]['neutral'] += neutral
    return results


def summary(rows):
    result = {}
    for key in ('current', 'neutral'):
        ordered = sorted(rows.items(), key=lambda row: row[1][key], reverse=True)
        result[key] = dict(ratio=ordered[0][1][key] / ordered[-1][1][key], top=ordered[:5], bottom=ordered[-5:])
    return result


def validate_model():
    # Check probabilities against the executable thresholds, not their comments.
    source = function(read('GACHA_ガチャシステム.ERB'), 'GACHA_PULL').split(';そのレア度を持つキャラ一覧')[0]
    branches = re.split(r'^CASE(?: ([1-4])|ELSE)\s*\n', source, flags=re.M)
    for i, tier in enumerate(ODDS):
        block = branches[2 * i + 2]
        thresholds = list(map(int, re.findall(r'LOCAL:9 < (\d+)', block))) + [10000]
        rarities = list(map(int, re.findall(r'LOCAL:8 = (\d+)', block)))
        actual = [0.0] * 6
        last = 0
        for threshold, rarity in zip(thresholds, rarities):
            actual[rarity - 1] = (threshold - last) / 10000
            last = threshold
        assert tuple(actual) == ODDS[tier], (tier, actual)
    assert score(1, 0, 8, 1) == (40, 40)
    assert score(1, 3, 8, 1) == (80, 40)
    assert score(4, 0, 60, 1) == (330, 300)
    assert score(4, 3, 60, 1) == (450, 300)
    assert score(4, 0, 60, 12) == (2045, 1860)
    # Independent hierarchical sampling: rarity -> uniform character -> card.
    rng = random.Random(20260914)
    grouped = {kind: [char for char in range(1, 72) if cards[pools[char, 1][0]]['kind'] == kind] for kind in range(4)}
    samples = {kind: [] for kind in range(4)}
    weighted_pools = {key: [cid for cid in ids for _ in range(1 if cid in event_ids else 10)] for key, ids in pools.items()}
    for _ in range(1000):
        copies = Counter()
        for rarity in rng.choices(range(1, 7), weights=ODDS['gold'], k=710):
            char = rng.randrange(1, 72)
            copies[rng.choice(weighted_pools[char, rarity])] += 1
        totals = defaultdict(int)
        for cid, n in copies.items():
            c = cards[cid]
            totals[c['char']] += score(c['rarity'], c['kind'], c['base'], n)[0]
        for kind, chars in grouped.items():
            samples[kind].append(sum(totals[c] for c in chars) / len(chars))
    expected = expectation(710, normal_probabilities('gold'))
    checked = {}
    for kind, chars in grouped.items():
        target = sum(expected[c]['current'] for c in chars) / len(chars)
        mean = statistics.mean(samples[kind])
        se = statistics.stdev(samples[kind]) / math.sqrt(len(samples[kind]))
        assert abs(mean - target) < 6 * se
        checked[kind] = dict(exact=target, simulation_mean=mean, standard_error=se)
    return checked


def main():
    output = dict(card_count=len(cards), event_card_count=len(event_ids), card_characters=71, excluded_no_cards=[names[c] for c in names if c > 0 and c not in {x['char'] for x in cards.values()}])
    inventory = {}
    for char in range(1, 72):
        cs = [c for c in cards.values() if c['char'] == char]
        inventory[char] = dict(name=names[char], count=len(cs), kinds=dict(Counter(c['kind'] for c in cs)), rarities=dict(Counter(c['rarity'] for c in cs)), all_once=sum(score(c['rarity'], c['kind'], c['base'], 1)[0] for c in cs))
    output['inventory'] = inventory
    assert all(len(row['kinds']) == 1 for row in inventory.values())
    output['validation'] = validate_model()
    output['normal'] = {}
    for tier in ODDS:
        for draws in (710, 3550, 7100):
            rows = expectation(draws, normal_probabilities(tier))
            output['normal'][f'{tier}_{draws}'] = dict(rows=rows, summary=summary(rows))

    # Supplementary scenario: each draw chooses an event uniformly at random.
    # Each draw attempts pickup with 25%; absent same-rarity cards fall back.
    pickup_pools = {key: [value for pos, value in globals_in(block).items() if 2200 <= pos < 2300] for key, block in cases(function(event_source, 'LOAD_EVENT_PICKUP_CARDS')).items()}
    output['pickup_equal_event'] = {}
    for tier in ('gold', 'diamond'):
        normal = normal_probabilities(tier)
        average = defaultdict(float)
        for ids in pickup_pools.values():
            by_rarity = {r: [cid for cid in ids if cards[cid]['rarity'] == r] for r in range(1, 7)}
            for cid, p in normal.items():
                r = cards[cid]['rarity']
                average[cid] += p * (0.75 if by_rarity[r] else 1) / len(pickup_pools)
            for r, matching in by_rarity.items():
                for cid in matching:
                    average[cid] += ODDS[tier][r-1] * 0.25 / len(matching) / len(pickup_pools)
        assert abs(sum(average.values()) - 1) < 1e-10
        rows = expectation(7100, average)
        output['pickup_equal_event'][tier] = dict(rows=rows, summary=summary(rows), events=len(pickup_pools))

    rewards = Counter()
    for block in cases(function(event_source, 'LOAD_EVENT_REWARDS')).values():
        values = globals_in(block)
        for i in range(values[2999]):
            if values[3100 + i] == 9:
                rewards[values[3200 + i]] += 1
    direct = {char: dict(name=names[char], current=0, neutral=0, copies=0) for char in range(1, 72)}
    for cid, copies in rewards.items():
        c = cards[cid]
        if c['char'] == 0:
            continue
        a, b = score(c['rarity'], c['kind'], c['base'], copies)
        direct[c['char']]['current'] += a
        direct[c['char']]['neutral'] += b
        direct[c['char']]['copies'] += copies
    output['fixed_rewards_one_loop_each'] = direct
    (ROOT / 'CARD_FAIRNESS_RESULTS_2026-09-14.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    labels = ['表現', '運動', '学力', 'デッキ戦力']
    groups = {k: [c for c in inventory if k in inventory[c]['kinds']] for k in range(4)}
    lines = ['# カード成長のキャラ別公平性調査（2026-09-14）', '',
        '## 結論', '',
        '同じ入手機会に対するカード成長という意味では、デッキ戦力型16人への継続的な優遇がある。カードごとの偶然の差ではなく、71人すべてで全カードの主補正タイプがキャラ単位で固定されていた。キャラ本人の能力・親密度・イベント選択まで含む総合的な攻略難度を測定したものではない。', '',
        '## 調査対象・計算条件', '',
        '- 全1884カードを解析。うちキャラ番号1～71に属する1842枚が個人の能力に加算される。キャラ番号0の42枚は通常ガチャの個人プールに入らず、個人補正再計算でも対象外。',
        '- 71人×6レア度の426プールを、カード定義と照合。各レア度で全71人が等確率に選ばれることを確認。追加キャラ「あんず」はカード定義なしで、この比較の対象外。',
        '- 通常ガチャのイベントカード重み1／その他10、レア度別重複減衰、12枚以上の加算、整数切捨てを反映。各カード枚数の二項分布から期待値を計算。運の良い一回の結果ではない。',
        '- 初期カードなし、カード由来のイベント発揮値のみを比較。キャラ能力・親密度とパーティ全体の倍率は含めない。710回は各キャラ平均10枚、3550回は50枚、7100回は100枚に相当する比較用の投入量であり、何日目で到達するという推定ではない。',
        '- 「2倍なし」は、他の抽選・重複条件を一切変えず、イベント計算からデッキ戦力の倍化だけを除いた仮想比較。ゲームへの変更はしていない。', '',
        '## 同じレア度の新品カード1枚の寄与', '',
        '| レア度 | 基本値 | 表現型 | 運動型 | 学力型 | デッキ戦力型 |',
        '|---|---:|---:|---:|---:|---:|']
    for r, label in enumerate(['N','R','HR','SR','UR','MR'], 1):
        base = next(c['base'] for c in cards.values() if c['rarity'] == r)
        lines.append('| ' + ' | '.join(map(str, [label, base] + [score(r, k, base, 1)[0] for k in range(4)])) + ' |')
    lines += ['', '## 通常ガチャを同じ回数引いたときのタイプ別平均', '',
        '| 条件 | 表現型20人 | 運動型26人 | 学力型9人 | デッキ戦力型16人 |', '|---|---:|---:|---:|---:|']
    for tier, draws in [('bronze',710),('gold',710),('gold',3550),('gold',7100),('diamond',7100)]:
        rows = output['normal'][f'{tier}_{draws}']['rows']
        for field, suffix in [('current','現行'),('neutral','2倍なし')]:
            values = [sum(rows[c][field] for c in groups[k]) / len(groups[k]) for k in range(4)]
            lines.append(f'| {tier} {draws}回・{suffix} | ' + ' | '.join(f'{v:,.0f}' for v in values) + ' |')
    lines += ['', 'ゴールド710回では、デッキ戦力型の平均約2140に対し他タイプは約1488～1528。倍化だけを除くと約1353対1290～1352となり、タイプ間の差の主因が倍化であることを確認できる。', '',
        '## ゴールド710回でカード成長の期待値が高い5人', '', '| キャラ | 現行 | 2倍なし |', '|---|---:|---:|']
    for _, row in output['normal']['gold_710']['summary']['current']['top']:
        lines.append(f"| {row['name']} | {row['current']:,.0f} | {row['neutral']:,.0f} |")
    lines += ['', 'ゴールド3550回・7100回でも上位5人はデッキ戦力型。集める量によって個人順位は変わるが、タイプの優遇は残る。', '',
        '## デッキ戦力型の16人', '', '、'.join(names[c] for c in groups[3]) + '。', '',
        '## 入手経路による違い・残る差', '',
        '- 全カードの種類数はキャラごとに異なる。通常ガチャのキャラ当選率は均等だが、種類が少ないと重複しやすく、種類が多いと新品を引きやすい。12枚ボーナスもあるため「種類が多いほど常に得」とは限らない。',
        '- 56イベントを毎回等確率で選ぶ仮想ピックアップ混合でも、ゴールド7100回の上位5人はデッキ戦力型。実際に一つのイベントを集中周回すれば、そのイベントの登場キャラが伸びるので順位は変わる。',
        '- 全イベントを各1周した固定カード報酬だけでは三波なつみが最大4095、羽森つばさが最小660。ボックスやガチャ報酬はこの固定報酬集計から除外しており、総獲得量ではない。イベント報酬の偏りと主補正タイプの優遇は別の要因。',
        '- よって「どんな遊び方でも16人が最強」とは結論しない。しかし同じレア度・枚数の成長効率については、16人が恒常的に有利。好きなキャラを同程度の収集で強くしたい設計なら調整する理由がある。', '',
        '## 検証・再現', '',
        '- レア度確率をERBの閾値と照合。データ数・426プール・確率総和・数値例を検証。',
        '- 別方式の階層抽選（レア度→キャラ→重み付きカード）で、ゴールド710回を1000試行。4タイプの平均は理論期待値と標本誤差の範囲内で一致。',
        '- 再実行: `python tools/era_angal_work/misc/audit_card_fairness.py`。詳細な71人分の結果は `CARD_FAIRNESS_RESULTS_2026-09-14.json`。実機・実セーブを用いた通しプレイではない。', '',
        '## 根拠となる現行処理', '',
        '- `ERB/CARD_DATA_カードデータ定義.ERB`: CARD_GET_DATA、CARD_GET_CHARS_FOR_RARITY、CARD_GET_CHARPOOL。',
        '- `ERB/GACHA_ガチャシステム.ERB`: GACHA_PULL（136行～）、GACHA_PICK_NORMAL_CARD（397行～）、CARD_RECALC_BONUSES（606行～、配分643行～、倍化684行～）。',
        '- `ERB/EVENT_BOARD_イベントボード周回.ERB`: EVENT_BOARD_CALC_HAKKIICHIでカード4補正を各5倍加算。',
        '- `ERB/EVENT_BOARD_DATA_イベントデータ.ERB`: LOAD_EVENT_PICKUP_CARDS、LOAD_EVENT_REWARDS、EVENT_BOARD_IS_EVENT_CARD。', '']
    (ROOT / 'CARD_FAIRNESS_REPORT_2026-09-14.md').write_text('\n'.join(lines), encoding='utf-8')
    print('1884 cards, 426 pools checked; 1000 simulation trials verified.')
    print('\n'.join(lines[lines.index('## 通常ガチャを同じ回数引いたときのタイプ別平均'):lines.index('## ゴールド710回でカード成長の期待値が高い5人')]))


if __name__ == '__main__':
    main()
