import json
import sys
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
EVAL_PATH = PROCESSED_DIR / "eval_dataset.json"

REQUIRED_SECTIONS = {"Problem", "Solution", "Market", "Business Model", "Team", "Ask"}


def load_eval_dataset(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Файл {path} не найден. Сначала запусти data_preprocessing_pipeline.py"
        )
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_required_fields(row: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not row.get("id"):
        errors.append("missing id")
    if not row.get("input_brief"):
        errors.append("missing input_brief")
    if not isinstance(row.get("target_deck"), list) or not row["target_deck"]:
        errors.append("empty target_deck")
    return errors


def check_slides_structure(row: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    slides = row.get("target_deck") or []
    if len(slides) < 6:
        errors.append(f"too_few_slides({len(slides)})")

    sections_present = set()
    for idx, slide in enumerate(slides):
        title = slide.get("title", "").strip()
        bullets = slide.get("bullets") or []
        section = slide.get("section", "").strip()

        if not title:
            errors.append(f"slide_{idx}_empty_title")
        if not isinstance(bullets, list) or not bullets:
            errors.append(f"slide_{idx}_empty_bullets")
        if section:
            sections_present.add(section)

    missing_sections = REQUIRED_SECTIONS - sections_present
    if missing_sections:
        errors.append(f"missing_sections({','.join(sorted(missing_sections))})")

    return errors


def validate_eval_dataset(path: Path) -> bool:
    rows = load_eval_dataset(path)
    if not rows:
        print("[ERROR] eval_dataset пустой")
        return False

    total = len(rows)
    failed = 0

    for row in rows:
        row_errors: List[str] = []
        row_errors.extend(check_required_fields(row))
        row_errors.extend(check_slides_structure(row))

        if row_errors:
            failed += 1
            print(f"[ROW {row.get('id')}] errors: {', '.join(row_errors)}")

    print(f"[SUMMARY] всего записей: {total}, с ошибками: {failed}")
    return failed == 0


if __name__ == "__main__":
    try:
        ok = validate_eval_dataset(EVAL_PATH)
    except FileNotFoundError as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)

    if not ok:
        sys.exit(1)
    sys.exit(0)
