
# flask imports
from flask import Blueprint, redirect, url_for, request, jsonify                     # type: ignore
from flask import render_template, send_from_directory                               # type: ignore
from flask_login import login_required                                               # type: ignore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import and_, or_

# core imports
from core.models import *
from core.configs import *
from core.web import *
# from core.mail import *
from core.system import *

# other imports
import os
import typing
import datetime
from enum import Enum

project_name: str = os.path.dirname(os.path.abspath(__file__))


################
# ENUMERATIVES #
#region ########

class TaskStatus(Enum):
    OPEN        = "open"
    IN_PROGRESS = "in_progress"
    CLOSED      = "closed"
    CANCELLED   = "cancelled"
# #endclass TaskStatus

#endregion #####
