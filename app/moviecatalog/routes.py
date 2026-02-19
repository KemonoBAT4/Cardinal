
# local imports
from ._common import *
from .models import *

MEDIA_FOLDER: typing.Final[str] = "/"

routes = Blueprint(f'{project_name}_routes', __name__)

@routes.route("/", methods=['GET'])
def index():
    """
    Redirects to the homepage
    """
    return redirect(url_for('moviecatalog_routes.home'))
# #enddef index

@routes.route("/home", methods=['GET'])
def home():
    page_title = "The Cardinal System"
    title = "Movie Catalog: Home"

    page = Page(page_title=page_title, title=title)

    card = Card("Home")

    page.addCard(card)
    return page.render()
# #enddef home

@routes.route("/configuration/movie/list", methods=['GET'])
def movie_list():

    page = Page(title="Lista Film")
    card = Card("Lista di tutti i Film")

    movie_list_section = Section().table(url="/movie/list")

    card.addSection(movie_list_section)
    page.addCard(card)

    return page.render()
# #enddef movie_list

@routes.route("/configuration/movie/add", methods=['GET'])
@routes.route("/configuration/movie/edit/<int:movie_id>", methods=['GET'])
def movie_edit(movie_id: str = None):

    movie: Movie = None

    if (movie_id is None):
        movie = Movie()
    else:
        movie = Movie.query.get(movie_id)
    # #endif

    form = MovieForm

    page = Page(title="Modifica Film")
    card = Card("Modifica Film")

    form_section = Section().form(
        formtype = form,
        object = movie,
        redir="moviecatalog_routes.movie_list"
    )

    card.addSection(form_section)
    page.addCard(card)

    return page.render()
# #enddef movie_edit

# NOTE: develop this function
@routes.route("/stream/<path:filename>", methods=["GET", "POST"])
def stream(filename: str):
    try:
        return send_from_directory(MEDIA_FOLDER, filenmae)
    except FileNotFoundError:
        abort(404)
    # #endtry
# #enddef stream
