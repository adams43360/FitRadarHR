# TeamFit — Makefile
# Usage : make <commande>

.PHONY: dev stop logs shell migrate makemigrations createsuperuser test

# ── Développement ────────────────────────────────────────────────────────────

dev:
	docker compose -f docker-compose.dev.yml up

dev-build:
	docker compose -f docker-compose.dev.yml up --build

stop:
	docker compose -f docker-compose.dev.yml down

logs:
	docker compose -f docker-compose.dev.yml logs -f app

# ── Django ───────────────────────────────────────────────────────────────────

shell:
	docker compose -f docker-compose.dev.yml exec app python manage.py shell

migrate:
	docker compose -f docker-compose.dev.yml exec app python manage.py migrate

makemigrations:
	docker compose -f docker-compose.dev.yml exec app python manage.py makemigrations

createsuperuser:
	docker compose -f docker-compose.dev.yml exec app python manage.py createsuperuser

seed-demo:
	docker compose -f docker-compose.dev.yml exec app python manage.py seed_demo --force

test:
	docker compose -f docker-compose.dev.yml exec app python manage.py test

test-fast:
	python manage.py test --settings=core.settings_test

# ── Production ───────────────────────────────────────────────────────────────

prod:
	docker compose -f docker/docker-compose.yml up -d

prod-build:
	docker compose -f docker/docker-compose.yml up -d --build

prod-stop:
	docker compose -f docker/docker-compose.yml down
