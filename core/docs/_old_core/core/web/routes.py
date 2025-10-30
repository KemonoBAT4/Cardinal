
# other imports
import os
import configparser

# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

# local imports
from .pages import *
from .handlers import *

from core.models.base import db
from core.models.models import *
from .pages import *

routes = Blueprint('main', __name__)

config = configparser.ConfigParser()
config.read("application.cfg")

@routes.route("/", methods=['GET'])
def index():
    """
    Redirects to the homepage
    """
    return redirect(url_for('main.home'))
#enddef

@routes.route("/home", methods=['GET'])
def home():
    current_version = config.get("Cardinal", "version")
    page_title = "The Cardinal System"
    title = "Cardinal: Home"

    page = Page(page_title=page_title, title=title)

    return page.render()
#enddef

#################z
# GET THE FILES #
#region #########

@routes.route("/styles/<string:app>/<path:filename>", methods=['GET'])
def styles(app, filename):
    if "cardinal" in app.lower():
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'styles'), filename)
    #endif
#enddef

@routes.route("/scripts/<string:app>/<path:filename>", methods=['GET'])
def scripts(app, filename):
    if "cardinal" in app.lower():
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'scripts'), filename)
    #enddef
#enddef


@routes.route("/icons/<string:app>/<path:filename>", methods=['GET'])
def icons(app, filename):
    if "cardinal" in app.lower():
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'icons'), filename)
    #enddef
#enddef

#endregion
