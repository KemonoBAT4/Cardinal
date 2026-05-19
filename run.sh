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
COMMAND="$2"
DB_SERVICE="db_${APP_NAME}"

if [ $# -lt 2 ]; then
  echo "Uso: ./run.sh <app> <command>"
  exit 1
fi

if [ "$COMMAND" == "reset" ]; then
  echo "🧨 Full DB reset (Docker volume)"

  docker compose down -v

  docker compose up -d "$APP_NAME" "$DB_SERVICE"

  exit 0
fi

if [ "$COMMAND" == "build" ]; then
  echo "🔨 Building image for $APP_NAME..."

  docker compose build "$APP_NAME"

  echo "✅ Build completata: cardinal-$APP_NAME"

  docker save cardinal-$APP_NAME > cardinal-$APP_NAME.tar

  exit 0
fi

echo "▶ Avvio container: $APP_NAME + $DB_SERVICE"
docker compose -f "$SCRIPT_DIR/docker-compose.yml" up -d "$APP_NAME" "$DB_SERVICE"
docker compose -f "$SCRIPT_DIR/docker-compose.yml" exec "$APP_NAME" \
  python run.py "$APP_NAME" "$COMMAND"
