# Cardinal: Home -- home page title

from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

import os
import configparser

from core.models.base import db
from core.models.models import *

from .pages import *

config = configparser.ConfigParser()
config.read("application.cfg")

main_routes = Blueprint('Main_Routes', __name__)

@main_routes.route("/", methods=['GET'])
def index():
    """
    Redirects to the homepage
    """
    return redirect(url_for('Main_Routes.home'))
#enddef

@main_routes.route("/home", methods=['GET'])
def home():
    current_version = config.get("Cardinal", "version")
    username = "Kemono_BAT_4" # current_user.username
    page_title = "The Cardinal System"

    website_title = "Cardinal: Home"

    page = Page(title=page_title, website_title=website_title)
    # section = Section(title)
    # Section()

    # page.addSection(
    # )

    return page.render()

    return render_template(
        'index.html',
        cardinal_version=current_version,
        logged_user=username,
        website_title=website_title,
        page_title=page_title
    )
#enddef

#################
# GET THE FILES #
#region #########

@main_routes.route("/styles/<string:app>/<path:filename>", methods=['GET'])
def styles(app, filename):
    if "cardinal" in app.lower():
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'styles'), filename)
    #endif
#enddef

@main_routes.route("/scripts/<string:app>/<path:filename>", methods=['GET'])
def scripts(app, filename):
    if "cardinal" in app.lower():
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'scripts'), filename)
    #enddef
#enddef


@main_routes.route("/icons/<string:app>/<path:filename>", methods=['GET'])
def icons(app, filename):
    if "cardinal" in app.lower():
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'web', 'icons'), filename)
    #enddef
#enddef

#endregion