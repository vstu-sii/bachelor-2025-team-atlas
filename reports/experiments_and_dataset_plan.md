
---

## `reports/experiments_and_dataset_plan.md`

```markdown
# План экспериментов и датасета – AI Pitch Deck Generator

## 1. Дизайн датасета

### 1.1. Схема примера (JSONL)

Каждая строка в `base_dataset.jsonl` имеет вид:

```json
{
  "id": "ex001",
  "startup_name": "FinSight AI",
  "stage": "pre-seed",
  "industry": "fintech",
  "language": "en",
  "input_brief": "Текстовое описание стартапа / интервью с основателем...",
  "constraints": {
    "tone": "confident",
    "language": "en"
  },
  "target_deck": {
    "slides": [
      {
        "index": 1,
        "title": "Problem",
        "goal": "Объяснить ключевую боль...",
        "key_points": ["...", "..."],
        "visuals_description": "..."
      }
    ]
  }
}
