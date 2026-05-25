
# flask imports
from flask import Flask, jsonify, redirect, url_for                                                                 # type: ignore
from flask_cors import CORS                                                                                         # type: ignore
from flask_sqlalchemy import SQLAlchemy                                                                             # type: ignore
from flask_migrate import Migrate                                                                                   # type: ignore
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user              # type: ignore
from flask_bcrypt import Bcrypt                                                                                     # type: ignore
from flask_mail import Mail, Message                                                                                # type: ignore
from flask import current_app                                                                                       # type: ignore
from flask_jwt_extended import JWTManager                                                                           # type: ignore

# other imports
from pathlib import Path
from dotenv import load_dotenv
import configparser
import os
import importlib
import secrets
import typing
import datetime

# local imports
from core.models.base import BaseModel, db
from core import configs # ARGUMENTS_LIST, HELP_COMMANDS_LIST, INFO_COMMANDS_LIST, name
from core.handlers import *

# web blueprint imports
from core.web.routes import routes
from core.web.api import api
from core.web.users import auth
from core.models.models import User

class Cardinal:

    _config: "configparser.ConfigParser"
    _name  : "str | None" = None

    _app        :"Flask"
    _app_context: "typing.Any"

    _host: str = "0.0.0.0"
    _port: int = 23104

    _secret     : "str        | None" = None
    _mail       : "Mail       | None" = None
    _jwt_manager: "JWTManager | None" = None

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
        is_resetted = self._resetDatabase()

        if is_resetted:
            cli_module = importlib.import_module(f'app.{self._name}.cli')
            application_setup_function = getattr(cli_module, 'setup', None)

            if application_setup_function is not None:
                application_setup_function()
            # #endif
        # #endif

        return is_resetted
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
            "--h",
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
            print(configs.get_cardinal_text(cardinal=self))

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

    def send_mail(
        self,
        subject: str,
        sender: str,
        recipients: "str | list[str | tuple[str, str]]",
        text_body: str,
        html_body: str,
        attachments: typing.Any = None
    ) -> "typing.Any":

        if isinstance(recipients, str):
            recipients = [recipients]
        # #endif

        message = Message(subject, sender=sender, recipients=recipients)

        message.body = text_body
        message.html = html_body

        if attachments is not None:
            message.attachments = attachments
        # #endif

        response: str = ""

        if (self._mail is not None):
            pass
            # response = self._mail.send(message)
        # #endif

        return response
    # #enddef send_mail

    #endregion #######


    ##############
    # PROPERTIES #
    #region ######

    @property
    def app(self) -> Flask:
        return self._app
    # #enddef app

    @property
    def secret(self) -> str:
        return self._secret if self._secret is not None else self._generateSecretKey()
    # #enddef secret

    @property
    def version(self) -> str:
        return f"{self. _config.get('Cardinal', 'version_type')} {self._config.get('Cardinal', 'version')}"
    # #enddef version

    @property
    def mail(self) -> "Mail | None":
        return self._mail
    # #enddef mail

    @property
    def config(self) -> "configparser.ConfigParser":
        return self._config
    # #enddef config

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
        template_folder = "../web/templates"

        # NOTE: change the template folder to the application templates folder
        # TODO: later implementation needed
        # , static_folder='../web/static'
        # if (self._name != "cardinal"):
        #     template_folder = f"../../app/{self._name}/templates"
        # # #endif

        # NOTE: change the template folder to the application templates folder
        self._app = Flask(
            __name__,
            template_folder=template_folder,
            # static_folder=f"../../app/{self._name}/static" # TODO: later implementation needed
        )

        load_dotenv()

        # gets the configuration
        self._setupApplicationConfig()

        cors = CORS(self._app)

        # login
        login_manager = LoginManager()

        login_manager.init_app(self._app)
        login_manager.login_view = "access.login" # type: ignore

        @login_manager.user_loader
        def load_user(user_id: int) -> "User | None":
            return User.query.get(int(user_id))
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

        self._app.config["SECRET_KEY"]               = os.getenv("JWT_SECRET_KEY")
        self._app.config["JWT_SECRET_KEY"]           = os.getenv("JWT_SECRET_KEY")
        self._app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)

        self._jwt_manager = JWTManager(self._app)

        # database
        db = SQLAlchemy(self._app)

        # app context & database
        self._db = db
        self._app_context = self._app.app_context()
        self._app_context.push()

        self._app.config['SQLALCHEMY_DATABASE_URI'] = configs.build_db_uri(self._config)
        # self._app.config['SQLALCHEMY_DATABASE_URI'] = str(self._config.get("Cardinal Database", "SQLALCHEMY_DATABASE_URI"))
        self._db.init_app(self._app)

        # gets the host and port
        self._host = str(self._config.get("Cardinal", "host"))
        self._port = int(self._config.get("Cardinal", "port"))

        # core blueprints setup for the application
        self._addBlueprint(routes, "/")
        self._addBlueprint(api, f"/api/v{self._config.get('Cardinal', 'api')}")
        self._addBlueprint(auth, "/auth")
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
        return "Not Implemented Yet"
    # #enddef _ports

    #endregion ##


    def __del__(self):
        self._app_context.pop() # type: ignore
    # #enddef

    def __repr__(self) -> str:
        return get_class_repr(classobject=self.__class__, description=self._config.get('Cardinal', 'version'))
    # #enddef __repr__
#endclass
