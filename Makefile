.PHONY: help install test lint clean up down logs build rebuild restart

help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-api: ## Installe les dépendances de l'API
	cd app_api && uv sync

install-front: ## Installe les dépendances du frontend
	cd app_front && uv sync

install: install-api install-front ## Installe toutes les dépendances

test: ## Lance les tests de l'API
	cd app_api && uv run pytest tests/ -v --cov

test-verbose: ## Lance les tests avec détails
	cd app_api && uv run pytest tests/ -vv --cov --cov-report=html

lint-api: ## Lint l'API
	cd app_api && uv run ruff check .

lint-front: ## Lint le frontend
	cd app_front && uv run ruff check .

lint: lint-api lint-front ## Lint tout le code

format-api: ## Formate le code de l'API
	cd app_api && uv run ruff format .

format-front: ## Formate le code du frontend
	cd app_front && uv run ruff format .

format: format-api format-front ## Formate tout le code

up: ## Démarre tous les services avec Docker Compose
	docker-compose up -d

down: ## Arrête tous les services
	docker-compose down

down-volumes: ## Arrête tous les services et supprime les volumes
	docker-compose down -v

logs: ## Affiche les logs en temps réel
	docker-compose logs -f

logs-api: ## Affiche les logs de l'API
	docker-compose logs -f api

logs-front: ## Affiche les logs du frontend
	docker-compose logs -f front

logs-db: ## Affiche les logs de la base de données
	docker-compose logs -f db

build: ## Build les images Docker
	docker-compose build

rebuild: ## Rebuild les images Docker sans cache
	docker-compose build --no-cache

restart: ## Redémarre tous les services
	docker-compose restart

restart-api: ## Redémarre l'API
	docker-compose restart api

restart-front: ## Redémarre le frontend
	docker-compose restart front

ps: ## Affiche l'état des services
	docker-compose ps

clean: ## Nettoie les fichiers temporaires
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "*.db" -delete
	find . -type f -name "*.sqlite" -delete

clean-docker: ## Nettoie Docker (images, conteneurs, volumes)
	docker-compose down -v
	docker system prune -af

prod-up: ## Lance en mode production (depuis DockerHub)
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Arrête le mode production
	docker-compose -f docker-compose.prod.yml down

prod-logs: ## Logs du mode production
	docker-compose -f docker-compose.prod.yml logs -f

env: ## Crée un fichier .env depuis .env.example
	cp .env.example .env
	@echo "Fichier .env créé. N'oubliez pas de le configurer!"

check: lint test ## Lance lint et tests

dev-api: ## Lance l'API en mode développement local
	cd app_api && uv run uvicorn main:app --reload --port 8000

dev-front: ## Lance le frontend en mode développement local
	cd app_front && uv run streamlit run main.py

health: ## Vérifie la santé des services
	@echo "Vérification de l'API..."
	@curl -f http://localhost:8000/health || echo "❌ API non accessible"
	@echo "\nVérification du Frontend..."
	@curl -f http://localhost:8501 || echo "❌ Frontend non accessible"
