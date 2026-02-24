# =============================================================================
# B3_Portfolio - Makefile
# =============================================================================
# Automation for common development tasks
#
# Usage:
#   make help           Show this help message
#   make install        Install all dependencies
#   make test           Run all tests
#   make lint           Check code quality
#   make format         Format code
#   make clean          Clean temporary files
#
# Backend specific:
#   make backend-test   Run backend tests
#   make backend-lint   Lint backend code
#
# Frontend specific:
#   make frontend-test  Run frontend tests
#   make frontend-lint  Lint frontend code
#
# Docker:
#   make docker-up      Start all services
#   make docker-down    Stop all services
# =============================================================================

.PHONY: help
help: ## Show this help message
	@echo "B3_Portfolio - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Setup & Installation
# =============================================================================

.PHONY: install
install: install-backend install-frontend ## Install all dependencies

.PHONY: install-backend
install-backend: ## Install Python dependencies
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Backend dependencies installed"

.PHONY: install-frontend
install-frontend: ## Install Node.js dependencies
	@echo "📦 Installing Node.js dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

.PHONY: setup
setup: install docker-up migrate ## Complete setup (install + docker + migrate)
	@echo "🎉 Setup complete!"

# =============================================================================
# Testing
# =============================================================================

.PHONY: test
test: backend-test frontend-test ## Run all tests

.PHONY: backend-test
backend-test: ## Run Python tests with coverage
	@echo "🧪 Running backend tests..."
	pytest --cov=app --cov-report=html --cov-report=term-missing -v
	@echo "✅ Backend tests complete"

.PHONY: frontend-test
frontend-test: ## Run TypeScript tests
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test
	@echo "✅ Frontend tests complete"

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	pytest --watch

.PHONY: coverage
coverage: ## Generate and open coverage report
	pytest --cov=app --cov-report=html
	open htmlcov/index.html

# =============================================================================
# Code Quality
# =============================================================================

.PHONY: lint
lint: backend-lint frontend-lint ## Check code quality (all)

.PHONY: backend-lint
backend-lint: ## Lint Python code
	@echo "🔍 Linting backend code..."
	black --check .
	isort --check-only .
	ruff check .
	mypy .
	@echo "✅ Backend lint complete"

.PHONY: frontend-lint
frontend-lint: ## Lint TypeScript code
	@echo "🔍 Linting frontend code..."
	cd frontend && npm run lint
	@echo "✅ Frontend lint complete"

.PHONY: format
format: backend-format frontend-format ## Format code (all)

.PHONY: backend-format
backend-format: ## Format Python code
	@echo "🎨 Formatting backend code..."
	black .
	isort .
	ruff check --fix .
	@echo "✅ Backend format complete"

.PHONY: frontend-format
frontend-format: ## Format TypeScript code
	@echo "🎨 Formatting frontend code..."
	cd frontend && npm run lint:fix && npm run format
	@echo "✅ Frontend format complete"

.PHONY: security
security: ## Run security checks
	@echo "🔒 Running security checks..."
	bandit -r . -c pyproject.toml
	safety check
	pip-audit
	@echo "✅ Security checks complete"

# =============================================================================
# Docker
# =============================================================================

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo "✅ Docker containers started"

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "🐳 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Docker containers stopped"

.PHONY: docker-restart
docker-restart: docker-down docker-up ## Restart Docker containers

.PHONY: docker-logs
docker-logs: ## View Docker logs
	docker-compose logs -f

.PHONY: docker-ps
docker-ps: ## List running containers
	docker-compose ps

.PHONY: docker-clean
docker-clean: docker-down ## Clean Docker resources
	@echo "🧹 Cleaning Docker resources..."
	docker-compose down -v --remove-orphans
	@echo "✅ Docker cleaned"

# =============================================================================
# Database
# =============================================================================

