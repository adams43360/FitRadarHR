#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# FitRadarHR — installation initiale d'un VPS Ubuntu 24.04 (à lancer UNE fois, en root)
#
#   ssh root@<ip-du-vps>
#   git clone https://github.com/adams43360/FitRadarHR.git /srv/fitradarhr
#   bash /srv/fitradarhr/deploy/setup-server.sh
#
# Ce script :
#   1. met à jour le système + active les mises à jour de sécurité automatiques
#   2. crée l'utilisateur « damien » (sudo, clé SSH copiée depuis root)
#   3. durcit SSH (pas de mot de passe, root par clé uniquement)
#   4. configure le pare-feu UFW (SSH/HTTP/HTTPS) et fail2ban
#   5. installe Docker + le plugin compose
#   6. crée le réseau docker « web » et l'arborescence multi-sites /srv
#   7. installe et démarre le reverse proxy central Caddy (/srv/proxy)
#
# Idempotent : peut être relancé sans casser l'existant.
# ══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

DEPLOY_USER="damien"
REPO_DIR="/srv/fitradarhr"

echo "── 1/7 Mises à jour système ──────────────────────────────────────────────"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get upgrade -y -q
apt-get install -y -q ca-certificates curl git ufw fail2ban unattended-upgrades

# Mises à jour de sécurité automatiques (redémarrage non forcé)
dpkg-reconfigure -f noninteractive unattended-upgrades
systemctl enable --now unattended-upgrades

echo "── 2/7 Utilisateur ${DEPLOY_USER} ────────────────────────────────────────"
if ! id "${DEPLOY_USER}" &>/dev/null; then
    adduser --disabled-password --gecos "" "${DEPLOY_USER}"
    usermod -aG sudo "${DEPLOY_USER}"
fi
# Copie de la clé SSH de root (celle fournie à la commande du VPS)
if [ -f /root/.ssh/authorized_keys ]; then
    mkdir -p "/home/${DEPLOY_USER}/.ssh"
    cp /root/.ssh/authorized_keys "/home/${DEPLOY_USER}/.ssh/authorized_keys"
    chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh"
    chmod 700 "/home/${DEPLOY_USER}/.ssh"
    chmod 600 "/home/${DEPLOY_USER}/.ssh/authorized_keys"
fi

echo "── 3/7 Durcissement SSH ──────────────────────────────────────────────────"
SSHD_HARDEN=/etc/ssh/sshd_config.d/90-hardening.conf
cat > "${SSHD_HARDEN}" <<'EOF'
PasswordAuthentication no
PermitRootLogin prohibit-password
MaxAuthTries 4
EOF
systemctl reload ssh || systemctl reload sshd

echo "── 4/7 Pare-feu + fail2ban ───────────────────────────────────────────────"
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
systemctl enable --now fail2ban

echo "── 5/7 Docker ────────────────────────────────────────────────────────────"
if ! command -v docker &>/dev/null; then
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list
    apt-get update -q
    apt-get install -y -q docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi
usermod -aG docker "${DEPLOY_USER}"
systemctl enable --now docker

echo "── 6/7 Arborescence multi-sites + réseau « web » ─────────────────────────"
docker network inspect web &>/dev/null || docker network create web
mkdir -p /srv/proxy /srv/backups
chown -R "${DEPLOY_USER}:${DEPLOY_USER}" /srv

echo "── 7/7 Reverse proxy central (Caddy) ─────────────────────────────────────"
if [ ! -f /srv/proxy/Caddyfile ]; then
    cp "${REPO_DIR}/deploy/proxy/docker-compose.yml" /srv/proxy/
    cp "${REPO_DIR}/deploy/proxy/Caddyfile" /srv/proxy/
    chown -R "${DEPLOY_USER}:${DEPLOY_USER}" /srv/proxy
fi
(cd /srv/proxy && docker compose up -d)

echo ""
echo "══════════════════════════════════════════════════════════════════════════"
echo "✓ Serveur prêt. Étapes suivantes (voir docs/technical/deploy.md) :"
echo "  1. cd ${REPO_DIR} && cp .env.prod.example .env && nano .env"
echo "  2. make prod-build   (ou --profile demo, voir le runbook)"
echo "  3. bash deploy/install-crons.sh   (relances J+3 + backups quotidiens)"
echo "  Reconnecte-toi désormais avec : ssh ${DEPLOY_USER}@<ip>"
echo "══════════════════════════════════════════════════════════════════════════"
