# TODO: implement this script

# NOTE: when using this script, it can execute any application in the "app" folder
# the name of the wanted application must be passed as the first argument

# NOTE: if the application wants to be started as setup (so by executing the "setup" function in the designated application)
# then the second argument must be "setup"

# NOTE: any other argument will be passed or converted based on what it is or what the application needs to run


#!/bin/bash

# takes all the apps in ./app as valid apps
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

python run.py "$@"
