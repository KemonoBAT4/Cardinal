
# local imports
from ._common import *
from .models import *

api = Blueprint(f'{project_name}_api', __name__)

@api.route("/movie/list", methods=['GET', 'POST'])
def table_movie_list():
    """
    #### DESCRIPTION:
    returns the list of all the movies
    """

    movie_list = Movie.query.all()
    return jsonify({"data": [movie.to_dict() for movie in movie_list]})
# #enddef table_movie_list
