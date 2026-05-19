# NOTE: when using this script, it can execute any application in the "app" folder
# the name of the wanted application must be passed as the first argument
# NOTE: if the application wants to be started as setup (so by executing the "setup" function in the designated application)
# then the second argument must be "setup"
# NOTE: any other argument will be passed or converted based on what it is or what the application needs to run

#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALID_APPS=($(ls -d "$SCRIPT_DIR/app"/*/  2>/dev/null | xargs -n1 basename))

if [ ${#VALID_APPS[@]} -eq 0 ]; then
  echo "Nessuna app trovata in $SCRIPT_DIR/app/"
  exit 1
fi

if [ $# -lt 2 ]; then
  echo "Uso: ./run.sh <app> <comando>"
  echo "App disponibili: ${VALID_APPS[*]}"
  exit 1
fi

if [[ ! " ${VALID_APPS[@]} " =~ " $1 " ]]; then
  echo "App non valida: $1"
  echo "App disponibili: ${VALID_APPS[*]}"
  exit 1
fi

APP_NAME="$1"
DB_SERVICE="db_${APP_NAME}"

if command -v docker &>/dev/null && [ -f "$SCRIPT_DIR/docker-compose.yml" ]; then
  echo "▶ Avvio container: $APP_NAME + $DB_SERVICE"
  docker compose -f "$SCRIPT_DIR/docker-compose.yml" up "$APP_NAME" "$DB_SERVICE" -d
  if [ $? -ne 0 ]; then
    echo "⚠ docker compose non riuscito, continuo con avvio locale..."
  fi
fi

python run.py "$@"
