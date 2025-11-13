"""
Experiment runner for AI Pitch Deck Generator models.

- Loads dataset examples from JSONL
- Runs one or several model clients
- Computes metrics and logs results into a SQLite DB
"""

from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from ml.model_clients import ModelConfig, EchoModelClient
from ml.metrics import compute_all_metrics


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "base_dataset.jsonl"
DB_PATH = ROOT / "data" / "pitchdeck_lab2.db"


def load_dataset(path: Path) -> List[Dict]:
    examples: List[Dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            examples.append(json.loads(line))
    return examples


def ensure_db_schema(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            model_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            config_json TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id INTEGER NOT NULL,
            example_id TEXT NOT NULL,
            model_name TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            output_deck_json TEXT NOT NULL,
            coverage REAL,
            structure REAL,
            lexical_similarity REAL,
            hallucination_proxy REAL,
            FOREIGN KEY (experiment_id) REFERENCES experiments (id)
        );
        """
    )

    conn.commit()
    conn.close()


def create_experiment(conn: sqlite3.Connection, name: str, config: ModelConfig) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO experiments (name, model_name, created_at, config_json)
        VALUES (?, ?, datetime('now'), ?);
        """,
        (name, config.name, json.dumps(asdict(config))),
    )
    conn.commit()
    return cur.lastrowid


def run_experiment(
    experiment_name: str = "lab2_baseline_echo",
) -> None:
    ensure_db_schema(DB_PATH)
    examples = load_dataset(DATA_PATH)

    # Single baseline model for lab2
    config = ModelConfig(
        name="echo-baseline-v1",
        provider="offline",
        mode="llm",
        max_tokens=2048,
        temperature=0.0,
    )
    model = EchoModelClient(config=config)

    conn = sqlite3.connect(DB_PATH)
    exp_id = create_experiment(conn, experiment_name, config)
    cur = conn.cursor()

    for ex in examples:
        brief = ex["input_brief"]
        constraints = ex.get("constraints", {})
        ref_deck = ex["target_deck"]

        start = time.perf_counter()
        gen_deck = model.generate_deck(brief, constraints)
        latency_ms = (time.perf_counter() - start) * 1000.0

        m = compute_all_metrics(ref_deck=ref_deck, gen_deck=gen_deck, input_brief=brief)

        cur.execute(
            """
            INSERT INTO predictions (
                experiment_id,
                example_id,
                model_name,
                latency_ms,
                output_deck_json,
                coverage,
                structure,
                lexical_similarity,
                hallucination_proxy
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                exp_id,
                ex["id"],
                config.name,
                latency_ms,
                json.dumps(gen_deck, ensure_ascii=False),
                m.coverage,
                m.structure,
                m.lexical_similarity,
                m.hallucination_proxy,
            ),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    run_experiment()
