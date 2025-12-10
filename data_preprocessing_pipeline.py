import json
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def load_json(path: Path) -> List[Dict[str, Any]]:
    """Загрузка JSON-массива из файла."""
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, rows: List[Dict[str, Any]]) -> None:
    """Сохранение списка словарей в JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def build_eval_dataset() -> List[Dict[str, Any]]:
    """
    Собирает eval-набор:
    - на входе: raw/startup_briefs.json + raw/pitch_decks_examples.json
    - на выходе: processed/eval_dataset.json
    Каждая запись: (бриф стартапа, метаданные, эталонный дек).
    """
    briefs_path = RAW_DIR / "startup_briefs.json"
    decks_path = RAW_DIR / "pitch_decks_examples.json"
    output_path = PROCESSED_DIR / "eval_dataset.json"

    briefs = load_json(briefs_path)
    decks = load_json(decks_path)

    decks_by_startup_id: Dict[str, Dict[str, Any]] = {}
    for deck in decks:
        startup_id = deck.get("startup_id")
        if not startup_id:
            continue
        decks_by_startup_id[startup_id] = deck

    eval_rows: List[Dict[str, Any]] = []
    for brief in briefs:
        startup_id = brief.get("id")
        if not startup_id:
            continue

        deck = decks_by_startup_id.get(startup_id)
        if deck is None:
            # можно залогировать warning, но не падать
            print(f"[WARN] Нет дека для стартапа {startup_id}")
            continue

        row = {
            "id": startup_id,
            "name": brief.get("name"),
            "industry": brief.get("industry"),
            "stage": brief.get("stage"),
            "language": brief.get("language", "en"),
            "input_brief": brief.get("brief", "").strip(),
            "config": brief.get("constraints", {}),
            "target_deck": deck.get("slides", []),
        }

        # простая нормализация
        if not row["input_brief"]:
            print(f"[WARN] Пустой бриф, пропуск: {startup_id}")
            continue

        # фильтруем пустые буллеты
        cleaned_slides = []
        for slide in row["target_deck"]:
            bullets = slide.get("bullets") or []
            cleaned_bullets = [b.strip() for b in bullets if isinstance(b, str) and b.strip()]
            cleaned_slides.append(
                {
                    "section": slide.get("section", "").strip(),
                    "title": slide.get("title", "").strip(),
                    "bullets": cleaned_bullets,
                }
            )
        row["target_deck"] = cleaned_slides

        eval_rows.append(row)

    save_json(output_path, eval_rows)
    print(f"[OK] Создан eval_dataset: {output_path} (записей: {len(eval_rows)})")
    return eval_rows


if __name__ == "__main__":
    build_eval_dataset()
