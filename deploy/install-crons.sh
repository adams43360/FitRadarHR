#!/usr/bin/env bash
# Installe les tâches planifiées FitRadarHR dans /etc/cron.d/ (à lancer en root ou sudo).
#   - 8h00 : relances questionnaire J+3 (manage.py send_reminders) — une seule
#            relance par lien, garde-fou démo intégré à la commande
#   - 3h30 : backup PostgreSQL (deploy/backup.sh, rotation 14 jours)
set -euo pipefail

REPO_DIR="/srv/fitradarhr"
CRON_FILE="/etc/cron.d/fitradarhr"

cat > "${CRON_FILE}" <<EOF
# FitRadarHR — géré par deploy/install-crons.sh (ne pas éditer à la main sur le serveur,
# modifier le script dans le dépôt puis le relancer)
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Relances questionnaire J+3, tous les jours à 8h
0 8 * * * root cd ${REPO_DIR} && docker compose -f docker/docker-compose.prod.yml exec -T app python manage.py send_reminders >> /var/log/fitradarhr-reminders.log 2>&1

# Backup PostgreSQL quotidien à 3h30 (rotation 14 jours)
30 3 * * * root ${REPO_DIR}/deploy/backup.sh >> /var/log/fitradarhr-backup.log 2>&1
EOF

chmod 644 "${CRON_FILE}"
echo "✓ Crons installés dans ${CRON_FILE} :"
grep -v "^#\|^SHELL\|^PATH\|^$" "${CRON_FILE}"
