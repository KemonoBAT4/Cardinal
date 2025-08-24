import configparser
import os
import importlib
import pkgutil

from pathlib import Path
from flask import current_app

from .cardinal import Cardinal
from core.models.base import BaseModel

config = configparser.ConfigParser()
config.read("application.cfg")

cardinal = Cardinal(config=config)
