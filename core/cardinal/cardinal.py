
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
    _prefix = None

    _applications = []  # a list of all the application data
    _threads = []
    _sockets = []

    _version = None
    _api_version = None

    def __init__(self, app, *args, **kwargs):
        self._app = app
        self._app_context = app.app_context()
        self._app_context.push()

        self._config = getConfig()
        self._preix = getApplicationRoutePrefix()
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

        # register the main routes
        current_app.register_blueprint(main_routes, url_prefix="/")
        current_app.register_blueprint(routes, url_prefix=self._prefix)

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

    def resetDatabase(self) -> bool:
        """
        DESCRIPTION:
        Resets the database by dropping all tables and creating new ones.

        PARAMETERS:
        - no parameters required

        RETURN:
        - True if the database was reset successfully, False otherwise.
        """
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
            # logger.error(f"Error resetting the database: {e}")
            # logger.debug("See the log file for the complete error.")
        #endtry
        return False
    #enddef
#endclass

