
from flask import Blueprint
api = Blueprint('account_api', __name__)

@api.route('/test')
def apiTest():
    return {"test": "test"}
#enddef