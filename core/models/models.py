from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from .base import BaseModel, BaseUser, db

class User(BaseUser):

    __tablename__ = "users"

    is_active = db.Column(db.Boolean, default=True)
#endclass

class Role(BaseModel):

    __tablename__ = "roles"

    code = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
#endclass

class Application(BaseModel):

    __tablename__ = "applications"

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
#endclass