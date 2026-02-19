
# local imports
from ._common import *
from .models import *

api = Blueprint('{project_name}_api', __name__)

@api.route("/movie/list", methods=['GET', 'POST'])
def table_movie_list():

    movie_list = Movie.query.all()

    return {"movies": [movie.to_dict() for movie in movie_list]}
#enddef
