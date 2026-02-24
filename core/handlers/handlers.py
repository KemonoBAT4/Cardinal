
#################
# CORE HANDLERS #
#################
from flask_login import current_user, AnonymousUserMixin
from flask_mail import Message
from core.configs import *

def get_class_repr(classobject, object):
    return f"<{classobject.__name__} {object.id}>"
# #enddef get_class_repr

# NOTE: fix this function
def logged_user():
    return current_user if current_user is not isinstance(current_user, AnonymousUserMixin) else None
# #enddef getLoggedUser

def send_mail(
    subject,
    sender,
    recipients,
    text_body,
    html_body,
    attachments=None
) -> "typing.Any":

    message = Message(subject, sender=sender, recipients=recipients)

    message.body = text_body
    message.html = html_body
    message.attachments = attachments

    return mail.send(message)

# #enddef send_mail