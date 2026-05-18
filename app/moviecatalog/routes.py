
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
    title = "Movie Catalog: Home"

    page = Page(page_title=page_title, title=title)

    card = Card("Home")

    page.addCard(card)
    return page.render()
# #enddef home

@routes.route("/dashboard/movie/list", methods=['GET'])
def movie_list():

    page = Page(title="Lista Film")
    card = Card("Lista di tutti i Film")

    movie_list_section = Section(title = "Lista di tutti i Film Presenti").table(
        url = "/moviecatalog/api/v1/movie/list",
        config = {
            "columns": {
                "id"             : { "title": "ID"          },
                "title"          : { "title": "Titolo"      },
                "description"    : { "title": "Descrizione" },
            }
        },
        click = "/moviecatalog/dashboard/movie/edit/{id}"
    )

    card.addSection(movie_list_section)
    page.addCard(card)

    return page.render()
# #enddef movie_list

@routes.route("/dashboard/movie/add", methods=['GET', 'POST'])
@routes.route("/dashboard/movie/edit/<int:movie_id>", methods=['GET', 'POST'])
def movie_edit(movie_id: "str | None" = None):

    title: str = "Modifica Film" if movie_id is not None else "Aggiungi Film"
    movie: Movie = Movie.query.get(movie_id) if movie_id is not None else Movie()

    form = MovieForm(obj = movie)
    form._obj = movie

    if form.validate_on_submit():

        if "submit" in request.form:
            form.saveForm(movie)
        # #endif

        return redirect(url_for(f"{project_name}_routes.movie_list"))
    # #endif

    page = Page(title=title)
    card = Card(title)
    section = Section(title="").form(form, action=request.path)

    card.addSection(section)
    page.addCard(card)

    return page.render()
# #enddef movie_edit

@routes.route("/configuration/movie/list", methods=['GET'])
def configuration_movie_list():

    page = Page(title="Lista Film")
    card = Card("Lista di tutti i Film")

    movie_list_section = Section(title = "Lista di tutti i Film Presenti").table(
        url = "/moviecatalog/api/v1/movie/list",
        config = {
            "columns": {
                "id"             : { "title": "ID"          },
                "title"          : { "title": "Titolo"      },
                "description"    : { "title": "Descrizione" },
                "movie_file_name": { "title": "Nome File"   },
            }
        },
        click = ""
    )

    card.addSection(movie_list_section)
    page.addCard(card)

    return page.render()
# #enddef movie_list

#endregion ---------------------- DASHBOARD ROUTES ------------------------- #

#region ------------------------- APP ROUTES ------------------------- #
#endregion ---------------------- APP ROUTES ------------------------- #


#region ---
# @routes.route("/configuration/movie/add", methods=['GET'])
# @routes.route("/configuration/movie/edit/<int:movie_id>", methods=['GET'])
# def movie_edit(movie_id: "str | None" = None):

#     movie: "Movie | None" = None

#     if (movie_id is None):
#         movie = Movie()
#     else:
#         movie = Movie.query.get(movie_id)
#     # #endif

#     form = MovieForm

#     page = Page(title="Modifica Film")
#     card = Card("Modifica Film")

#     form_section = Section().form(
#         formtype = form,
#         object = movie,
#         redir="moviecatalog_routes.movie_list"
#     )

#     card.addSection(form_section)
#     page.addCard(card)

#     return page.render()
# # #enddef movie_edit
#endregion ---

# NOTE: develop this function
@routes.route("/stream/<path:filename>", methods=["GET", "POST"]) # type: ignore
def stream(filename: str):
    # NOTE: this is currently working
    # use this snippet
    #<!DOCTYPE html>
    # <html lang="en">
    #     <head>
    #         <meta charset="UTF-8">
    #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #         <title>Document</title>
    #     </head>
    #     <body>
    #         <video width="640" height="480" autoplay controls>
    #             <source src="http://127.0.0.1:23104/moviecatalog/stream/Arknights The Movie Stars From The End.mp4" type="video/mp4">
    #         </video>
    #     </body>
    # </html>

    try:
        print(f"{MEDIA_FOLDER}\{filename}")
        return send_from_directory(MEDIA_FOLDER, filename)
    except FileNotFoundError:
        # abort(404)
        pass
    # #endtry
# #enddef stream
