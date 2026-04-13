
# flask imports
from flask import Blueprint, redirect, url_for                                  # type: ignore
from flask import render_template, send_from_directory                          # type: ignore
from flask_login import login_required                                          # type: ignore

# core imports
from core.models import *
from core.configs import *
from core.web import *
# from core.mail import *
from core.system import *

# other imports
import os
import typing
from enum import Enum

project_name: str = os.path.dirname(os.path.abspath(__file__))

# "D:\documents\projects\moviecatalog"
MEDIA_FOLDER: str = cardinal.config.get("Cardinal Custom", "MEDIA_FOLDER", fallback="/")
