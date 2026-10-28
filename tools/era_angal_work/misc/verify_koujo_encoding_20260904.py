from __future__ import annotations

from pathlib import Path


def main() -> int:
    bad: list[str] = []
    for path in sorted((Path(__file__).resolve().parents[1] / "ERB" / "CHAR").glob("CHAR_*_COM.ERB")):
        raw = path.read_bytes()
        try:
            raw.decode("cp932")
        except UnicodeDecodeError as exc:
            bad.append(f"{path.name}: CP932 decode: {exc}")
        if b"\n" in raw.replace(b"\r\n", b""):
            bad.append(f"{path.name}: lone LF")
    print(f"encoding_crlf_bad={len(bad)}")
    print("\n".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
