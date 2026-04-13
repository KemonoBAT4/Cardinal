
from ._common import *
from core.models.base import BaseModel, db, BaseUser

class Movie(BaseModel):

    __tablename__ = "movie"

    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)

    movie_file_name = db.Column(db.String(255), unique=False, nullable=True)

    # TODO: OTHER DATA TO STORE (implement)
# #endclass
