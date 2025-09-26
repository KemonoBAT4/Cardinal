
from flask import Blueprint

routes = Blueprint('intranet', __name__)

@routes.route('/test')
def route1Test():
    return 'route 2 test'
#enddef

