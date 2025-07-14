
# FIXME: fix this if its not working
# from core.system import current_app as app

# other imports
import os
import configparser

# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

# local imports
from core.models.base import db
from core.models.models import *
from core.handlers.handlers import *
from .pages import *

config = configparser.ConfigParser()
config.read("application.cfg")

api = Blueprint('main_routes', __name__)

# /api/v1/

@api.route("/users/<username>", methods=['GET'])
def get_user(username):

    users = User.query.filter(User.username.contains(username)).all()

    if not users:
        pass
    #endif

    return [user.to_dict() for user in users]
#enddef