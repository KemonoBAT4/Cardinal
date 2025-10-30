# other imports
import os
import configparser

# flask imports
from flask import Blueprint, redirect, url_for, request
from flask import render_template, send_from_directory

# local imports
from .pages import *
from .handlers import *

from core.configs import config

from core.models.base import db
from core.models.models import User

users = Blueprint('access', __name__)

@users.route("/", methods=['GET'])
def index():
    return redirect(url_for('access.me'))
#enddef

@users.route("/login", methods=['GET', 'POST'])
def login():

    if (request.method == 'POST'):
        # TODO: implement login
        pass
    else:
        page = Page(page_title="The Cardinal System", title="Cardinal: Login")
        return page.render()
    #endif
#enddef

@users.route("/register", methods=['GET', 'POST'])
def register():

    if (request.method == 'POST'):
        # TODO: implement register
        pass
    else:
        page = Page(page_title="The Cardinal System", title="Cardinal: Register")
        return page.render()
    #endif
#enddef

@users.route("/me", methods=['GET'])
def me():

    # TODO: really check if the user is logged in
    tempUserLogged = False

    if (tempUserLogged == False):
        return redirect(url_for("access.login"))
    else:
        page = Page(page_title="The Cardinal System", title="Cardinal: Me")
        return page.render()
    #endif
#enddef

@users.route("/logout", methods=['GET'])
def logout():

    # TODO: really check if the user is logged in
    tempUserLogged = False

    if (tempUserLogged == True):
        # TODO: implement logout
        pass
    #endif

    return redirect(url_for("access.login"))
#enddef
