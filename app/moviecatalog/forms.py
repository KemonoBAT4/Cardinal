

from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm                                                             # type: ignore

# local imports
from ._common import *
from .handlers import *
from .models import *

from core.form import *

# example form
class ExampleForm(FlaskForm):

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

class MovieForm(BaseForm):
    title       = StringField('Titolo',      [validators.DataRequired()], render_kw={"size": 6})
    description = StringField('Descrizione', [validators.DataRequired()], render_kw={"size": 6})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #enddef

    def saveForm(self, obj, *args, **kwargs):
        self.populate_obj(obj)
        obj.save()
    # #enddef
#endclass

