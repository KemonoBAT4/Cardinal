# other imports
import os

# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

# core imports
from core.models.base import db
from core.models.models import *
from core.configs import config
from core.web import *

# local imports
from .forms import *
from .models import *
from .handlers import *

routes = Blueprint('moviecatalog_routes', __name__)

@routes.route("/", methods=['GET'])
def index():
    """
    Redirects to the homepage
    """
    return redirect(url_for('example_routes.home'))
#enddef
@routes.route("/home", methods=['GET'])
def home():
    page_title = "The Cardinal System"
    title = "Example: Home"

    page = Page(page_title=page_title, title=title)

    card = Card("Home")

    page.addCard(card)
    return page.render()
#enddef
