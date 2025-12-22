

from wtforms import Form, StringField, PasswordField, validators, SubmitField

# local imports
from .handlers import *
from .models import *

# example form
class ExampleForm(Form):
    field1 = StringField('Field 1', [validators.DataRequired()])
    field2 = StringField('Field 2', [validators.DataRequired()])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
    #enddef

    def saveFom(self, form, obj, *args, **kwargs):
        pass
    #enddef
#endclass