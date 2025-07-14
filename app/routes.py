
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

from core.models.base import db
from core.handlers.handlers import *

from core.web.pages import *
from .handlers import *
from .models import *

config = getConfig()
routes = Blueprint(config.get("name"), __name__)

@routes.route("/test", methods=['GET', 'POST'])
def index():
    return "test"
#enddef
