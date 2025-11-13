# AI Pitch Deck Generator

Фокус лабораторной:

- Анализ требований к LLM / VLM моделям
- Исследование подходящих AI-методов и архитектур
- Определение метрик качества (accuracy, latency, hallucination)
- Планирование экспериментов и базового набора данных (dataset)
- Предоставление запускаемого базового кода (датасет + метрики + эксперимент + локальная БД SQLite)

---

## Структура репозитория

```text
.
├── README.md
├── .env.example        # Пример файла с переменными окружения для LLM-провайдеров
├── requirements.txt    # Python-зависимости (минимальные)
├── data
│   ├── base_dataset.jsonl   # Маленький базовый датасет (brief → эталонный pitch deck)
│   ├── schema.sql           # Схема SQLite для примеров, экспериментов и предсказаний
│   └── init_sqlite_db.py    # Скрипт инициализации БД и загрузки базового датасета
├── ml
│   ├── __init__.py
│   ├── model_clients.py     # Абстракция клиента модели + оффлайновая baseline-модель (Echo)
│   ├── metrics.py           # Метрики: coverage / structure / similarity / proxy-hallucination
│   └── experiment_runner.py # Запуск эксперимента и логирование результатов в SQLite
└── reports
    ├── llm_vlm_requirements.md         # Анализ требований к LLM/VLM
    ├── methods_and_architecture.md     # Обзор методов и целевой архитектуры
    └── experiments_and_dataset_plan.md # План экспериментов и датасета
