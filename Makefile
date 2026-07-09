# TeamFit — Makefile
# Usage : make <commande>

.PHONY: dev stop logs shell migrate makemigrations createsuperuser test remind remind-dry-run

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

remind:
	docker compose -f docker-compose.dev.yml exec app python manage.py send_reminders

remind-dry-run:
	docker compose -f docker-compose.dev.yml exec app python manage.py send_reminders --dry-run

test:
	docker compose -f docker-compose.dev.yml exec app python manage.py test

test-fast:
	python manage.py test --settings=core.settings_test

# ── Production (VPS — voir docs/technical/deploy.md) ─────────────────────────
# Le profil demo active le service demo-reset (nécessite DEMO_MODE=True dans .env)

COMPOSE_PROD = docker compose --env-file .env -f docker/docker-compose.prod.yml --profile demo

prod:
	$(COMPOSE_PROD) up -d

prod-build:
	$(COMPOSE_PROD) up -d --build

prod-stop:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f app

# Mise à jour complète : récupère main, rebuild, relance (migrations + collectstatic
# sont exécutées automatiquement au démarrage du conteneur app)
deploy:
	git pull origin main
	$(COMPOSE_PROD) up -d --build
	docker image prune -f

prod-createsuperuser:
	$(COMPOSE_PROD) exec app python manage.py createsuperuser

prod-remind-dry-run:
	$(COMPOSE_PROD) exec app python manage.py send_reminders --dry-run

backup:
	bash deploy/backup.sh
