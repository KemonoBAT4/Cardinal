
# imports
import os
import configparser

#################
# CONFIGURATION #
#region #########

config = configparser.ConfigParser()

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