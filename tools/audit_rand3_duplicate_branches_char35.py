from pathlib import Path

try:
    import audit_rand3_duplicate_branches_char34 as audit
except ImportError:
    from tools import audit_rand3_duplicate_branches_char34 as audit


audit.TARGET = Path(__file__).resolve().parents[1] / "ERB" / "CHAR" / "CHAR_35_梅園かな_COM.ERB"


if __name__ == "__main__":
    audit.main()
