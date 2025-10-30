
# flask imports
from flask import Flask, jsonify, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import current_app

# other imports
from pathlib import Path
import configparser
import json
import os
import importlib
import pkgutil

# local imports
from core.models.base import BaseModel, db

# web blueprint imports
from core.web.routes import routes
from core.web.api import api
from core.web.users import users

class Cardinal:

    _config = None

    _app = None
    _app_context = None

    _host = None
    _port = None

    # TODO: complete

    def __init__(self, config=None, setup=False):
        self._app = Flask(__name__, template_folder='../web/templates')
        # , static_folder='../web/static'

        self._config = config
        self._db = db

        self._app_context = self._app.app_context()
        self._app_context.push()

        cors = CORS(self._app)

        if (setup == True):
            self.setup()
        #endif

        self._host = str(self._config.get("Cardinal", "host"))
        self._port = int(self._config.get("Cardinal", "port"))

        self._addBlueprint(routes, "/")
        self._addBlueprint(api, f"/api/v{self._config.get('Cardinal', 'api')}")
        self._addBlueprint(users, "/access")
    #enddef

    def __del__(self):
        self._app_context.pop()
    #enddef

    def setup(self):
        """
        #### DESCRIPTION:
        Sets up the database and creates all tables.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - True if the database was set up successfully, False otherwise
        """
        print("Setting up database...")
        return self._resetDatabase()
    #enddef

    def run(self, host=None, port=None):
        """
        #### DESCRIPTION:
        Runs the application.

        #### PARAMETERS:
        - host: The host to run the application if different from the default
        - port: The port to run the application if different from the default

        RETURN:
        - no return
        """

        self._host = host if host is not None else self._host
        self._port = port if port is not None else self._port

        welcome_text = f"""

        #######################
        # WELCOME TO CARDINAL #
        #######################

        booting now . . .

        # --- SYSTEM INFORMATIONS --- #
        - current system version: {self._config.get('Cardinal', 'version')}
        - author: {self._config.get('Cardinal', 'author')}
        - source code: {self._config.get('Cardinal', 'source')}
        - current database version: {self._config.get('Cardinal', 'version')}

        # --- SYSTEM CONFIGURATIONS --- #
        - host: {self._host}
        - port: {self._port}

        # --- CONFIGURED PATHS --- #
        - cardinal dashboard base path: '/cardinal'
        - cardinal authentication base path: '/access'

        """

        self._app.run(debug=True, host=self._host, port=self._port)
    #enddef

    #############
    # UTILITIES #
    #region #####

    def _resetDatabase(self) -> bool:
        """
        #### DESCRIPTION:
        Resets the database by dropping all tables and creating new ones.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - True if the database was reset successfully, False otherwise.
        """

        models = self._importModels()

        try:
            if self._db is not None:
                self._db.drop_all()
                self._db.create_all()
                return True
            else:
                raise Exception("Database is not set up. Cannot reset.")
            #endif
        except Exception as e:
            print(f"Error resetting the database: {e}")
        #endtry
        return False
    #enddef

    def _importModels(self) -> list:
        """
        #### DESCRIPTION:
        Dynamically imports all SQLAlchemy models from registred applications.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - no return
        """

        if not self._app:
            raise RuntimeError("No Flask application context available.")
        #endif

        cardinal_root = os.path.join(self._app.root_path, "..", "..", "app")
        path_parts =os.path.normpath(cardinal_root).split(os.sep)
        apps_root = os.sep.join(path_parts[:-1])

        apps_root = os.path.join(apps_root, "app")

        imported_models = []

        for dirpath, dirnames, filenames in os.walk(apps_root):
            if 'models.py' in filenames:
                try:
                    module_path = f"app.{(str(os.path.relpath(dirpath, apps_root).replace(os.sep, '.') + '.models'))}"

                    if '__' in module_path:
                        continue
                    #endif

                    module = importlib.import_module(module_path)

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)

                        if isinstance(attr, type) and issubclass(attr, BaseModel) and attr:
                            imported_models.append(attr.__name__)
                            print(f"Imported model: {attr.__name__} from {module_path}")
                        #endif
                    #endfor

                except ImportError as e:
                    print(f"Failed to import model from {dirnames}: {str(e)}")
                except Exception as e:
                    print(f"Unexpected error loading {dirnames}: {str(e)}")
                #endtry
            #endif
        #endfor

        return imported_models
    #enddef

    def _addBlueprint(self, bluprint, prefix):
        """
        #### DESCRIPTION:
        Adds a blueprint to the application.

        #### PARAMETERS:
        - bluprint: The blueprint to add.
        - prefix: The prefix to use for the blueprint.

        #### RETURN:
        - True if the blueprint was added successfully, False otherwise.
        """

        try:
            self._app.register_blueprint(bluprint, url_prefix=prefix)
            return True
        except Exception as e:
            return False
        #endtry
    #enddef

    def _getAllPaths(self):
        # TODO: see if this is correct
        return self._app.url_map.iter_rules()
    #enddef

    #endregion ##
#endclass