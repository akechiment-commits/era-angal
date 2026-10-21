import unittest
import os

class TestUnawareVirginFlags(unittest.TestCase):
    def test_cflag_definition(self):
        with open("CSV/Cflag.csv", "rb") as f:
            content = f.read().decode("cp932")
        self.assertIn("1245,無自覚処女喪失", content)

    def test_tflag_definition(self):
        with open("CSV/Tflag.csv", "rb") as f:
            content = f.read().decode("cp932")
        self.assertIn("28,無自覚処女喪失発覚", content)

    def test_source_unconscious_defloration(self):
        source_path = [os.path.join("ERB", f) for f in os.listdir("ERB") if f.startswith("SOURCE_")][0]
        with open(source_path, "rb") as f:
            content = f.read().decode("cp932")
        self.assertIn("CFLAG:TARGET:1245 = 1", content)
        self.assertIn("CFLAG:TARGET:1245 == 1 && TFLAG:19 && TFLAG:899 == 0 && BASE:TARGET:0 > 0", content)
        self.assertIn("TFLAG:28 = 1", content)
        self.assertIn("CFLAG:TARGET:1245 = 2", content)
        self.assertIn("PRINTFORML 「」", content)

    def test_casino_no_unaware_flag(self):
        """Underground casino defloration should NOT set unaware virginity flag since character is aware."""
        casino_path = [os.path.join("ERB", f) for f in os.listdir("ERB") if f.startswith("CASINO_UNDERGROUND")][0]
        with open(casino_path, "rb") as f:
            content = f.read().decode("cp932")
        self.assertNotIn("1245", content)

    def test_system_fog_defloration(self):
        system_path = [os.path.join("ERB", f) for f in os.listdir("ERB") if f.startswith("SYSTEM_基本")][0]
        with open(system_path, "rb") as f:
            content = f.read().decode("cp932")
        self.assertIn("CFLAG:COUNT:1245 = 1", content)

    def test_shop_item_regeneration(self):
        shop_path = [os.path.join("ERB", f) for f in os.listdir("ERB") if f.startswith("SHOP_ITEM")][0]
        with open(shop_path, "rb") as f:
            content = f.read().decode("cp932")
        self.assertIn("CFLAG:LOCAL:1245 = 0", content)

    def test_usercom_tflag_reset(self):
        usercom_path = [os.path.join("ERB", f) for f in os.listdir("ERB") if f.startswith("USERCOM")][0]
        with open(usercom_path, "rb") as f:
            content = f.read().decode("cp932")
        self.assertIn("TFLAG:28 = 0", content)

if __name__ == "__main__":
    unittest.main()
