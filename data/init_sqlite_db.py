"""
Initialize local SQLite DB for AI Pitch Deck Generator lab2
and populate it with base examples from JSONL.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "base_dataset.jsonl"
DB_PATH = ROOT / "data" / "pitchdeck_lab2.db"
SCHEMA_PATH = ROOT / "data" / "schema.sql"


def apply_schema(conn: sqlite3.Connection, schema_path: Path) -> None:
    with schema_path.open("r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()


def load_examples(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    apply_schema(conn, SCHEMA_PATH)

    cur = conn.cursor()
    for ex in load_examples(DATASET_PATH):
        cur.execute(
            """
            INSERT OR IGNORE INTO examples (
                example_id,
                startup_name,
                stage,
                industry,
                language,
                input_brief,
                constraints_json,
                target_deck_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                ex["id"],
                ex["startup_name"],
                ex.get("stage"),
                ex.get("industry"),
                ex.get("language", "en"),
                ex["input_brief"],
                json.dumps(ex.get("constraints", {}), ensure_ascii=False),
                json.dumps(ex["target_deck"], ensure_ascii=False),
            ),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
