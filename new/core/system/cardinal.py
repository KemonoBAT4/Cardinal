
# flask imports
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask import current_app


# other imports
import configparser
import json
import os

# local imports
from core.models.base import BaseModel, db
from core.models.models import *
# from handlers.handlers import *
from core.web.routes import main_routes
from core.web.apis import api_routes

class Cardinal:

    config = None
    app = None
    host = None
    port = None

    # TODO: complete

    def __init__(self, config=None):

        self.app = Flask(__name__,  template_folder="core/web/templates")
        self.config = config

        try:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = str(self.config.get("Cardinal Database", "SQLALCHEMY_DATABASE_URI"))
        except Exception as e:
            self.logger.info(f"Exception: {e}")
        #endtry

        # TODO: test if this is correct
        self.host = (str(self.config.get("Cardinal", "host")), "0.0.0.0")
        self.port = (int(self.config.get("Cardinal", "port")), 23104)

        # register routes
        self.app.register_blueprint(main_routes, url_prefix="/")
        self.app.register_blueprint(api_routes, url_prefix="")
    #enddef

    def start(self, host=None, port=None):

        self.host = host if host is not None else self.host
        self.port = port if port is not None else self.port

        self.app.run(debug=True, host=self.host, port=self.port)
    #enddef
#endclass