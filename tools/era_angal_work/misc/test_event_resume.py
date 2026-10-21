"""Focused source-driven checks for monthly menus and saved board state.

The small executor supports only the integer/state instructions used by the
save/load/reset helpers. It is not an Emuera runtime or a UI test.
"""
from collections import defaultdict
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BOARD = (ROOT / 'ERB/EVENT_BOARD_イベントボード周回.ERB').read_bytes().decode('cp932').replace('\r\n', '\n')
DATA = (ROOT / 'ERB/EVENT_BOARD_DATA_イベントデータ.ERB').read_bytes().decode('cp932').replace('\r\n', '\n')


def body(text, name):
    return re.search(r'^@' + name + r'(?:\([^\n]*\))?\n(.*?)(?=^@|\Z)', text, re.M | re.S)[1]


def expression(value):
    value = re.sub(r'FLAG:\(([^()]*)\)', r'flags[\1]', value)
    value = re.sub(r'FLAG:(\d+)', r'flags[\1]', value)
    value = re.sub(r'DAY:(\d+)', r'day[\1]', value)
    value = value.replace('ARG:1', 'arg1').replace('ARG', 'arg')
    return value.replace('||', ' or ').replace('&&', ' and ')


def execute(name, flags, day=None, arg=0, arg1=0):
    lines = ['def compiled():']
    level = 1
    single = False
    for source in body(BOARD, name).splitlines():
        line = source.split(';', 1)[0].strip()
        if not line:
            continue
        if line.startswith('#DIM DYNAMIC '):
            line = line.split()[2].rstrip(',') + ' = 0'
        if line in ('NEXT', 'REND', 'ENDIF'):
            level -= 1
            continue
        prefix = '    ' * level
        if line.startswith('SIF '):
            lines.append(prefix + 'if ' + expression(line[4:]) + ':')
            single = True
            continue
        if line.startswith('IF '):
            lines.append(prefix + 'if ' + expression(line[3:]) + ':')
            level += 1
            continue
        if line.startswith('FOR '):
            var, start, end = line[4:].split(',')
            lines.append(prefix + f'for {var} in range({start},{end}):')
            level += 1
            continue
        if line.startswith('REPEAT '):
            lines.append(prefix + f'for COUNT in range({line[7:]}):')
            level += 1
            continue
        if line.startswith('CALL '):
            line = f"execute('{line[5:]}', flags, day)"
        elif line.startswith('RETURN '):
            line = 'return ' + expression(line[7:])
        elif re.match(r'[A-Z_][A-Z_0-9]*(?::[^=]+)? = ', line):
            line = expression(line)
        else:
            raise AssertionError(f'Unsupported instruction: {line}')
        lines.append(prefix + ('    ' if single else '') + line)
        single = False
    namespace = dict(flags=flags, day=day or {}, arg=arg, arg1=arg1, execute=execute)
    exec('\n'.join(lines), namespace)
    return namespace['compiled']()


class EventResumeTests(unittest.TestCase):
    def test_all_month_menus_and_reward_routes(self):
        month_body = body(DATA, 'LOAD_MONTH_EVENTS')
        pickups = body(DATA, 'LOAD_EVENT_PICKUP_CARDS')
        rewards = body(DATA, 'LOAD_EVENT_REWARDS')
        count = 0
        for month in range(1, 13):
            region = re.search(r'^CASE ' + str(month) + r'\n(.*?)(?=^CASE|^ENDSELECT)', month_body, re.M | re.S)[1]
            size = int(re.search(r'RETURN (\d+)', region)[1])
            slots = set(map(int, re.findall(r'TSTR:(\d+) =', region)))
            self.assertEqual(slots, set(range(100, 100 + size)))
            for choice in range(size):
                slot = execute('EVENT_BOARD_MENU_SLOT', {}, arg=month, arg1=choice)
                key = (month - 1) * 6 + slot
                self.assertRegex(pickups, rf'(?m)^CASE {key}\s')
                self.assertRegex(rewards, rf'(?m)^CASE {key}\s')
            count += size
        self.assertEqual(count, 56)
        self.assertEqual(execute('EVENT_BOARD_MENU_SLOT', {}, arg=7, arg1=4), 5)
        july = body(DATA, 'EVENT_BOARD_GET_EVENT_INDEX').split('CASE 7\n')[1].split('CASE 8\n')[0]
        self.assertIn('RETURN 55', july)
        self.assertIn('SIF FLAG:68 == 4\n\t\tRETURN -1', july)

    def test_roundtrip_and_event_isolation(self):
        flags = defaultdict(int)
        for slot in range(6):
            flags[68] = slot
            for offset in range(8):
                flags[15050 + offset] = slot * 100 + offset + 1
            execute('EVENT_BOARD_STATE_SAVE', flags)
        for slot in (0, 5, 2, 1, 4, 3, 0):
            flags[68] = slot
            execute('EVENT_BOARD_STATE_LOAD', flags)
            self.assertEqual([flags[15050 + i] for i in range(8)], [slot * 100 + i + 1 for i in range(8)])

    def test_existing_save_import_only_once(self):
        flags = defaultdict(int, {68: 5, 15050: 18, 15054: 7, 15055: 90, 15056: 2, 15057: 50})
        execute('EVENT_BOARD_STATE_INIT', flags)
        flags[15055] = 0
        execute('EVENT_BOARD_STATE_INIT', flags)
        execute('EVENT_BOARD_STATE_LOAD', flags)
        self.assertEqual([flags[i] for i in (15050, 15054, 15055, 15056, 15057)], [18, 7, 90, 2, 50])

    def test_month_change_clears_every_slot_but_not_player_level(self):
        flags = defaultdict(int, {67: 107, 15070: 12, 15071: 456})
        for i in range(15300, 15348):
            flags[i] = i
        execute('EVENT_BOARD_MONTHLY_RESET', flags, {3: 1, 8: 7})
        self.assertEqual(flags[15300], 15300)
        execute('EVENT_BOARD_MONTHLY_RESET', flags, {3: 1, 8: 8})
        self.assertEqual([flags[i] for i in range(15300, 15348)], [0] * 48)
        self.assertEqual([flags[i] for i in range(15050, 15058)], [0] * 8)
        self.assertEqual((flags[15070], flags[15071]), (12, 456))

    def test_main_uses_save_load_and_preserves_menu_identity(self):
        main = body(BOARD, 'EVENT_BOARD_MAIN')
        self.assertLess(main.index('CALL EVENT_BOARD_STATE_INIT'), main.index('FLAG:68 = RESULT'))
        self.assertLess(main.index('TSTR:99 = %TSTR:A%'), main.index('CALL EVENT_BOARD_MENU_SLOT'))
        self.assertIn('$BOARD_LOOP\n;各操作の結果を保存する。退出・別イベントへの切替後もここから再開する。\nCALL EVENT_BOARD_STATE_SAVE', main)
        self.assertIn('CALL EVENT_BOARD_STATE_LOAD', main)
        self.assertNotIn('FLAG:15055 = 0', main)
        self.assertNotIn('FLAG:15050 = 0', main)

    def test_generator_keeps_fixed_titles_and_story_ids(self):
        path = ROOT / 'tools/era_angal_work/scripts/add_main_story_election_events.py'
        spec = importlib.util.spec_from_file_location('event_generator', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.update_month_titles(DATA), DATA)
        self.assertEqual(module.update_event_index(DATA), DATA)


if __name__ == '__main__':
    unittest.main()
