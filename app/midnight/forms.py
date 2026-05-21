

from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm                                                             # type: ignore

# local imports
from ._common import *
from .handlers import *
from .models import *

from core.form import *
