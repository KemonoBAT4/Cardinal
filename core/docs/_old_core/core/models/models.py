

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from .base import BaseModel, _BaseUser, db

class User(_BaseUser):

    _classname = "User"
    __tablename__ = "users"

    is_active = db.Column(db.Boolean, default=True)
#endclass

class Role(BaseModel):

    _classname = "Role"
    __tablename__ = "roles"

    code = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
#endclass

class Application(BaseModel):

    _classname = "Application"
    __tablename__ = "applications"

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
#endclass