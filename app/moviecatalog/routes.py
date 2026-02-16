# other imports
import os

# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

# core imports
from core.models.base import db
from core.models.models import *
from core.configs import config
from core.web import *

# local imports
from .models import *

routes = Blueprint(f'moviecatalog_routes', __name__)

@routes.route("/", methods=['GET'])
def index():
    """
    Redirects to the homepage
    """
    return redirect(url_for('moviecatalog_routes.home'))
# #enddef

@routes.route("/home", methods=['GET'])
def home():
    page_title = "The Cardinal System"
    title = "Movie Catalog: Home"

    page = Page(page_title=page_title, title=title)

    card = Card("Home")

    page.addCard(card)
    return page.render()
# #enddef

@routes.route("/configuration/movie/list", methods=['GET'])
def movie_list():

    page = Page(title="Lista Film")
    card = Card("Lista di tutti i Film")

    movie_list_section = Section().table(url="/movie/list")

    card.addSection(movie_list_section)
    page.addCard(card)

    return page.render()
# #enddef

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

# #enddef

