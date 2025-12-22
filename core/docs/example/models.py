
from core.models import *
from core.configs import *

class Example(BaseModel):

    __tablename__ = "examples"

    # string related fields
    string = db.Column(db.String(255), unique=False, nullable=True)
    text = db.Column(db.Text, unique=False, nullable=True)

    # numeric related fields
    integer = db.Column(db.Integer, unique=False, nullable=True)
    float = db.Column(db.Float, unique=False, nullable=True)

    # date related fields
    date = db.Column(db.Date, unique=False, nullable=True)
    datetime = db.Column(db.DateTime, unique=False, nullable=True)
    time = db.Column(db.Time, unique=False, nullable=True)

    # other fields
    boolean = db.Column(db.Boolean, unique=False, nullable=True)
    largebinary = db.Column(db.LargeBinary, unique=False, nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #enddef

    def normal_method(self, *args, **kwargs):
        pass
    #enddef

    @classmethod
    def class_method(cls, *args, **kwargs):
        pass
    #enddef
#endclass
