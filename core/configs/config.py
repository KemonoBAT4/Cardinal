
# imports
import os
import configparser
import sys

#################
# CONFIGURATION #
#region #########

config = configparser.ConfigParser()

args: list = sys.argv.copy()
runner: str = args.pop(0) # run.py
name: str = args.pop(0) # name

ARGUMENTS_LIST = [
    "setup",
    "run",
    "test",   # TODO: not implemented yet
    "build",  # TODO: not implemented yet
    "deploy", # TODO: not implemented yet
    "migrate" # TODO: not implemented yet

    "--help",
    "help",
]
#endregion ######


# from bcrypt import hashpw, gensalt, checkpw

# class JsonWebToken: