
# flask imports:
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from core.cardinal.cardinal import Cardinal

# other imports
import configparser
import json
import os

# local imports
from core.cardinal.cardinal import Cardinal
from core.models.base import db
from core.handlers.handlers import *

# Create App
app = Flask(__name__,  template_folder="core/web/templates")
cors = CORS(app)

config = configparser.ConfigParser()
config.read("application.cfg")

host = str(config.get("Cardinal", "host"))
# port = int(config.get("Cardinal", "port"))

# register the application routes
# json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'application', 'config.json')
# json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'application', 'config.json')

data = getConfig()

# with open(json_path, 'r') as f:
#     data = json.load(f)
# #endwith

try:
    # mysql+pymysql://root:root@localhost/ProgrammingLibrary
    app.config['SQLALCHEMY_DATABASE_URI'] = data.get("sql_alchemy_uri") if data.get("sql_alchemy_uri") != "" or data.get("sql_alchemy_uri") != "default-sql-alchemy-uri" else config.get("Cardinal", "SQLALCHEMY_DATABASE_URI")
    port = int(config.get("Cardinal", "port"))
except ValueError:
    port = 5000
#endtry

# Init app's database
db.init_app(app)

cardinal = Cardinal(app=app, config=data)

if __name__ == "__main__":
    cardinal.start()
    app.run(debug=True, host=host, port=port)
#endif
