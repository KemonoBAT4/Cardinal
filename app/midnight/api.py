
# local imports
from ._common import *
from .models import *

api = Blueprint(f'{project_name}_api', __name__)

# @api.route("/midnight/list", methods=['GET', 'POST'])
# def table_midnight_list():
#     return jsonify({"data": "not implemented yet"})
# # #enddef table_midnight_list

@api.route("/tasks/list", methods=['GET', 'POST'])
@jwt_required()
def tasks_all_list():
    current_user_uname  = get_jwt_identity()
    user: "User | None" = User.query.filter(User.uname == current_user_uname).first()

    if user is None:
        return jsonify({"status": False, "message": "User not found"}), 401
    # #endif

    tasks: list[Task] = Task.query.filter(Task.user_id == user.id).all()
    return jsonify({"data": [task.to_dict() for task in tasks]})
# #enddef table_tasks_list

# NOTE: maybe implement, not sure
# # @api.route("/tasks/open/list", methods=['GET'])
# # @jwt_required()
# # def tasks_open_list():
# #     current_user_uname  = get_jwt_identity()
# #     user: "User | None" = User.query.filter(User.uname == current_user_uname).first()

# #     if user is None:
# #         return jsonify({"status": False, "message": "User not found"}), 401
# #     # #endif

# #     tasks: list[Task] = Task.query.filter(
# #         Task.user_id == user.id,
# #         Task.status == TaskStatus.OPEN # type: ignore # NOTE: pylance cannot get the types properly
# #     ).all()

# #     return jsonify({"data": [task.to_dict() for task in tasks]})
# # # #enddef table_tasks_list

@api.route("/notes/list")
@jwt_required()
def notes_list():

    current_user_uname  = get_jwt_identity()
    user: "User | None" = User.query.filter(User.uname == current_user_uname).first()

    if user is None:
        return jsonify({"status": False, "message": "User not found"}), 401
    # #endif

    notes: list[Note] = Note.query.filter(Note.user_id == user.id).all()
    return jsonify({"data": [note.to_dict() for note in notes]})
# #enddef notes_list

@api.route("/login", methods=['POST'])
def login():

    data = request.get_json()
    user_or_tuple: "User | tuple" = User.login(
        email    = data.get("email"   , ""),
        password = data.get("password", "")
    )

    if (isinstance(user_or_tuple, tuple)):
        return jsonify({"status": False, "message": user_or_tuple[1]}), 401
    # #endif

    token: str = create_access_token(identity=user_or_tuple.uname)
    return jsonify({"status": True, "token": token}), 200
# #enddef login

@api.route("/register", methods=['POST'])
def register():

    data = request.get_json()
    user_or_tuple: "User | tuple" = User.register(**data)

    if isinstance(user_or_tuple, tuple):
        return jsonify({"status": user_or_tuple[0], "message": user_or_tuple[1]}), 401
    # #endif

    token: str = create_access_token(identity=user_or_tuple.uname)
    return jsonify({"status": True, "token": token}), 200
# #enddef login
