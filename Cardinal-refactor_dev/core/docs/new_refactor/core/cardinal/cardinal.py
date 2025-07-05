
import os
import uuid
import socket
import configparser
import threading
import time
import subprocess
import importlib
import json

from core.models.base import db
from core.models.models import *
from core.handlers.handlers import *
from core.web.routes import main_routes
from application.routes import routes

from flask import current_app

class Cardinal:

    _app = None
    _app_context = None
    _db = None

    _config = None

    _applications = []  # a list of all the application data
    _threads = []
    _sockets = []

    _version = None
    _api_version = None

    def __init__(self, app, config: dict):

        self._app = app
        self._app_context = app.app_context()
        self._app_context.push()

        self._config = config
        # self._config = config if config else configparser.ConfigParser()

        self._db = db

        # Register routes
        # self._app.register_blueprint(main_routes)

        # Load version from config
        # self._version = self._config.get("Cardinal", "version", fallback="0.1.0")
    #enddef

    def __del__(self):
        self._app_context.pop()
    #enddef

    def start(self):
        """
        DESCRIPTION:
        Starts the Cardinal instance by setting up the database, loading registered applications,
        and starting the applications in separate threads or sockets.

        PARAMETERS:
        - no parameters required

        RETURN:
        - no return
        """
        main_prefix = f'/'

        # register the main routes
        current_app.register_blueprint(main_routes, url_prefix=main_prefix)

        # register the application routes
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", 'application', 'config.json')
        data = {}

        with open(json_path, 'r') as f:
            data = json.load(f)
        #endwith
        current_app.register_blueprint(routes, url_prefix=data.get("prefix"))

        # initialize all the applications
        # # # # # # # # import os
        # # # # # # # # import importlib

        # # # # # # # # applications_folder = 'applications'

        # # # # # # # # # Get all folder names inside the applications folder
        # # # # # # # # app_folders = [f.name for f in os.scandir(applications_folder) if f.is_dir()]

        # # # # # # # # for app_folder in app_folders:
        # # # # # # # #     try:
        # # # # # # # #         # Construct the module path for the routes file
        # # # # # # # #         routes_module_path = f'{applications_folder}.{app_folder}.routes'

        # # # # # # # #         # Import the routes module
        # # # # # # # #         routes_module = importlib.import_module(routes_module_path)

        # # # # # # # #         # Get the <applicationname_routes> variable
        # # # # # # # #         app_routes_var_name = f'{app_folder}_routes'
        # # # # # # # #         if hasattr(routes_module, app_routes_var_name):
        # # # # # # # #             app_routes = getattr(routes_module, app_routes_var_name)
        # # # # # # # #             print(f'Routes for {app_folder}: {app_routes}')
        # # # # # # # #         else:
        # # # # # # # #             print(f'No routes variable found for {app_folder}')
        # # # # # # # #     except Exception as e:
        # # # # # # # #         print(f'Error processing {app_folder}: {e}')


        # if not self._running:
        #     self._running = True


            # self._logger.debug(self._showStartData())
            # self._setupApplications()
            # self._startApplications()
    #enddef
#endclass






















# class Handlers:
#     def __init__(self):
#         pass

# logger = CardinalLogger()

# def resetDatabase(self):
#     """
#     DESCRIPTION:
#     Resets the database by dropping all tables and creating new ones.

#     PARAMETERS:
#     - no parameters required

#     RETURN:
#     - no return
#     """
#     try:
#         if db is not None:
#             logger.debug("Resetting the database . . .")
#             db.drop_all()
#             db.create_all()
#             logger.debug("Database reset complete")
#         else:
#             logger.error("Database is not set up. Cannot reset.")
#         #endif
#     except Exception as e:
#         logger.error(f"Error resetting the database: {e}")
#         logger.debug("See the log file for the complete error.")
#     #endtry
# #endde

