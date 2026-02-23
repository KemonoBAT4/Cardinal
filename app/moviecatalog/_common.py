
# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory
from flask_login import login_required

# core imports
from core.models import *
from core.configs import *
from core.web import *
from core.mail import *

# other imports
import os
import typing
from enum import Enum

project_name: str = os.path.dirname(os.path.abspath(__file__))
