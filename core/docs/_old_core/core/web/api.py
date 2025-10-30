
from flask import Blueprint
from .pages import *
from .handlers import *

api = Blueprint('main_api', __name__)

@api.route('/test')
def apiTest():
    
    return {"test": "test"}
#enddef

