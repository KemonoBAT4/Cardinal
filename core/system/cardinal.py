
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
import os
import importlib
import secrets
import typing

# local imports
from core.models.base import BaseModel, db
from core.configs import config, ARGUMENTS_LIST

# web blueprint imports
from core.web.routes import routes
from core.web.api import api
from core.web.users import users


class Cardinal:

    _config = None
    _name = None

    _app: Flask = None
    _app_context = None

    _host: str = "0.0.0.0"
    _port: int = 23104

    _reference_app: str = None

    _secret: str = None

    def __init__(self, name: str = "cardinal"):

        # sets the name
        self._name = name

        # init the application
        self._initApplication()
    #enddef

    ##################
    # PUBLIC METHODS #
    #region ##########
    def setup(self) -> bool:
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

    def run(self, host=None, port=None) -> None:
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

        if (self._name != "cardinal"):
            self._addBlueprint(importlib.import_module(f'app.{self._name}.routes').routes, f"/{self._name}")
            self._addBlueprint(importlib.import_module(f'app.{self._name}.api').api, f"/{self._name}/api/v{self._config.get('Cardinal', 'api')}")
        #endif

        # print(self._app.url_map)

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

    def reload(self, name: str) -> None:
        """
        #### DESCRIPTION:
        Reloads the application. This re-creates the application based
        on the new configuration name given (the "name" is the name of the application folder in the "app" folder).

        #### PARAMETERS:
        - name: The name of the application folder in the "app" folder

        #### RETURN:
        - no return
        """

        # sets the name
        self._name = name

        # init the application
        self._initApplication()
    # #enddef
    #endregion #######


    ##############
    # PROPERTIES #
    #region ######
    @property
    def app(self) -> Flask:
        return self._app
    # #enddef

    @property
    def secret(self) -> str:
        return self._secret if self._secret is not None else self._generateSecretKey()
    # #enddef
    #endregion ###


    #############
    # UTILITIES #
    #region #####

    def handle(self, argument: str) -> None:
        argument = argument.lower()
        # help argument
        if (argument == "--help" or argument == "help"):
            print("Available arguments:")
            for key, argument in ARGUMENTS_LIST:
                print(f" - {key}: {argument['description']}")
            #endfor

        elif (argument == "--version" or argument == "version"):
            print(f"Cardinal Version: {self._config.get('Cardinal', 'version_type')} {self._config.get('Cardinal', 'version')}")

        elif (argument == "--info" or argument == "info"):
            # booting now . . .
            welcome_text = f"""

            #######################
            # WELCOME TO CARDINAL #
            #######################

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
        # #endif
    # #enddef

    def _initApplication(self) -> None:
        """
        #### DESCRIPTION:
        Initializes the application in the same Cardinal instance, overwriting the previous one.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - no return
        """

        # , static_folder='../web/static'
        self._app = Flask(__name__, template_folder='../web/templates')

        # gets the configuration
        self._setupApplicationConfig()

        cors = CORS(self._app)

        # csrf
        self._app.config["SECRET_KEY"] = self._generateSecretKey()


        self._db = db
        self._app_context = self._app.app_context()
        self._app_context.push()

        self._app.config['SQLALCHEMY_DATABASE_URI'] = str(self._config.get("Cardinal Database", "SQLALCHEMY_DATABASE_URI"))
        self._db.init_app(self._app)

        self._host = str(self._config.get("Cardinal", "host"))
        self._port = int(self._config.get("Cardinal", "port"))

        self._addBlueprint(routes, "/")
        self._addBlueprint(api, f"/api/v{self._config.get('Cardinal', 'api')}")
        self._addBlueprint(users, "/access")
    # #enddef

    def _generateSecretKey(self) -> str:
        """
        #### DESCRIPTION:
        Generates a secret key for the application.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - no return
        """

        secret = secrets.token_hex(32)

        self._secret = secret
        return self._secret
    # #enddef

    def _setupApplicationConfig(self) -> None:
        """
        #### DESCRIPTION:
        Returns the application configuration.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - no return
        """

        config = configparser.ConfigParser()

        if (self._name != "cardinal"):
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', self._name, 'application.cfg')
        else:
            # cardinal
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'application.cfg')
        #endif

        config.read(config_path)
        self._config = config
    # #enddef

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
    # #enddef

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

        apps_root = os.path.join(self._app.root_path, "..", "..", "app", self._name)

        imported_models = []

        for dirpath, dirnames, filenames in os.walk(apps_root):
            if 'models.py' in filenames:
                try:

                    module_path = f"app.{self._name}.models"
                    module = importlib.import_module(module_path)

                    # Loop through all the attributes in the module
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
    # #enddef

    def _addBlueprint(self, bluprint, prefix) -> bool:
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
    # #enddef

    def _getAllPaths(self) -> typing.Any:
        return self._app.url_map
    # #enddef

    #endregion ##

    def __del__(self):
        self._app_context.pop()
    # #enddef

    def __repr__(self) -> str:
        return f"<Cardinal {self._config.get('Cardinal', 'version')}>"
    # #enddef
#endclass
