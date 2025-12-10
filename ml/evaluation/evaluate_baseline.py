import json
from pathlib import Path
from typing import Any, Dict, List

from ml.models.baseline import generate_deck
from ml.prompt_templates import PitchDeckPromptConfig
from ml.evaluation.metrics import evaluate_pair
from ml.evaluation.hallucination import numeric_hallucinations


BASE_DIR = Path(__file__).resolve().parents[2]  # корень проекта
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
EVAL_PATH = PROCESSED_DIR / "eval_dataset.json"
RESULTS_DIR = BASE_DIR / "ml" / "evaluation" / "results"


def load_eval_dataset(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Файл {path} не найден. Сначала запусти data_preprocessing_pipeline.py"
        )
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def aggregate(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    if not metrics_list:
        return {}
    keys = metrics_list[0].keys()
    agg: Dict[str, float] = {}
    n = len(metrics_list)
    for k in keys:
        s = sum(m.get(k, 0.0) for m in metrics_list)
        agg[k] = s / n
    return agg


def main() -> None:
    rows = load_eval_dataset(EVAL_PATH)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    per_sample: List[Dict[str, Any]] = []
    metrics_only: List[Dict[str, float]] = []

    for row in rows:
        brief: str = row["input_brief"]
        target_deck = {"slides": row["target_deck"]}
        cfg_raw = row.get("config") or {}

        config = PitchDeckPromptConfig(
            target_slide_count=cfg_raw.get("target_slide_count", 10),
            tone=cfg_raw.get("tone", "formal"),
            audience=cfg_raw.get("audience", "early-stage VC"),
            language=row.get("language", "en"),
        )

        print(f"[INFO] Генерация дека для стартапа {row['id']}...")

        generated_deck = generate_deck(brief=brief, config=config)

        m = evaluate_pair(
            input_brief=brief,
            target_deck=target_deck,
            generated_deck=generated_deck,
            target_slide_count=config.target_slide_count,
        )
        h = numeric_hallucinations(
            input_brief=brief,
            target_deck=target_deck,
            generated_deck=generated_deck,
        )

        sample_result: Dict[str, Any] = {
            "id": row["id"],
            "name": row.get("name"),
            "metrics": m | h,
        }
        per_sample.append(sample_result)
        metrics_only.append(m | h)

    agg = aggregate(metrics_only)

    # сохраняем подробный и агрегированный результаты
    with (RESULTS_DIR / "baseline_per_sample.json").open("w", encoding="utf-8") as f:
        json.dump(per_sample, f, ensure_ascii=False, indent=2)

    with (RESULTS_DIR / "baseline_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(agg, f, ensure_ascii=False, indent=2)

    print("[OK] Результаты сохранены в ml/evaluation/results/")
    print("Агрегированные метрики:")
    for k, v in agg.items():
        print(f"  {k}: {v:.4f}")


if __name__ == "__main__":
    main()
