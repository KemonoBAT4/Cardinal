
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
    title = "example Catalog: Home"

    page = Page(page_title=page_title, title=title)

    card = Card("Home")

    page.addCard(card)
    return page.render()
# #enddef home

@routes.route("/dashboard/example/list", methods=['GET'])
def example_list():

    page = Page(title="Example List")
    card = Card("Example of a Table")

    example_list_section = Section(title = "Example of a Table").table(
        url = "/example/api/v1/example/list",
        config = {
            "columns": {
                "id"     : { "title": "Id"             },
                "text1"  : { "title": "Example Text 1" },
                "text2"  : { "title": "Example Text 2" },
                "text3"  : { "title": "Example Text 3" },
                "text4"  : { "title": "Example Text 4" },
                "text5"  : { "title": "Example Text 5" },
                "text6"  : { "title": "Example Text 6" },
            }
        },
        # click = "/example/dashboard/example/edit/{id}"
    )

    card.addSection(example_list_section)
    page.addCard(card)

    return page.render()
# #enddef example_list


#endregion ---------------------- DASHBOARD ROUTES ------------------------- #
