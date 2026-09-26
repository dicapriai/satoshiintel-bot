#!/usr/bin/env bash
# Sube el código al VPS y relevanta el bot con DOCKER. Se ejecuta DESDE EL MAC.
# Uso: VPS=root@mi-servidor ./deploy.sh
set -euo pipefail

# El servidor NO se escribe aquí (repo público). Se pasa al ejecutar:
#   VPS=root@mi-servidor ./deploy.sh
VPS=${VPS:?define VPS, ej: VPS=root@mi-servidor ./deploy.sh}

echo "==> Subiendo código a $VPS"
# --delete deja el VPS igual que el Mac, pero .env y la base de datos están
# excluidos: no se suben ni se borran allí.
rsync -az --delete \
  --exclude '.git' --exclude '.venv' --exclude '__pycache__' \
  --exclude '*.db' --exclude '.env' --exclude '.DS_Store' \
  ./ "$VPS:/opt/satoshiintel/app/"

echo "==> Reconstruyendo el contenedor"
ssh "$VPS" 'cd /opt/satoshiintel/app && docker compose up -d --build && sleep 6 && docker compose ps && echo "--- logs ---" && docker compose logs --tail 8'
