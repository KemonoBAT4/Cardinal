
# imports
import os
import configparser
import sys
import typing

#################
# CONFIGURATION #
#region #########

config = configparser.ConfigParser()

args: list = sys.argv.copy()
runner: str = args.pop(0) # run.py
name: str = args.pop(0) # name

def getCardinalText(cardinal: "Cardinal") -> str:
    return f"""

    #######################
    # WELCOME TO CARDINAL #
    #######################

    # --- SYSTEM INFORMATIONS --- #
    - current system name: {cardinal._config.get('Cardinal', 'name')}
    - current system version: {cardinal.version}
    - author: {cardinal._config.get('Cardinal', 'author')}
    - source code: {cardinal._config.get('Cardinal', 'source')}
    - current database version: {cardinal._config.get('Cardinal', 'version')}

    # --- SYSTEM CONFIGURATIONS --- #
    - host: {cardinal._host}
    - port: {cardinal._port}

    # --- DATABASE INFORMATIONS --- #
    - current database path: {cardinal._config.get('Cardinal Database', 'SQLALCHEMY_DATABASE_URI')}

    # --- SYSTEM DEFAULT PATHS --- #
    - cardinal dashboard base path: '/cardinal'
    - cardinal authentication base path: '/access'

    """
# #enddef
#endregion ######


# from bcrypt import hashpw, gensalt, checkpw

# class JsonWebToken: