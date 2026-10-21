from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import UnityPy


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "server_assets" / "addressable" / "resources" / "Android" / "packedassets_assets_assets" / "story"
TEXT_OUT = ROOT / "tools" / "scenarios_packedassets"
JSON_OUT = ROOT / "tools" / "scenarios_packedassets_json"
MANIFEST = TEXT_OUT / "manifest.csv"


def text_asset_payload(bundle: Path) -> str:
    env = UnityPy.load(str(bundle))
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        data = obj.read()
        raw = getattr(data, "script", None)
        if raw is None:
            raw = getattr(data, "m_Script", None)
        if raw is None:
            raw = getattr(data, "data", None)
        if raw is None:
            raw = getattr(data, "m_Data", None)
        if isinstance(raw, bytes):
            return raw.decode("utf-8-sig")
        return str(raw or "")
    raise ValueError("TextAsset not found")


def parse_commands(raw: str):
    value = json.loads(raw)
    if isinstance(value, dict) and isinstance(value.get("script"), str):
        value = json.loads(value["script"])
    if not isinstance(value, list):
        raise ValueError("story payload is not a command list")
    return value


def main() -> None:
    TEXT_OUT.mkdir(parents=True, exist_ok=True)
    JSON_OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    bundles = sorted(SOURCE.glob("*.bundle"), key=lambda path: int(re.match(r"^(\d+)", path.name).group(1)))
    for index, bundle in enumerate(bundles, start=1):
        match = re.match(r"^(\d+)\.json_", bundle.name)
        if not match:
            continue
        story_id = int(match.group(1))
        status = "ok"
        error = ""
        commands = []
        raw = ""
        try:
            raw = text_asset_payload(bundle)
            commands = parse_commands(raw)
            (JSON_OUT / f"{story_id}.json").write_text(
                json.dumps(commands, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            talks = [command for command in commands if command.get("command") == "talk"]
            text_file = ""
            if talks:
                lines = [f"=== {story_id} ===", ""]
                lines.extend(f"【{talk.get('speaker', '')}】{talk.get('text', '')}" for talk in talks)
                text_file = f"{story_id}.txt"
                (TEXT_OUT / text_file).write_text("\n".join(lines), encoding="utf-8")
        except Exception as exc:
            status = "error"
            error = f"{type(exc).__name__}: {exc}"
            talks = []
            text_file = ""
        rows.append(
            {
                "id": story_id,
                "source": str(bundle.relative_to(ROOT)).replace("\\", "/"),
                "commands": len(commands),
                "talks": len(talks),
                "text_file": text_file,
                "status": status,
                "error": error,
            }
        )
        if index % 250 == 0 or index == len(bundles):
            print(f"processed={index}/{len(bundles)}", flush=True)

    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "source", "commands", "talks", "text_file", "status", "error"])
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: int(row["id"])))

    print(f"bundles={len(rows)}")
    print(f"text_files={sum(bool(row['text_file']) for row in rows)}")
    print(f"errors={sum(row['status'] != 'ok' for row in rows)}")
    print(f"manifest={MANIFEST}")


if __name__ == "__main__":
    main()
