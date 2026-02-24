
#################
# CORE HANDLERS #
#################
from flask_login import current_user, AnonymousUserMixin
from flask_mail import Message
from core.configs import *
from core.system import mail

def get_class_repr(classobject: typing.Any, description: str):
    return f"<{classobject.__name__} {description}>"
# #enddef get_class_repr

# NOTE: fix this function
def logged_user():
    return current_user if current_user is not isinstance(current_user, AnonymousUserMixin) else None
# #enddef getLoggedUser

def send_mail(
    subject: str,
    sender: str,
    recipients: "str | list[str | tuple[str, str]]",
    text_body: str,
    html_body: str,
    attachments: typing.Any = None
) -> "typing.Any":

    if isinstance(recipients, str):
        recipients = [recipients]
    # #endif

    message = Message(subject, sender=sender, recipients=recipients)

    message.body = text_body
    message.html = html_body

    if attachments is not None:
        message.attachments = attachments
    # #endif

    if (mail is not None):
        return mail.send(message)
    # #endif
# #enddef send_mail
