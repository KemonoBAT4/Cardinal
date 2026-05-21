
# local imports
from ._common import *
from .models import *

api = Blueprint(f'{project_name}_api', __name__)

@api.route("/midnight/list", methods=['GET', 'POST'])
def table_midnight_list():
    return jsonify({"data": "not implemented yet"})
# #enddef table_midnight_list
