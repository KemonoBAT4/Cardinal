
from flask import Blueprint
from core.web.handlers import *
from core.web.pages import *

routes = Blueprint('account', __name__)

@routes.route('/test')
def login():

    page = Page("title")
    return page.render()
#enddef
