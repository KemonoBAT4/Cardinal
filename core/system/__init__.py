import configparser
import os
import importlib
import pkgutil
import sys

from pathlib import Path
from flask import current_app

from core.models.base import BaseModel
from core.configs import config

from .cardinal import *
# config.read(sys.argv[sys.argv.index("--config")+1] if "--config" in sys.argv else "application.cfg")
#           sys.argv[sys.argv.index("--config")+1] if "--config" in sys.argv else "application.cfg"


cardinal = Cardinal()