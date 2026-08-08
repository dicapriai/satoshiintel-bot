#!/usr/bin/env bash
# Instala el bot gratis SatoshiIntel en el VPS, con su PostgreSQL propio.
# Se ejecuta UNA vez, como root. Idempotente: repetirlo no rompe nada.
set -euo pipefail

APP=/opt/satoshiintel/app
DATA=/opt/satoshiintel/data
VENV=/opt/satoshiintel/venv
DB_NAME=satoshiintel
DB_USER=satoshiintel

echo "==> Dependencias del sistema"
apt-get update -qq
apt-get install -y -qq python3-venv python3-pip rsync postgresql postgresql-client

echo "==> PostgreSQL"
systemctl enable --now postgresql
# La contraseña se genera aquí y solo vive en el .env: nunca pasa por el chat
# ni queda en el historial. La base solo escucha en localhost.
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
  DB_PASS=$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 24)
  sudo -u postgres psql -q -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
  sudo -u postgres psql -q -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
  echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASS@127.0.0.1:5432/$DB_NAME" > /root/satoshiintel-db.env
  chmod 600 /root/satoshiintel-db.env
  echo "    base creada; su URL quedó en /root/satoshiintel-db.env"
else
  echo "    el usuario de base de datos ya existía, se respeta"
fi

echo "==> Usuario de servicio (sin login, no root)"
id -u satoshiintel >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin -d /opt/satoshiintel satoshiintel

echo "==> Carpetas"
mkdir -p "$APP" "$DATA"

echo "==> Entorno virtual e instalación de librerías"
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$APP/requirements.txt"

echo "==> Comprobando secretos"
if [ ! -f "$APP/.env" ]; then
  echo "ERROR: falta $APP/.env — cópialo antes de seguir." >&2
  exit 1
fi
# Añade la DATABASE_URL local si el .env no trae una.
if ! grep -q '^DATABASE_URL=' "$APP/.env" && [ -f /root/satoshiintel-db.env ]; then
  cat /root/satoshiintel-db.env >> "$APP/.env"
  echo "    DATABASE_URL local añadida al .env"
fi
chmod 600 "$APP/.env"

echo "==> Permisos"
chown -R satoshiintel:satoshiintel /opt/satoshiintel

echo "==> Servicio systemd"
cp "$APP/satoshiintel.service" /etc/systemd/system/satoshiintel.service
systemctl daemon-reload
systemctl enable --now satoshiintel

sleep 4
systemctl status satoshiintel --no-pager --lines=20 || true
