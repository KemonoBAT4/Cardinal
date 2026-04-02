
#################
# CORE HANDLERS #
#################
from flask_login import current_user, AnonymousUserMixin
from flask_mail import Message
from core.configs import *

def get_class_repr(classobject: typing.Any, description: str):
    return f"<{classobject.__name__} {description}>"
# #enddef get_class_repr

# NOTE: fix this function
def logged_user():
    # NOTE: the result on the html is "<flask_login.mixins.AnonymousUserMixin object at 0x000001E1FCC57550>" not something like "not logged in" or "AnonymousUser"
    return current_user if current_user is not isinstance(current_user, AnonymousUserMixin) and current_user.is_authenticated else "Not Logged In"
# #enddef getLoggedUser

