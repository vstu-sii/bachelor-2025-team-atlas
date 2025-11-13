-- SQLite schema for AI Pitch Deck Generator lab2.

CREATE TABLE IF NOT EXISTS examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    example_id TEXT UNIQUE NOT NULL,
    startup_name TEXT NOT NULL,
    stage TEXT,
    industry TEXT,
    language TEXT NOT NULL,
    input_brief TEXT NOT NULL,
    constraints_json TEXT,
    target_deck_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    config_json TEXT NOT NULL
);

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
