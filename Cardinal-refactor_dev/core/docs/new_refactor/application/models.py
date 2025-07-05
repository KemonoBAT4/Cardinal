
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from core.models.base import BaseModel, db
from .handlers import *


class undefined(BaseModel):
    pass
#endclass

