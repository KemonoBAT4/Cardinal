# other imports
import os
import configparser

# flask imports
from flask import Blueprint, redirect, url_for, request, jsonify
from flask import render_template, send_from_directory
from flask_login import login_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# local imports
from .pages import *
from .handlers import *

from core.configs import config

from core.models.base import db
from core.models.models import User

auth = Blueprint('auth', __name__)

@auth.route("/", methods=['GET'])
def index():
    return redirect(url_for('access.me'))
# #enddef index

@auth.route("/login", methods=['GET', 'POST'])
def login():
    return ""
# #enddef login

@auth.route("/register", methods=['GET', 'POST'])
def register():

    if (request.method == 'POST'):
        # TODO: implement register
        data = request.get_json()

        pass
    else:
        page = Page(page_title="The Cardinal System", title="Cardinal: Register")
        return page.render()
    # #endif
# #enddef register

@auth.route("/me", methods=['GET'])
def me():

    # TODO: really check if the user is logged in
    tempUserLogged = False

    if (tempUserLogged == False):
        return redirect(url_for("access.login"))
    else:
        page = Page(page_title="The Cardinal System", title="Cardinal: Me")
        return page.render()
    # #endif
# #enddef me

@auth.route("/logout", methods=['GET'])
def logout():

    # TODO: really check if the user is logged in
    tempUserLogged = False

    if (tempUserLogged == True):
        # TODO: implement logout
        pass
    #endif

    return redirect(url_for("access.login"))
#enddef
