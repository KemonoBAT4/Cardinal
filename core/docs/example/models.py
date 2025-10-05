# /models.py

from core.models.base import BaseModel, db

# Creates all the models

# class Role(BaseModel):

#     _classname = "Role"
#     __tablename__ = "roles"

#     code = db.Column(db.String(80), unique=True, nullable=False)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(120), unique=True, nullable=False)
# #endclass