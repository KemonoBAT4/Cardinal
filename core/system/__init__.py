import configparser
import os
import importlib
import pkgutil
import sys

from pathlib import Path
from flask import current_app

from .cardinal import Cardinal
from core.models.base import BaseModel
from core.configs import config

# config.read(sys.argv[sys.argv.index("--config")+1] if "--config" in sys.argv else "application.cfg")
#           sys.argv[sys.argv.index("--config")+1] if "--config" in sys.argv else "application.cfg"
cardinal = Cardinal(_config=config)
