
# local imports
from ._common import *
from .models import *

api = Blueprint(f'{project_name}_api', __name__)

@api.route("/example/list", methods=['GET', 'POST'])
def table_example_list():
    """
    #### DESCRIPTION:
    returns the list of all the movies
    """

    example_list = Example.query.all()
    return jsonify({"data": [example.to_dict() for example in example_list]})
# #enddef table_example_list
