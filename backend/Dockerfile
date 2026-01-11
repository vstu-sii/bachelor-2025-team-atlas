FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для парсинга файлов
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    poppler-utils \
    libreoffice-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание необходимых директорий
RUN mkdir -p uploads templates exports logs

# Создание non-root пользователя
RUN useradd -m -u 1000 autopitch && chown -R autopitch:autopitch /app
USER autopitch

EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
