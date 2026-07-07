# Déploiement production — fitradarhr.fr

> Runbook du déploiement sur le VPS Scaleway Dedibox (VPS-START-2-M, Ubuntu 24.04, Paris).
> Architecture multi-sites : un proxy Caddy central route les domaines vers chaque projet.

## Vue d'ensemble

```
Internet ──443──▶ Caddy (/srv/proxy, TLS Let's Encrypt auto)
                    │ réseau docker « web »
                    ├─▶ fitradarhr-web (nginx interne : statiques + proxy)──▶ gunicorn ──▶ PostgreSQL
                    └─▶ <futur-projet>-web ...
```

Un seul composant expose 80/443 : Caddy. Chaque projet est une stack Docker Compose
autonome sans port publié, jointe au réseau `web`. Ajouter un site = un bloc dans
`/srv/proxy/Caddyfile` + un `docker compose up` dans `/srv/<projet>`.

## 1. DNS (console Scaleway, une fois)

Dans la zone DNS de `fitradarhr.fr`, créer :

| Type | Nom | Valeur |
|---|---|---|
| A | `fitradarhr.fr` (racine / @) | IP du VPS |
| A | `www` | IP du VPS |

Propagation en général < 1 h. Vérifier : `dig +short fitradarhr.fr`.

## 2. Installation du serveur (une fois)

```bash
ssh root@<ip-du-vps>
git clone https://github.com/adams43360/FitRadarHR.git /srv/fitradarhr
bash /srv/fitradarhr/deploy/setup-server.sh
```

Le script (idempotent) : mises à jour + unattended-upgrades, utilisateur `damien`
(sudo, clé SSH copiée), durcissement SSH (mot de passe désactivé), UFW (22/80/443),
fail2ban, Docker + compose, réseau `web`, arborescence `/srv`, proxy Caddy démarré.

**Ensuite, se reconnecter en `ssh damien@<ip>`** (root reste accessible par clé en secours).

## 3. Configuration (une fois)

```bash
cd /srv/fitradarhr
cp .env.prod.example .env
nano .env
```

À remplir (voir les commentaires du fichier) :

- `DJANGO_SECRET_KEY` et `DB_PASSWORD` — générer avec les commandes indiquées en commentaire
- SMTP **Brevo** : créer le compte sur brevo.com → Paramètres → SMTP & API → clé SMTP.
  Authentifier le domaine `fitradarhr.fr` chez Brevo (2 enregistrements DNS à copier
  dans la zone Scaleway) pour une bonne délivrabilité
- Stripe : laisser vide au lancement — l'écran abonnement affichera « configuration
  requise », le reste de l'app fonctionne normalement. À configurer plus tard
  (produit + Price **39 €/mois** + webhook `https://fitradarhr.fr/billing/webhook/`)

## 4. Premier déploiement

```bash
cd /srv/fitradarhr
make prod-build        # build + démarrage (migrations et collectstatic automatiques)
make prod-logs         # vérifier le démarrage (Ctrl+C pour quitter)
sudo bash deploy/install-crons.sh   # relances J+3 (8h) + backups quotidiens (3h30)
make prod-createsuperuser           # compte d'administration Django
```

Le profil `demo` est inclus dans les cibles make : l'org de démonstration « Nexatech »
est seedée au premier démarrage puis resetée toutes les 24 h (`DEMO_MODE=True` requis
dans `.env`).

Vérifications :

- `https://fitradarhr.fr` répond en HTTPS (certificat émis automatiquement — si erreur
  TLS dans les premières minutes, laisser Caddy finir l'émission puis recharger)
- `https://www.fitradarhr.fr` redirige vers la racine
- Bouton « Essayer la démo » fonctionnel
- Inscription B2B : email de confirmation reçu (sinon vérifier la config SMTP —
  `make prod-logs`)
- `make prod-remind-dry-run` liste les relances sans les envoyer

## 5. Mises à jour applicatives

En local : développer, commiter, pousser sur `main`. Puis sur le serveur :

```bash
ssh damien@<ip>
cd /srv/fitradarhr && make deploy
```

`make deploy` = `git pull` + rebuild + relance ; les migrations et `collectstatic`
s'exécutent au démarrage du conteneur. Interruption de service : quelques secondes.

## 6. Sauvegardes

- Quotidiennes à 3h30 (`/srv/backups/fitradarhr_YYYY-MM-DD.sql.gz`, rotation 14 jours),
  manuel : `make backup`
- Restauration : voir le commentaire en tête de `deploy/backup.sh`
- Les fichiers média (volume `media_data`) ne contiennent que peu de choses en V1 ;
  la base contient l'essentiel
- **Hors serveur** : penser à rapatrier ponctuellement un dump en local
  (`scp damien@<ip>:/srv/backups/<dernier>.sql.gz ~/Backups/`) — un backup sur la
  même machine ne protège pas d'une perte du VPS

## 7. Ajouter un autre site sur le même VPS

1. `/srv/<projet>` : stack compose sans port publié, service web avec
   `container_name: <projet>-web` et `networks: [default, web]` (réseau `web` external)
2. Bloc dans `/srv/proxy/Caddyfile` : `domaine.fr { reverse_proxy <projet>-web:80 }`
3. `cd /srv/proxy && docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile`
4. DNS : enregistrement A du nouveau domaine → même IP

## Dépannage rapide

| Symptôme | Piste |
|---|---|
| 502 Bad Gateway | conteneur app arrêté ou en cours de démarrage — `make prod-logs` |
| Boucle de redirections | `X-Forwarded-Proto` non transmis — vérifier `docker/nginx.prod.conf` |
| Emails non reçus | credentials Brevo dans `.env`, puis `make prod-logs` lors d'une inscription |
| CSRF « origin checking failed » | `ALLOWED_HOSTS` incomplet dans `.env` (les origines CSRF en dérivent) |
| Certificat non émis | DNS pas encore propagé vers l'IP, ou port 80 bloqué — `docker compose logs caddy` dans `/srv/proxy` |
