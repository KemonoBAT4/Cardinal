# other imports
import os

# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

# local imports
from core.models.base import db
from core.models.models import *
from core.configs import config
from .pages import *
from .handlers import *

routes = Blueprint('main', __name__)

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

    card = Card("Home")

    page.addCard(card)
    return page.render()
#enddef

##################
# ABOUT CARDINAL #
#region ##########

@routes.route("/about", methods=['GET'])
def about():
    current_version = config.get("Cardinal", "version")
    page_title = "The Cardinal System"
    title = "Cardinal: About"

    page = Page(page_title=page_title, title=title)

    return page.render()
#enddef

#endregion #######

#################z
# GET THE FILES #
#region #########

@routes.route("/styles/<string:app>/<path:filename>", methods=['GET'])
def styles(app, filename):
    if "cardinal" == app:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'styles'), filename)
    else:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', '..', 'app', app, 'static', 'styles'), filename)
    #endif
#enddef

@routes.route("/scripts/<string:app>/<path:filename>", methods=['GET'])
def scripts(app, filename):
    if "cardinal" == app:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'scripts'), filename)
    else:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', '..', 'app', app, 'static', 'scripts'), filename)
    #endif
#enddef

@routes.route("/icons/<string:app>/<path:filename>", methods=['GET'])
def icons(app, filename):
    if "cardinal" == app:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'icons'), filename)
    else:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', '..', 'app', app, 'static', 'icons'), filename)
    #endif
#enddef

@routes.route("/assets/<string:app>/<path:filename>", methods=['GET'])
def assets(app, filename):
    if "cardinal" == app:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'assets'), filename)
    else:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', '..', 'app', app, 'assets'), filename)
    #endif
#enddef

#endregion ######

