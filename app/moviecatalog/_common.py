
# other imports
import os
from enum import Enum

# core imports
from core.models import *
from core.web import *
from core.configs import *

# local imports
from .api import *
from .handlers import *
from .models import *
from .forms import *
from .routes import *

project_name: str = os.path.dirname(os.path.abspath(__file__))

