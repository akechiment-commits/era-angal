from pathlib import Path

try:
    import audit_rand3_similar_branches_char34 as audit
except ImportError:
    from tools import audit_rand3_similar_branches_char34 as audit


audit.TARGET = Path(__file__).resolve().parents[1] / "ERB" / "CHAR" / "CHAR_36_遠見ちか_COM.ERB"


if __name__ == "__main__":
    audit.main()
