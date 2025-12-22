
from flask import Blueprint
from .handlers import *

api = Blueprint('example_api', __name__)

@api.route('/exmaple')
def apiTest():

    return {"exmaple": "example"}
#enddef
