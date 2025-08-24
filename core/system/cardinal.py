
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
from pathlib import Path
import configparser
import json
import os
import importlib
import pkgutil

# local imports
from core.models.base import BaseModel, db
from core.web.routes import routes
from core.web.api import api






class Cardinal:

    _config = None
    _app = None
    _app_context = None
    _host = None
    _port = None

    # TODO: complete

    def __init__(self, config=None, setup=False):

        self._app = Flask(__name__, template_folder="../web/templates")
        self._config = config
        self._db = db

        self._app_context = self._app.app_context()
        self._app_context.push()

        cors = CORS(self._app)

        try:
            self._app.config['SQLALCHEMY_DATABASE_URI'] = str(self._config.get("Cardinal Database", "SQLALCHEMY_DATABASE_URI"))
        except Exception as e:
            print("Error while setting up database connection: " + str(e))
        #endtry

        self._db.init_app(self._app)

        if setup == True: # TODO: change this, instead of False, use a setup variable
            self.setup()
        #endif

        # TODO: test if this is correct
        self._host = str(self._config.get("Cardinal", "host"))
        self._port = int(self._config.get("Cardinal", "port"))

        # register routes
        self._app.register_blueprint(routes, url_prefix="/")
        self._app.register_blueprint(api, url_prefix="/api/v")
    #enddef

    def run(self, host=None, port=None):
        """
        DESCRIPTION:
        Runs the application.

        PARAMETERS:
        - host: The host to run the application if different from the default
        - port: The port to run the application if different from the default

        RETURN:
        - no return
        """

        self._host = host if host is not None else self._host
        self._port = port if port is not None else self._port

        self.processRoutes()
        self.processApis()

        self._app.run(debug=True, host=self._host, port=self._port)
    #enddef

    def processRoutes(self):
        """
        DESCRIPTION:
        Dynamically import all route files in the directory provided

        PARAMETERS:
        - filename: The name of the file to import

        RETURN:
        - True if the files were imported successfully, False otherwise
        """

        result = self._processBlueprints("routes")
        return result
    #enddef

    def processApis(self):
        """
        DESCRIPTION:
        Dynamically import all route files in the directory provided

        PARAMETERS:
        - filename: The name of the file to import

        RETURN:
        - True if the files were imported successfully, False otherwise
        """

        result = self._processBlueprints("api")
        return result
    #enddef

    def setup(self):
        """
        DESCRIPTION:
        Sets up the database and creates all tables.

        PARAMETERS:
        - no parameters required

        RETURN:
        - True if the database was set up successfully, False otherwise
        """
        print("Setting up database...")
        return self._resetDatabase()
    #enddef

    #############
    # UTILITIES #
    #region #####

    def __del__(self):
        self._app_context.pop()
    #enddef

    def _processBlueprints(self, filename="routes.py"):
        """
        DESCRIPTION:
        Dynamically import all route files in the directory provided

        PARAMETERS:
        - filename: The name of the file to import

        RETURN:
        - True if the files were imported successfully, False otherwise
        """

        app_dir = 'app'

        for folder in os.listdir(app_dir):
            folder_path = os.path.join(app_dir, folder)

            if os.path.isdir(folder_path):
                routes_file = os.path.join(folder_path, f"{filename}.py")

                if os.path.isfile(routes_file):
                    module_name = os.path.splitext(os.path.basename(routes_file))[0]
                    module = importlib.import_module(f'{app_dir}.{folder}.{module_name}')
                    bp = getattr(module, module_name)

                    if filename == "routes":
                        self._addBlueprint(bp, f'/{folder}')
                    elif filename == "api":
                        self._addBlueprint(bp, f'/{folder}/api/v{self._config.get("Cardinal", "api")}')
                    #endif
                #endif
            #endif
        #endfor
    #enddef

    def _addBlueprint(self, bluprint, prefix):
        """
        DESCRIPTION:
        Adds a blueprint to the application.

        PARAMETERS:
        - bluprint: The blueprint to add.
        - prefix: The prefix to use for the blueprint.

        RETURN:
        - True if the blueprint was added successfully, False otherwise.
        """

        try:
            self._app.register_blueprint(bluprint, url_prefix=prefix)
            return True
        except Exception as e:
            return False
        #endtry
    #enddef

    def _resetDatabase(self) -> bool:
        """
        DESCRIPTION:
        Resets the database by dropping all tables and creating new ones.

        PARAMETERS:
        - no parameters required

        RETURN:
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
        DESCRIPTION:
        Dynamically imports all SQLAlchemy models from registred applications.

        PARAMETERS:
        - no parameters required

        RETURN:
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
                    # module = importlib.import_module(module_path)
                #endtry
            #endif
        #endfor

        return imported_models
    #enddef
#endclass

    # class Config:
    #     # Model discovery configuration
    #     MODEL_DISCOVERY_PATHS = [
    #         'apps/*/models.py',
    #         'apps/*/models/*.py',  # Modular models within apps
    #         'libs/*/models.py'     # Shared libraries
    #     ]
    #     MODEL_CLASS_ATTRS = ['__tablename__', '_sa_class_manager']  # SQLAlchemy markers

    # app.config.from_object(Config)

    #endregion ##
