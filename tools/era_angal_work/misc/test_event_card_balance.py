from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
EVENT = ROOT / "ERB/EVENT_BOARD_イベントボード周回.ERB"
GACHA = ROOT / "ERB/GACHA_ガチャシステム.ERB"
DECK = ROOT / "ERB/DECK_BATTLE_校内定期戦.ERB"


def read(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n")


class EventCardBalanceTests(unittest.TestCase):
    def test_event_score_uses_normalized_fourth_stat(self):
        text = read(EVENT)
        self.assertEqual(text.count("\tLOCAL:1 += (CFLAG:Z:306 / 2) * 5"), 1)
        self.assertEqual(text.count("CFLAG:Z:306 / 2) * 5"), 2)
        self.assertNotIn("LOCAL:1 += CFLAG:Z:306 * 5", text)
        self.assertNotIn(
            "LOCAL:3 = (CFLAG:Z:303 + CFLAG:Z:304 + CFLAG:Z:305 + CFLAG:Z:306) * 5",
            text,
        )

    def test_shared_recalc_and_school_deck_remain_unchanged(self):
        self.assertIn("CFLAG:COUNT:306 *= 2", read(GACHA))
        deck = read(DECK)
        self.assertIn("LOCAL:1 += CFLAG:ARG:306 * 2", deck)
        self.assertIn("LOCAL:1 = DECK_MEMBER_SCORE(Z)", deck)
        self.assertIn(
            "LOCAL:7 = (CFLAG:Z:303 + CFLAG:Z:304 + CFLAG:Z:305 + CFLAG:Z:306) * 2",
            deck,
        )

    def test_event_breakdown_matches_event_formula(self):
        text = read(EVENT)
        score_start = text.index("@EVENT_BOARD_CALC_HAKKIICHI")
        breakdown_start = text.index("@EVENT_BOARD_SHOW_SCORE")
        score = text[score_start:breakdown_start]
        breakdown = text[breakdown_start:]
        self.assertIn("(CFLAG:Z:306 / 2) * 5", score)
        self.assertIn("CFLAG:Z:306 / 2) * 5", breakdown)

    def test_files_are_cp932_crlf(self):
        for path in (EVENT, GACHA, DECK):
            raw = path.read_bytes()
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""), path.name)
            raw.decode("cp932")


if __name__ == "__main__":
    unittest.main()
