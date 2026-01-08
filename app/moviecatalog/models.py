
from ._common import *

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

class Person(BaseModel):

    __tablename__ = "person"
    _classname = "Person"

    name = db.Column(db.String(255),    unique=False, nullable=False, info={ "classname": _classname, "label": "Nome"   , "description": "" })
    surname = db.Column(db.String(255), unique=False, nullable=False, info={ "classname": _classname, "label": "Cognome", "description": "" })

    # person type (actor, director, writer, ecc...)
    person_type_id = db.Column(db.Integer, db.ForeignKey('person_type.id'), nullable=False)
    person_type = db.relationship('PersonType', backref=db.backref('peoples', lazy=True))

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('movies', lazy=True))
# #endclass

class PersonType(BaseModel):

    __tablename__ = "person_type"

    code = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
# #endclass

class Movie(BaseModel):

    __tablename__ = "movie"

    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    # @property
    # def authors(self):
    #     return Author.query.filter(Author.movie_id == self.id).all()
# #endclass

class MoviePersons(BaseModel):

    __tablename__ = "movie_persons_reference"

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('movie_persons', lazy=True))

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    person = db.relationship('Person', backref=db.backref('movie_persons', lazy=True))

    person_type_id = db.Column(db.Integer, db.ForeignKey('person_type.id'), nullable=False)
    person_type = db.relationship('PersonType', backref=db.backref('movie_persons', lazy=True))
# #endclass