#!/bin/bash

ACTION=$1
APP_NAME=$2
APP_PORT=$3
APP_DATA="./${APP_NAME}_data"

if [ "$ACTION" = "start" ]; then
    if [ -z "$APP_NAME" ] || [ -z "$APP_PORT" ]; then
        echo "❌ Usage: $0 start <app_name> <port>"
        exit 1
    fi

    # Controllo config
    CONFIG_PATH="./app/$APP_NAME/application.cfg"
    if [ ! -f "$CONFIG_PATH" ]; then
        echo "❌ Config file $CONFIG_PATH not found"
        exit 1
    fi

    # Creo cartella DB se non esiste
    mkdir -p "$APP_DATA"

    echo "🚀 Launching $APP_NAME on port $APP_PORT with DB in $APP_DATA"

    APP_NAME=$APP_NAME APP_PORT=$APP_PORT APP_DATA=$APP_DATA \
    docker compose -p $APP_NAME up -d

elif [ "$ACTION" = "stop" ]; then
    if [ -z "$APP_NAME" ]; then
        echo "❌ Usage: $0 stop <app_name>"
        exit 1
    fi

    echo "🛑 Stopping and removing $APP_NAME"

    docker compose -p $APP_NAME down -v

elif [ "$ACTION" = "status" ]; then
    echo "ℹ️  Current running apps:"
    docker ps --format "table {{.Names}}\t{{.Ports}}" | grep cardinal

else
    echo "❌ Unknown action: $ACTION"
    echo "Usage:"
    echo "  $0 start <app_name> <port>"
    echo "  $0 stop <app_name>"
    echo "  $0 status"
    exit 1
fi
