# /api.py

from flask import Blueprint

api = Blueprint('Example_api', __name__)

@api.route('/test')
def apiTest():
    return {"test": "test"}
#enddef