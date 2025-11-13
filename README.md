[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/P3ZvldYO)
# sii-project-template

Фокус лабораторной:

- Анализ требований к LLM / VLM моделям
- Исследование подходящих AI-методов и архитектур
- Определение метрик качества (accuracy, latency, hallucination)
- Планирование экспериментов и базового набора данных (dataset)
- Предоставление запускаемого базового кода (датасет + метрики + эксперимент + локальная БД SQLite)

---

Структура репозитория

README.md
.env.example        # Пример файла с переменными окружения для LLM-провайдеров
requirements.txt    # Python-зависимости (минимальные)
data
   base_dataset.jsonl   # Маленький базовый датасет (brief → эталонный pitch deck)
   schema.sql           # Схема SQLite для примеров, экспериментов и предсказаний
   init_sqlite_db.py    # Скрипт инициализации БД и загрузки базового датасета
ml
   __init__.py
   model_clients.py     # Абстракция клиента модели + оффлайновая baseline-модель (Echo)
   metrics.py           # Метрики: coverage / structure / similarity / proxy-hallucination
   experiment_runner.py # Запуск эксперимента и логирование результатов в SQLite
reports
   llm_vlm_requirements.md         # Анализ требований к LLM/VLM
   methods_and_architecture.md     # Обзор методов и целевой архитектуры
   experiments_and_dataset_plan.md # План экспериментов и датасета

    
Как запустить локально
Рекомендуемая версия Python: 3.10+

Создать и активировать виртуальное окружение (по желанию, но желательно):

python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# или
.\.venv\Scripts\activate    # Windows

Установить зависимости:

pip install -r requirements.txt
Инициализировать SQLite-базу и загрузить базовый датасет:

python data/init_sqlite_db.py
Это создаст файл data/pitchdeck_lab2.db со следующими таблицами:

examples – базовые примеры стартапов (brief + эталонный pitch deck)

experiments – метаданные экспериментов

predictions – выходы моделей и вычисленные метрики

Запустить базовый эксперимент (оффлайновая Echo-модель):
python -m ml.experiment_runner

В результате:

Загружаются примеры из data/base_dataset.jsonl

Используется EchoModelClient (простая шаблонная baseline-модель)

Считаются метрики:
coverage
structure
lexical_similarity
hallucination_proxy

Результаты сохраняются в data/pitchdeck_lab2.db в таблицы experiments и predictions
