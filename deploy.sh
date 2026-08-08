#!/usr/bin/env bash
# Sube el código al VPS y reinicia el bot gratis. Se ejecuta DESDE EL MAC.
# Uso: ./deploy.sh
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

echo "==> Reiniciando servicio"
ssh "$VPS" 'systemctl restart satoshiintel && sleep 4 && systemctl is-active satoshiintel && journalctl -u satoshiintel -n 15 --no-pager'
