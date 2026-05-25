
# local imports
from ._common import *
from .models import *
from .forms import *

routes = Blueprint(f'{project_name}_routes', __name__)

#region ------------------------- DASHBOARD ROUTES ------------------------- #

@routes.route("/", methods=['GET'])
def index():
    """
    Redirects to the homepage
    """
    return redirect(url_for(f'{project_name}_routes.home'))
# #enddef index

@routes.route("/home", methods=['GET'])
def home():
    page_title = "The Cardinal System"
    title = "Midnight: Home"

    page = Page(page_title=page_title, title=title)

    card = Card("Home")

    page.addCard(card)
    return page.render()
# #enddef home
