.PHONY: help install install-dev lint format test run dev clean frontend-install frontend-dev frontend-build

help:
	@echo "Available commands:"
	@echo "  make install          - Install backend dependencies"
	@echo "  make install-dev      - Install backend + dev dependencies"
	@echo "  make frontend-install - Install frontend dependencies"
	@echo "  make lint             - Run linters (ruff)"
	@echo "  make format           - Format code (black, ruff)"
	@echo "  make test             - Run tests"
	@echo "  make run              - Run backend server"
	@echo "  make dev              - Run backend in development mode"
	@echo "  make frontend-dev     - Run frontend dev server"
	@echo "  make frontend-build   - Build frontend for production"
	@echo "  make clean            - Clean cache and temp files"

install:
	pip install -r requirements.txt

install-dev: install
	pip install pytest pytest-asyncio pytest-cov httpx ruff black mypy

frontend-install:
	cd frontend && npm install

lint:
	ruff check backend/
	mypy backend/ --ignore-missing-imports

format:
	black backend/
	ruff check --fix backend/

test:
	pytest -v --cov=backend tests/

run:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf dist/ build/ *.egg-info
