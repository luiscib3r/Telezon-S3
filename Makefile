.PHONY: format
format:
	poetry run ruff format app/

.PHONY: dev
dev:
	docker compose -f docker-compose.dev.yaml up -d
	poetry run fastapi dev app/main.py

.PHONY: run
run:
	docker compose -f docker-compose.dev.yaml up -d
	poetry run fastapi run app/main.py

.PHONY: setup_bot_storage
setup_bot_storage:
	poetry run python setup_bot_storage.py
