"""Preserve pre-pregnancy milk trait; protect dormant player birth branch."""
import unittest
from test_master_ability_purchase import source, function
from test_memory_drug import evaluate

PREG = source('EVENT_N_妊娠*')

class CareMilkTests(unittest.TestCase):
    def record(self, state):
        return evaluate(function(PREG,'RECORD_PRE_CARE_MILK'), {'ARG':1,**state})

    def end(self,state):
        body=function(PREG,'END_CARE_MILK').replace(
            'CALL BUST_ADJUST, ARG, -(RAND:31 + 30)', 'MILK_SHRINK += 1')
        return evaluate(body,{'ARG':1,**state})

    def test_original_trait_survives_and_repeated_record_does_not_change_it(self):
        recorded=self.record({'TALENT:1:130':1})
        self.assertEqual(recorded['CFLAG:1:1284'],2)
        ended=self.end(self.record(recorded))
        self.assertEqual(ended['TALENT:1:130'],1)
        self.assertEqual(ended['MILK_SHRINK'],0)
        self.assertEqual(ended['CFLAG:1:1284'],0)

    def test_new_trait_is_removed_and_random_shrink_runs_only_once(self):
        recorded=self.record({})
        self.assertEqual(recorded['CFLAG:1:1284'],1)
        recorded['TALENT:1:130']=1
        recorded=self.record(recorded) # Birth must not reinterpret pregnancy record.
        ended=self.end(recorded)
        self.assertEqual(ended['TALENT:1:130'],0)
        self.assertEqual(ended['MILK_SHRINK'],1)
        self.assertEqual(self.end(ended)['MILK_SHRINK'],1)

    def test_legacy_and_already_absent_trait_are_not_removed_or_shrunk(self):
        for recorded,present in [(0,1),(0,0),(1,0),(2,1)]:
            ended=self.end({'CFLAG:1:1284':recorded,'TALENT:1:130':present})
            self.assertEqual(ended['TALENT:1:130'],present)
            self.assertEqual(ended['MILK_SHRINK'],0)

    def test_lifecycle_records_before_birth_and_nurse_effects_and_copies_to_new_character(self):
        change=function(PREG,'CHANGE_N_STATUS')
        self.assertLess(change.index('CALL RECORD_PRE_CARE_MILK, T'),change.index('MAXBASE:T:0 -= 500'))
        birth=function(PREG,'CHILD_BIRTH')
        self.assertLess(birth.index('CALL RECORD_PRE_CARE_MILK, C'),birth.index('TALENT:C:130 = 1'))
        nurse=function(PREG,'SELECT_NURSE')
        self.assertIn('SIF TALENT:RESULT:135 == 0\r\n\t\tCALL RECORD_PRE_CARE_MILK, RESULT',nurse)
        self.assertIn('CALL END_CARE_MILK, C',function(PREG,'DEPEARENT'))
        self.assertIn('CFLAG:C:1284 = CFLAG:D:1284',function(source('SHOP_ITEM*'),'MEMORY_DRUG_KEEP_BODY'))
        self.assertIn('CFLAG:ARG:1284 = 0',function(PREG,'MEMORY_DRUG_END_CARE'))
        # Pregnancy size reversal continues to use its own random draw.
        self.assertIn('CALL BUST_ADJUST, C, -(RAND:51 + 40)',function(PREG,'REVERSE_B_SIZE'))

    def test_dormant_player_birth_checks_bounds_before_reading_father(self):
        branch=function(PREG,'CHILD_BIRTH').split('IF C == MASTER',1)[1].split('\r\nELSE\r\n',1)[0]
        for father in (-1,-999,3,999):
            result=evaluate(branch.replace('TALENT:E:',f'TALENT:{father}:'),{'E':father,'CHARANUM':3})
            self.assertEqual(result['Y'],-1)
            self.assertEqual(result['TFLAG:17'],2)
        for away,love,y,kind in [(1,1,-1,2),(0,1,1,1),(0,0,1,2)]:
            result=evaluate(branch.replace('TALENT:E:','TALENT:1:'),{'E':1,'CHARANUM':3,'CFLAG:1:21':away,'TALENT:1:85':love})
            self.assertEqual(result['Y'],y)
            self.assertEqual(result['TFLAG:17'],kind)
        self.assertLess(branch.index('IF E < 0 || E >= CHARANUM'),branch.index('CFLAG:E:21'))

if __name__=='__main__': unittest.main()
