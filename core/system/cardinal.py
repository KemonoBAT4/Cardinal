
# flask imports
from flask import Flask, jsonify, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
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
from core import configs # ARGUMENTS_LIST, HELP_COMMANDS_LIST, INFO_COMMANDS_LIST, name
from core.handlers import *

# web blueprint imports
from core.web.routes import routes
from core.web.api import api
from core.web.users import users
from core.models.models import User

class Cardinal:

    _config: "configparser.ConfigParser"
    _name: "str | None" = None

    _app: "Flask"
    _app_context =  None

    _host: str = "0.0.0.0"
    _port: int = 23104

    _secret: "str | None" = None
    _mail: "Mail | None" = None

    def __init__(self, name: str = "cardinal"):

        # sets the name
        self._name = name

        # init the application
        self._initApplication()
    # #enddef __init__

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
    # #enddef setup

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
    # #enddef run

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
    # #enddef reload

    def handle(self) -> None:
        """
        #### DESCRIPTION:
        Handles the command line arguments.

        #### PARAMETERS:
        - arguments: The command line arguments

        #### RETURN:
        - no return
        """

        # NOTE: this is a temporary solution, need to find a better way to
        # handle all the commands, including --help on specific commands
        # also need to implement a way to show all the commands (rewrite the _buildCommandText function)

        ARGUMENTS_LIST = {
            "setup"   : { "description": "Sets up the selected application", "callable": self.setup  , "example": "python run.py <application name> setup"   },
            "run"     : { "description": "Runs the selected application"   , "callable": self.run    , "example": "python run.py <application name> run"     },
            "build"   : { "description": "Builds the selected application" , "callable": self.build  , "example": "python run.py <application name> build"   },
            "deploy"  : { "description": " - Not implemented yet"          , "callable": self.deploy , "example": "python run.py <application name> deploy"  },
            "migrate" : { "description": "Migrates the database"           , "callable": self.migrate, "example": "python run.py <application name> migrate" },
        }

        INFO_COMMANDS_LIST = [
            "--info",
            "--i",
            "-info",
            "-i",
            "info"
        ]

        HELP_COMMANDS_LIST = [
            "--help",
            "--h"
            "-help",
            "-h",
            "help",
        ]

        args: list = configs.args
        name   = configs.name

        if (name in HELP_COMMANDS_LIST):
            print("Available commands:")
            for key, argument in ARGUMENTS_LIST.items():
                print(f" - {key}: {argument['description']}")
            # #endfor

            print("")

            print("Available info commands:")
            for command in INFO_COMMANDS_LIST:
                print(f" - {command}")
            # #endfor
            return None
        # #endif

        self.reload(name=name)
        command: str = str(args.pop(0)).lower()


        if (command in INFO_COMMANDS_LIST):
            print(configs.getCardinalText(cardinal=self))

        elif (command in ARGUMENTS_LIST.keys()):
            callable_function = ARGUMENTS_LIST[command]["callable"]
            callable_function()
        # #endif
    # #enddef handle

    def build(self):
        print("Function not implemented yet.")
    # #enddef build

    def deploy(self):
        print("Function not implemented yet.")
    # #enddef deploy

    def migrate(self):
        print("Function not implemented yet.")
    # #enddef migrate
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

    @property
    def version(self) -> str:
        return f"{self. _config.get('Cardinal', 'version_type')} {self._config.get('Cardinal', 'version')}"
    # #enddef

    @property
    def mail(self) -> "Mail | None":
        return self._mail
    # #enddef

    #endregion ###


    #############
    # UTILITIES #
    #region #####

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
        # NOTE: change the template folder to the application templates folder
        self._app = Flask(__name__, template_folder='../web/templates')

        # gets the configuration
        self._setupApplicationConfig()

        cors = CORS(self._app)

        # login
        login_manager = LoginManager()

        login_manager.init_app(self._app)
        login_manager.login_view = "access.login" # type: ignore

        @login_manager.user_loader
        def load_user(user_id: int) -> User:
            return User.query.get(int(user_id)) # type: ignore
        # #enddef load_user

        # mail server
        try:
            self._app.config["MAIL_SERVER"] = str(self._config.get("Cardinal Mail", "MAIL_SERVER"))
            self._app.config["MAIL_PORT"] = str(self._config.get("Cardinal Mail", "MAIL_PORT"))
            self._app.config["MAIL_USE_TLS"] = str(self._config.get("Cardinal Mail", "MAIL_USE_TLS"))
            self._app.config["MAIL_USERNAME"] = str(self._config.get("Cardinal Mail", "MAIL_USERNAME"))
            self._app.config["MAIL_PASSWORD"] = str(self._config.get("Cardinal Mail", "MAIL_PASSWORD"))
            self._app.config["MAIL_DEFAULT_SENDER"] = str(self._config.get("Cardinal Mail", "MAIL_DEFAULT_SENDER"))
        except Exception as e:
            pass
            # print(self.logger.info("Errors during mail setup ... skipping"))
            # print(self.logger.error(f"[Mail Error] - {e}"))
        # #endtry

        self._mail = Mail(self._app)

        # csrf
        self._app.config["SECRET_KEY"] = self._generateSecretKey()

        # app context & database
        self._db = db
        self._app_context = self._app.app_context()
        self._app_context.push()

        self._app.config['SQLALCHEMY_DATABASE_URI'] = str(self._config.get("Cardinal Database", "SQLALCHEMY_DATABASE_URI"))
        self._db.init_app(self._app)

        # gets the host and port

        self._host = str(self._config.get("Cardinal", "host"))
        self._port = int(self._config.get("Cardinal", "port"))

        # core blueprints setup for the application
        self._addBlueprint(routes, "/")
        self._addBlueprint(api, f"/api/v{self._config.get('Cardinal', 'api')}")
        self._addBlueprint(users, "/access")
    # #enddef _initApplication

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
    # #enddef _generateSecretKey

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
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', self._name, 'application.cfg') # type: ignore
        else:
            # cardinal
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'application.cfg')
        #endif

        config.read(config_path)
        self._config = config
    # #enddef _setupApplicationConfig

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
    # #enddef _resetDatabase

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

        apps_root = os.path.join(self._app.root_path, "..", "..", "app", self._name) # type: ignore

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
    # #enddef _importModels

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
    # #enddef _addBlueprint

    def _getAllPaths(self) -> typing.Any:
        return self._app.url_map
    # #enddef _getAllPaths

    def _buildCommandText(
        self,
        name: str,
        description: str,
        options: str,
        example: str
    ) -> str:

        return f"""
        command: {name}
        -------------------------------------

        Description: {description}
        -------------------------------------

        Options: {options}
        -------------------------------------

        Example: {example}
        -------------------------------------
        """
    # #enddef _buildCommandText

    def _ports(self) -> str:
        pass
    # #enddef _ports

    #endregion ##

    def __del__(self):
        self._app_context.pop() # type: ignore
    # #enddef

    def __repr__(self) -> str:
        return f"<Cardinal {self._config.get('Cardinal', 'version')}>"
    # #enddef
#endclass
