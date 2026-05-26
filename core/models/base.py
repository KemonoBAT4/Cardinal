from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

import bcrypt
import typing

from core.handlers import get_class_repr
from core.configs import generate_uuid

db = SQLAlchemy()

class BaseModel(db.Model):
    """
    #### DESCRIPTION:
    Base model class for all database models in the application.
    """
    __abstract__ = True

    id         = db.Column(db.Integer    , primary_key = True , autoincrement = True )
    uname      = db.Column(db.String(255), unique      = True , nullable      = False)
    created_at = db.Column(db.DateTime   , unique      = False, nullable      = False)
    updated_at = db.Column(db.DateTime   , unique      = False, nullable      = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.uname = generate_uuid()
    # #enddef __init__

    class Result:

        status: bool = False
        message: str = ""

        def __init__(
            self,
            status: bool,
            message: str
        ) -> "None":
            super().__init__()

            self.status = status
            self.message = message
        # #enddef __init__

        def result(self) -> tuple:
            return self.status, self.message
        # #enddef result

        def __repr__(self) -> str:
            return get_class_repr( classobject = self.__class__, description = "None" )
        # #enddef __repr__
    # #endclass Result

    def save(self) -> tuple:
        """
        #### DESCRIPTION:
        Saves the model instance to the database.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - tuple: A tuple containing the status and message of the operation.
        """

        response = self.Result(True, "Object saved successfully")

        try:
            if self.id is None:
                self.created_at = db.func.current_timestamp()
                self.updated_at = db.func.current_timestamp()
            else:
                self.updated_at = db.func.current_timestamp()
            # #endif

            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()

            response.status = False
            response.message = f"Error while saving object: {str(e)}"
        # #endtry

        return response.result()
    # #enddef save

    def delete(self) -> tuple:
        """
        #### DESCRIPTION:
        Deletes the model instance from the database.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - tuple: A tuple containing the status and message of the operation.
        """

        response = self.Result(True, "Object deleted successfully")

        try:
            if self.id != None:
                db.session.query(self.__class__).filter_by(id=self.id).delete(synchronize_session=False)
            else:
                response.status = False
                response.message = "Object ID is None, cannot delete"
            # #endif
        except Exception as e:
            db.session.rollback()

            response.status = False
            response.message = (f"Error while deleting object: {str(e)}")
        # #endtry
        db.session.commit()

        return response.result()
    # #enddef delete

    def update(self, object: typing.Any) -> tuple:
        """
        #### DESCRIPTION:
        Updates the model instance with the new object's values without changing the id.

        #### PARAMETERS:
        - object (any): The object to update the model instance with (must be of the same type).

        #### RETURN:
        - dict: A dictionary containing the status and message.
        """

        response = self.Result(True, "Object updated successfully")

        if not isinstance(object, self.__class__):
            response.status = False
            response.message = "Object type mismatch"
            return response.result()
        # #endif

        try:
            for attr in dir(object):
                if not attr.startswith('_') and attr not in ['id', 'creation_date']:
                    setattr(self, attr, getattr(object, attr))
                # #endif
            # #endfor

            status, message = self.save()

            if status == False:
                response.status = False
                response.message = message
            # #endif

        except Exception as e:
            response.status = False
            response.message = f'Error: {str(e)}'
        # #endtry

        return response.result()
    # #enddef update

    def to_dict(self) -> dict:
        """
        #### DESCRIPTION:
        Converts the model instance to a dictionary representation.

        #### PARAMETERS:
        - no parameters required

        #### RETURN:
        - dict: A dictionary representation of the model instance.
        """
        result = { }

        # TODO: try it
        # for column in self.__table__.columns:
        #     if column.name not in self._methods_to_avoid:
        #         result[column.name] = getattr(self, column.name)
        # REFACTOR:

        for key, value in vars(self).items():
            if not callable(getattr(self, key)) and not key.startswith('_'):
                result[key] = value
            # #endif
        # #endfor

        return result
    # #enddef to_dict

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"
    # #enddef
# #endclass BaseModel