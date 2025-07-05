
from core.models.base import db
from core.models.models import *
from core.handlers.handlers import *

from .models import *

import os
import json















#############
# UTILITIES #
#region #####

def get_config() -> dict:
    data = {}

    with open(f'{os.path.dirname(os.path.realpath(__file__))}\config.json', 'r') as f:
        data = json.load(f)
    #endwith

    return data
#enddef

#endregion ##

