

from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm

# local imports
from ._common import *
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


class MovieForm(FlaskForm):

    title = StringField('Title', [validators.DataRequired()])
    description = StringField('Description', [validators.DataRequired()])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #enddef

    def saveForm(self, obj, *args, **kwargs):

        breakpoint()

        self.populate_obj(obj)
        obj.save()
    #enddef


    # def saveFom(self, form, obj, *args, **kwargs):
    #     breakpoint()

    #     form.populate_obj(obj)
    #     obj.save()
    # #enddef
#endclass

