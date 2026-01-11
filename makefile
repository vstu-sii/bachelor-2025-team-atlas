.PHONY: help up down build logs clean db migrate test lint format init

help:
	@echo "AutoPitch Deck Generator - Development Commands"
	@echo ""
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make build     - Rebuild all Docker images"
	@echo "  make logs      - View service logs"
	@echo "  make clean     - Clean all data and containers"
	@echo "  make db        - Connect to PostgreSQL database"
	@echo "  make migrate   - Run database migrations"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run code linting"
	@echo "  make format    - Format code"
	@echo "  make init      - Initialize project"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build --no-cache

logs:
	docker-compose logs -f --tail=100

clean:
	docker-compose down -v
	docker system prune -f
	rm -rf backend/__pycache__ backend/app/__pycache__
	rm -rf frontend/.next frontend/node_modules

db:
	docker exec -it autopitch_postgres psql -U autopitch_user -d autopitch

migrate:
	docker exec autopitch_backend python -m alembic upgrade head

test:
	docker exec autopitch_backend pytest tests/ -v
	docker exec autopitch_frontend npm test

lint:
	docker exec autopitch_backend black --check app/
	docker exec autopitch_backend isort --check-only app/
	docker exec autopitch_frontend npm run lint

format:
	docker exec autopitch_backend black app/
	docker exec autopitch_backend isort app/
	docker exec autopitch_frontend npm run format

init:
	@echo "Initializing AutoPitch project..."
	cp backend/.env.example backend/.env
	cp frontend/.env.example frontend/.env.local
	@echo "Please edit the .env files with your configuration"
	@echo ""
	@echo "To start the project:"
	@echo "  1. Edit backend/.env and frontend/.env.local"
	@echo "  2. Run: make up"
	@echo "  3. Open http://localhost:3000"

# Development shortcuts
dev-backend:
	docker-compose up -d postgres redis
	cd backend && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev

# Database backup
backup:
	docker exec autopitch_postgres pg_dump -U autopitch_user autopitch > backup_$(date +%Y%m%d_%H%M%S).sql

# Database restore
restore:
	@read -p "Enter backup file: " file; \
	docker exec -i autopitch_postgres psql -U autopitch_user autopitch < $$file
