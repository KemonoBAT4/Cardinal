
#################
# CORE HANDLERS #
#################
from flask_login import current_user, AnonymousUserMixin


def get_class_repr(classobject, object):
    return f"<{classobject.__name__} {object.id}>"
# #enddef get_class_repr

# NOTE: fix this function
def logged_user():
    return current_user if current_user is not isinstance(current_user, AnonymousUserMixin) else None
# #enddef getLoggedUser