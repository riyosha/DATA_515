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
	# @echo "coverage-frontend  - Run frontend tests with coverage"
	# @echo "coverage-backend   - Run backend tests with coverage"
	# @echo "coverage-backend-report - Generate backend coverage report"
	# @echo "coverage           - Run all tests with coverage"
	@echo "lint-frontend      - Run frontend linting"
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

# coverage-frontend:
# 	docker-compose exec frontend npm test -- --coverage

shell-frontend:
	docker-compose exec frontend /bin/sh

# Backend commands
test-backend:
	docker-compose exec backend conda run -n letterboxd python -m unittest discover -s tests

# coverage-backend:
# 	docker-compose exec backend conda run -n letterboxd coverage run --source=src -m unittest discover -s tests
# 	@echo "Run 'make coverage-backend-report' to see the coverage report"

# coverage-backend-report:
# 	docker-compose exec backend conda run -n letterboxd coverage report
# 	docker-compose exec backend conda run -n letterboxd coverage html

lint-backend:
	docker-compose exec backend flake8

shell-backend:
	docker-compose exec backend /bin/bash

# Combined commands
test: test-backend test-frontend

# coverage: coverage-frontend coverage-backend

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