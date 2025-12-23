Архитектура проекта

project/
├─ backend/
│   ├─ main.py
│   ├─ req.txt
│   └─ Dockerfile.dev
├─ db/
│   └─ init/
├─ frontend/
│   ├─ .next/
│   ├─ app/
│   ├─ node_modules/
│   ├─ .dockerignore
│   ├─ Dockerfile.dev
│   ├─ next.config.js
│   └─ package.json
├─ llm-service/
│   └─ Dockerfile.dev
├─ monitoring/
│   ├─ docker-compose.yml
│   ├─ loki-config.yaml
│   ├─ prometheus.yml
│   ├─ promtail-config.yaml
│   └─ grafana/
│       └─ datasources.yaml
├─ .github/
│   └─ workflows/
│       └─ ci-cd.yml
├─ docker-compose.dev.yml
└─ README.md


Запуск проекта локально

Перезодим в папку с окружением, выполняем команду: docker compose -f docker-compose.dev.yml up -d

