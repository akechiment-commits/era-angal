"""Memory potion preserves the body and transfers childcare using actual ERB helpers."""
import re
import unittest
from test_master_ability_purchase import source, function
from test_audit4_fixes import run

SHOP = source('SHOP_ITEM*')
PREG = source('EVENT_N_妊娠*')

def evaluate(body, state):
    body = body.replace('\r\n', '\n')
    # Model string copies separately; numeric arrays use the existing ERB evaluator.
    body = re.sub(r"(?m)^.*'=.*$", '', body)
    body = re.sub(r'(?m)^FOR LOCAL, 2000, 2100\n(.*?)\nNEXT',
                  lambda m: '\n'.join(m[1].replace(':LOCAL', ':' + str(i)) for i in range(2000, 2100)),
                  body, flags=re.S)
    aliases = {'C': state.get('C', 0), 'D': state.get('D', 0),
               'ARG': state.get('ARG', 0), 'RESULT': state.get('RESULT', 0)}
    body = re.sub(r'\b(TALENT|MARK|EXP|ABL):([A-Z]+):',
                  lambda m: m[1] + ':' + str(aliases[m[2]]) + ':', body)
    body = re.sub(r'(?m)^([ \t]*)RETURNF (.*)$', r'\1ANSWER = \2\n\1RETURN 0', body)
    body = re.sub(r'SIF ([^\n]+)\n([ \t]*)ANSWER = ([^\n]+)\n[ \t]*RETURN 0',
                  r'IF \1\n\2ANSWER = \3\n\2RETURN 0\nENDIF', body)
    body = body.replace('CALL SELECT_NURSE, LOCAL:0', 'NURSE_MENU = LOCAL:0 + 1')
    return run(body, state)

