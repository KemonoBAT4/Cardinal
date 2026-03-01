
# local imports
from ._common import *
from .models import *

api = Blueprint(f'{project_name}_api', __name__)

@api.route("/movie/list", methods=['GET', 'POST'])
def table_movie_list():


    return {
        "data": [
            {
                "id": 1,
                "nome": "Mario Rossi",
                "eta": 30,
                "citta": "Roma"
            },
            {
                "id": 2,
                "nome": "Luca Bianchi",
                "eta": 25,
                "citta": "Milano"
            }
        ]
    }
    movie_list = Movie.query.all()

    return [movie.to_dict() for movie in movie_list]
#enddef
