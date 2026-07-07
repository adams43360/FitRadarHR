#!/usr/bin/env bash
# Backup quotidien PostgreSQL — pg_dump compressé dans /srv/backups, rotation 14 jours.
# Installé en cron par deploy/install-crons.sh (3h30 du matin).
# Restauration :
#   gunzip -c /srv/backups/fitradarhr_YYYY-MM-DD.sql.gz | \
#     docker compose -f docker/docker-compose.prod.yml exec -T db psql -U $DB_USER $DB_NAME
set -euo pipefail

REPO_DIR="/srv/fitradarhr"
BACKUP_DIR="/srv/backups"
RETENTION_DAYS=14

# Récupère DB_USER / DB_NAME depuis le .env du projet
set -a
source "${REPO_DIR}/.env"
set +a

STAMP=$(date +%F)
OUT="${BACKUP_DIR}/fitradarhr_${STAMP}.sql.gz"

docker compose -f "${REPO_DIR}/docker/docker-compose.prod.yml" exec -T db \
    pg_dump -U "${DB_USER:-teamfit}" "${DB_NAME:-teamfit}" | gzip > "${OUT}"

# Rotation
find "${BACKUP_DIR}" -name "fitradarhr_*.sql.gz" -mtime +${RETENTION_DAYS} -delete

echo "$(date -Is) backup ok : ${OUT} ($(du -h "${OUT}" | cut -f1))"