class MemoryDrugTests(unittest.TestCase):
    def test_actual_body_copy_preserves_changes_and_general_skills(self):
        indices = {'CFLAG': [96,109,112,1100,1101,1102,1103,1270,1271,1272,1280,1281,1282,1283,2001,2071,2099],
                   'TALENT': [131,132,133,135,136,141,143,144,145,146,149,154,300,301,589,596,597],
                   'ABL': [90,93,94,95,98], 'EXP': [95,96,99,100],
                   'BASE': [1,3], 'MAXBASE': [1]}
        initial = {'C': 2, 'D': 1}
        for array, nums in indices.items():
            for n in nums:
                initial[f'{array}:1:{n}'] = n + 123
        result = evaluate(function(SHOP, 'MEMORY_DRUG_KEEP_BODY'), initial)
        for array, nums in indices.items():
            for n in nums:
                self.assertEqual(result[f'{array}:2:{n}'], n + 123, (array,n))
        self.assertEqual(result['ABL:2:2'], 0)  # Training technique still resets.
        self.assertEqual(result['CFLAG:2:2'], 0)  # Affection still resets.

    def test_care_end_restores_recovery_and_keeps_physical_sizes(self):
        for original in (0,1,2):
            initial = {'ARG': 2, 'TALENT:2:135': 1, 'MARK:2:90': 1,
                       'TALENT:2:112': 1, 'CFLAG:2:96': original,
                       'CFLAG:2:1101': 1040, 'CFLAG:2:1103': 172,
                       'TALENT:2:130': 1, 'CFLAG:2:2001': 3}
            result = evaluate(function(PREG, 'MEMORY_DRUG_END_CARE'), initial)
            self.assertEqual(result['TALENT:2:135'], 0)
            self.assertEqual(result['MARK:2:90'], 0)
            self.assertEqual(result['CFLAG:2:96'], 0)
            self.assertEqual(result['TALENT:2:111'], int(original==1))
            self.assertEqual(result['TALENT:2:112'], int(original==2))
            self.assertEqual(result['NURSE_MENU'], 3)
            for key in ('CFLAG:2:1101','CFLAG:2:1103','TALENT:2:130','CFLAG:2:2001'):
                self.assertEqual(result[key],initial[key])

    def test_pregnant_and_non_parent_skip_care_menu(self):
        for initial in ({'TALENT:2:134':1,'MARK:2:90':1,'CFLAG:2:110':120}, {}):
            result = evaluate(function(PREG, 'MEMORY_DRUG_END_CARE'), {'ARG':2,**initial})
            self.assertEqual(result['NURSE_MENU'],0)
            for key,value in initial.items(): self.assertEqual(result[key],value)

    def test_orphaned_legacy_room_flag_is_also_released(self):
        result=evaluate(function(PREG,'MEMORY_DRUG_END_CARE'),
                        {'ARG':2,'MARK:2:90':1,'TALENT:2:111':1})
        self.assertEqual(result['MARK:2:90'],0)
        self.assertEqual(result['TALENT:2:111'],1)
        self.assertEqual(result['NURSE_MENU'],3)

    def test_nurse_eligibility_excludes_patient_absent_and_pregnant(self):
        body=function(PREG,'CAN_NURSE')
        for actor,excluded,extras,expected in [
            (1,2,{'TALENT:1:136':1},1),(1,2,{'TALENT:1:135':1},1),
            (1,1,{'TALENT:1:136':1},0),(1,2,{'TALENT:1:136':1,'CFLAG:1:21':1},0),
            (1,2,{'TALENT:1:136':1,'TALENT:1:134':1},0),(1,2,{},0),
            (-1,2,{},0),(3,2,{},0)]:
            result=evaluate(body,{'ARG':actor,'ARG:1':excluded,'CHARANUM':3,**extras})
            self.assertEqual(result['ANSWER'],expected)
        self.assertNotRegex(body,r'\b[CD] =') # Does not overwrite birth event's global C.

    def test_existing_nurse_retains_original_recovery_record(self):
        block=function(PREG,'SELECT_NURSE').split(';育児期間を設定する',1)[1]
        block=block[:block.rindex('ENDIF')]
        for recorded in (0,1,2):
            result=evaluate(block,{'RESULT':1,'DAY:7':100,'TALENT:1:135':1,
                                   'TALENT:1:112':1,'CFLAG:1:96':recorded})
            self.assertEqual(result['CFLAG:1:96'],recorded)
            self.assertEqual(result['CFLAG:1:110'],100)
            self.assertEqual(result['MARK:1:90'],1)

    def test_adoption_never_indexes_array_and_copy_precedes_deletion(self):
        menu=function(PREG,'SELECT_NURSE')
        adoption=menu[menu.index('IF RESULT == -1'):menu.index('ELSEIF RESULT < 0')]
        for size,choice,expected in [(3,100,1),(3,-1,1),(3,1000,1),(101,100,0),(101,1000,1)]:
            guard=adoption.splitlines()[0][3:]
            guard=guard.replace('CHARANUM',str(size)).replace('RESULT',str(choice))
            self.assertEqual(bool(eval(guard.replace('||',' or ').replace('&&',' and '))),bool(expected))
        self.assertIn('RETURN 0',adoption)
        self.assertNotIn('CFLAG:',adoption)
        memory=SHOP.split(';記憶消去\r\nIF BOUGHT == 98',1)[1].split(';単体エンド',1)[0]
        self.assertLess(memory.index('CALL MEMORY_DRUG_KEEP_BODY'),memory.index('DELCHARA R'))
        self.assertLess(memory.index('DELCHARA R'),memory.index('CALL MEMORY_DRUG_END_CARE'))
        self.assertIn('SIF R == ASSI',memory)
        self.assertIn('TALENT:TARGET:151 = TALENT:R:151',memory)
        self.assertIn('CFLAG:TARGET:KOJO_VERSION = CFLAG:R:KOJO_VERSION',memory)
        self.assertIn('SIF TALENT:R:153',memory)
        self.assertIn('CALL SELECT_NURSE, LOCAL:0',function(PREG,'MEMORY_DRUG_END_CARE'))

if __name__=='__main__': unittest.main()
