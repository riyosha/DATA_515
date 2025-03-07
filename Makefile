.PHONY: up down build rebuild logs ps help test-frontend test-backend lint-frontend lint-backend shell-frontend shell-backend test lint clean dev init

# Help command
help:
	@echo "Docker Compose Makefile Commands:"
	@echo "=================================="
	@echo "up                 - Start all containers in detached mode"
	@echo "down               - Stop and remove all containers"
	@echo "build              - Build all containers"
	@echo "rebuild            - Force rebuild all containers"
	@echo "logs               - View logs from all containers"
	@echo "ps                 - List running containers"
	@echo "test-frontend      - Run frontend tests"
	@echo "test-backend       - Run backend tests"
	@echo "test               - Run all tests (frontend and backend)"	
	@echo "coverage-frontend  - Run frontend tests with coverage"
	@echo "coverage-backend   - Run backend tests with coverage"
	@echo "coverage           - Run all tests with coverage"
	@echo "lint-frontend      - Run frontend linting"
	@echo "lint-fix-frontend  - Run frontend linting and fix issues"
	@echo "lint-backend       - Run backend linting"
	@echo "lint               - Run all linting (frontend and backend)"
	@echo "shell-frontend     - Get a shell in the frontend container"
	@echo "shell-backend      - Get a shell in the backend container"
	@echo "clean              - Remove all containers, volumes, and images"
	@echo "dev                - Start development mode with hot reloading"
	@echo "init               - Initialize project (first-time setup)"

# Docker Compose commands
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache

logs:
	docker-compose logs -f

ps:
	docker-compose ps

# Frontend commands
test-frontend:
	docker-compose exec frontend npm test

lint-frontend:
	docker-compose exec frontend npm run lint

lint-fix-frontend:
	docker-compose exec frontend npm run lint:fix

coverage-frontend:
	docker-compose exec frontend npm test -- --coverage
	@echo "Frontend coverage report available in frontend/coverage/lcov-report/index.html"

shell-frontend:
	docker-compose exec frontend /bin/sh

# Backend commands
test-backend:
	docker-compose exec backend conda run -n letterboxd python -m unittest discover -s tests

coverage-backend:
	docker-compose exec backend conda run -n letterboxd coverage run -m unittest discover -s tests
	docker-compose exec backend conda run -n letterboxd coverage report
	@echo "Running backend coverage report..."
	docker-compose exec backend conda run -n letterboxd coverage html
	@echo "Backend coverage report available in backend/htmlcov/index.html"

lint-backend:
	docker-compose exec backend conda run -n letterboxd pylint --output-format=colorized src/ tests/

shell-backend:
	docker-compose exec backend /bin/bash

# Combined commands
test: test-backend test-frontend

coverage: coverage-backend coverage-frontend

lint: lint-frontend lint-backend

# Development mode (with hot reloading)
dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Cleanup
clean:
	docker-compose down -v --rmi local

# First-time setup
init: build up
	@echo "Project initialized successfully!"