

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from .base import BaseModel, db

# class User(BaseModel):

#     _classname = "User"
#     __tablename__ = "users"

#     name = db.Column(db.String(80), nullable=False)
#     surname = db.Column(db.String(80), nullable=False)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     is_active = db.Column(db.Boolean, default=True)
# #endclass

# class Role(BaseModel):

#     _classname = "Role"
#     __tablename__ = "roles"

#     code = db.Column(db.String(80), unique=True, nullable=False)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(120), unique=True, nullable=False)
# #endclass

# class UserRole(BaseModel):

#     _classname = "UserRole"
#     __tablename__ = "user_roles"

#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     user = relationship(User, backref=backref("user_roles", cascade="all, delete-orphan"))

#     role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
#     role = relationship(Role, backref=backref("user_roles", cascade="all, delete-orphan"))
# #endclass

# class Application(BaseModel):

#     _classname = "Application"
#     __tablename__ = "applications"

#     name = db.Column(db.String(255), unique=True, nullable=False)
#     description = db.Column(db.Text, unique=False, nullable=False)

#     blueprint_name = db.Column(db.String(255), nullable=False)
#     folder_path = db.Column(db.Text, nullable=False)
#     url_prefix = db.Column(db.String(255), nullable=False)

#     is_active = db.Column(db.Boolean, default=True, nullable=False)
# #endclass
