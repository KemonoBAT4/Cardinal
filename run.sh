# NOTE: when using this script, it can execute any application in the "app" folder
# the name of the wanted application must be passed as the first argument
# NOTE: if the application wants to be started as setup (so by executing the "setup" function in the designated application)
# then the second argument must be "setup"
# NOTE: any other argument will be passed or converted based on what it is or what the application needs to run

#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  Cardinal – run.sh
#
#  Uso:
#    ./run.sh <app> run         → avvia in DEV (live reload)
#    ./run.sh <app> setup       → setup DB in DEV
#    ./run.sh <app> build       → crea immagine PROD baked
#    ./run.sh <app> deploy      → avvia in PROD (standalone)
#    ./run.sh <app> reset       → distrugge e ricrea i volumi DB
# ─────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_DEV="$SCRIPT_DIR/docker-compose.yml"
COMPOSE_PROD="$SCRIPT_DIR/docker-compose.prod.yml"

VALID_APPS=($(ls -d "$SCRIPT_DIR/app"/*/  2>/dev/null | xargs -n1 basename))

# ── Validazione args ──────────────────────────────────────────
if [ ${#VALID_APPS[@]} -eq 0 ]; then
  echo "❌ Nessuna app trovata in $SCRIPT_DIR/app/"
  exit 1
fi

if [ $# -lt 2 ]; then
  echo "Uso: ./run.sh <app> <comando>"
  echo "App disponibili: ${VALID_APPS[*]}"
  exit 1
fi

if [[ ! " ${VALID_APPS[@]} " =~ " $1 " ]]; then
  echo "❌ App non valida: $1"
  echo "App disponibili: ${VALID_APPS[*]}"
  exit 1
fi

APP_NAME="$1"
COMMAND="$2"
CONTAINER="cardinal_${APP_NAME}"
DB_SERVICE="db_${APP_NAME}"

# ── RESET: abbatte i volumi e riparte ────────────────────────
if [ "$COMMAND" == "reset" ]; then
  echo "🧨 Reset completo volumi DB per $APP_NAME..."
  docker compose -f "$COMPOSE_DEV" down -v "$APP_NAME" "$DB_SERVICE"
  docker compose -f "$COMPOSE_DEV" up -d "$APP_NAME" "$DB_SERVICE"
  echo "✅ Reset completato."
  exit 0
fi

# ── BUILD: crea immagine prod baked (niente volume) ──────────
if [ "$COMMAND" == "build" ]; then
  echo "🔨 Build immagine PROD per $APP_NAME..."
  docker build \
    --build-arg APP_NAME="$APP_NAME" \
    -t "kemonobat4/cardinal-${APP_NAME}:latest" \
    "$SCRIPT_DIR"
  echo "✅ Immagine pronta: kemonobat4/cardinal-${APP_NAME}:latest"
  echo "💾 Salvataggio tar..."
  docker save "kemonobat4/cardinal-${APP_NAME}:latest" \
    -o "$SCRIPT_DIR/cardinal-${APP_NAME}.tar"
  echo "✅ Salvata in cardinal-${APP_NAME}.tar"
  exit 0
fi

# ── DEPLOY: avvia in PROD con l'immagine baked ───────────────
if [ "$COMMAND" == "deploy" ]; then
  echo "🚀 Deploy PROD di $APP_NAME..."
  docker compose -f "$COMPOSE_PROD" up -d "$APP_NAME" "$DB_SERVICE"
  echo "✅ $APP_NAME in esecuzione (prod)."
  exit 0
fi

# ── DEV: avvia container con bind mount ed esegue il comando ─
echo "▶ Avvio DEV: $APP_NAME + $DB_SERVICE"
docker compose -f "$COMPOSE_DEV" up -d "$APP_NAME" "$DB_SERVICE"

echo "⏳ Attendo che $CONTAINER sia in running..."
until docker ps --filter "name=^${CONTAINER}$" --filter "status=running" \
      --format '{{.Names}}' | grep -q "^${CONTAINER}$"; do
  sleep 1
done

echo "▶ Eseguo: python run.py $APP_NAME $COMMAND"
docker compose -f "$COMPOSE_DEV" exec "$APP_NAME" \
  python run.py "$APP_NAME" "$COMMAND"