.PHONY: migrate
migrate: ## Run database migrations
	@echo "🗄️  Running migrations..."
	cd services/portfolio && alembic upgrade head
	@echo "✅ Migrations complete"

.PHONY: migrate-create
migrate-create: ## Create new migration (usage: make migrate-create MSG="description")
	@echo "🗄️  Creating migration..."
	cd services/portfolio && alembic revision --autogenerate -m "$(MSG)"
	@echo "✅ Migration created"

.PHONY: db-reset
db-reset: ## Reset database (⚠️  destructive!)
	@echo "⚠️  Resetting database..."
	docker-compose down -v
	docker-compose up -d postgres redis
	sleep 3
	$(MAKE) migrate
	@echo "✅ Database reset"

# =============================================================================
# Development
# =============================================================================

.PHONY: dev
dev: ## Start development servers (all)
	@echo "🚀 Starting development servers..."
	@echo "Run in separate terminals:"
	@echo "  Terminal 1: make backend-dev"
	@echo "  Terminal 2: make frontend-dev"

.PHONY: backend-dev
backend-dev: ## Start backend development server
	@echo "🚀 Starting backend server..."
	cd services/api-gateway && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: frontend-dev
frontend-dev: ## Start frontend development server
	@echo "🚀 Starting frontend server..."
	cd frontend && npm run dev

# =============================================================================
# Build
# =============================================================================

.PHONY: build
build: build-backend build-frontend ## Build all services

.PHONY: build-backend
build-backend: ## Build backend Docker images
	@echo "🏗️  Building backend..."
	docker-compose build
	@echo "✅ Backend built"

.PHONY: build-frontend
build-frontend: ## Build frontend for production
	@echo "🏗️  Building frontend..."
	cd frontend && npm run build
	@echo "✅ Frontend built"

# =============================================================================
# Cleaning
# =============================================================================

.PHONY: clean
clean: clean-python clean-frontend ## Clean all temporary files

.PHONY: clean-python
clean-python: ## Clean Python temporary files
	@echo "🧹 Cleaning Python files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage build/ dist/
	@echo "✅ Python cleaned"

.PHONY: clean-frontend
clean-frontend: ## Clean Node.js temporary files
	@echo "🧹 Cleaning Node.js files..."
	cd frontend && rm -rf node_modules dist build coverage
	@echo "✅ Frontend cleaned"

.PHONY: clean-all
clean-all: clean docker-clean ## Clean everything including Docker

# =============================================================================
# Documentation
# =============================================================================

.PHONY: docs
docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	cd docs && make html
	@echo "✅ Documentation generated"

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	cd docs && python -m http.server 8080

# =============================================================================
# Utilities
# =============================================================================

.PHONY: shell
shell: ## Open Python shell with project context
	ipython

.PHONY: db-shell
db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U postgres -d portfolio_db

.PHONY: redis-shell
redis-shell: ## Open Redis CLI
	docker-compose exec redis redis-cli

.PHONY: logs
logs: ## View application logs
	tail -f logs/*.log

.PHONY: update
update: ## Update dependencies
	@echo "📦 Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	cd frontend && npm update
	@echo "✅ Dependencies updated"

.PHONY: audit
audit: ## Run security audit
	@echo "🔍 Running security audit..."
	pip-audit
	cd frontend && npm audit
	@echo "✅ Audit complete"

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

.PHONY: version
version: ## Show versions
	@echo "🔢 Versions:"
	@echo "  Python:     $$(python --version)"
	@echo "  Node:       $$(node --version)"
	@echo "  npm:        $$(npm --version)"
	@echo "  Docker:     $$(docker --version)"
	@echo "  Docker Compose: $$(docker-compose --version)"

# =============================================================================
# CI/CD
# =============================================================================

.PHONY: ci
ci: lint test security ## Run CI pipeline locally
	@echo "✅ CI pipeline complete"

# =============================================================================
# Default target
# =============================================================================

.DEFAULT_GOAL := help
