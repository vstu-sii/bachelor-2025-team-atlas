graph TB
    %% Основные компоненты системы
    subgraph "AutoPitch Deck Generator"
        A2["A2: Frontend<br/>Веб-интерфейс React"]
        A3["A3: Backend API<br/>FastAPI сервер"]
        A4["A4: File Parser<br/>Парсинг PPTX/PDF"]
        A5["A5: LLM Optimizer<br/>AI-оптимизация текста"]
        A6["A6: Design Engine<br/>Дизайн-движок"]
        A7["A7: База данных<br/>PostgreSQL + Redis"]
        A8["A8: Export Module<br/>PPTX/PDF генератор"]
        A9["A9: Task Queue<br/>Celery + Redis"]
    end

    %% Пользователь
    A1["👨‍💼 Предприниматель"] -->|"1. Загружает презентацию<br/>2. Получает улучшенную версию"| A2

    %% Связи Frontend-Backend
    A2 -->|"r23: HTTP запрос с файлом/данными"| A3
    A3 -->|"r32: JSON ответ с результатом/статусом"| A2
    
    %% Парсинг файла
    A3 -->|"r34: Запуск парсинга файла"| A4
    A4 -->|"r43: Структурированные данные слайдов"| A3
    A3 -->|"r39: Асинхронная задача"| A9
    A9 -->|"r94: Фоновый парсинг"| A4
    
    %% AI-оптимизация
    A3 -->|"r35: Текст для оптимизации через LLM"| A5
    A5 -->|"r53: Оптимизированный контент"| A3
    A9 -->|"r95: Фоновая оптимизация"| A5
    
    %% Дизайн-движок
    A3 -->|"r36: Данные + шаблон"| A6
    A6 -->|"r63: Слайды с примененным дизайном"| A3
    
    %% Экспорт
    A3 -->|"r38: Данные для экспорта"| A8
    A8 -->|"r83: Ссылка на готовый файл"| A3
    A9 -->|"r98: Фоновая генерация файла"| A8
    
    %% Связи с базой данных
    A3 -->|"r37: Запись логов и метаданных"| A7
    A4 -->|"r47: Сохранение распарсенных данных"| A7
    A5 -->|"r57: Кэширование промптов и ответов"| A7
    A6 -->|"r67: Шаблоны дизайна"| A7
    A8 -->|"r87: История экспортов"| A7
    A9 -->|"r97: Статусы задач"| A7

    %% Внутренние связи между модулями
    A4 -->|"r45: Структура слайдов"| A5
    A5 -->|"r56: Оптимизированный контент"| A6
    A6 -->|"r68: Готовые к экспорту слайды"| A8

    %% Стили для визуального разделения
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef processing fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef storage fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef user fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef export fill:#e0f7fa,stroke:#006064,stroke-width:2px
    classDef queue fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class A1 user
    class A2 frontend
    class A3 backend
    class A4,A5,A6 processing
    class A7 storage
    class A8 export
    class A9 queue
