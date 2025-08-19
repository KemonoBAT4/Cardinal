from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    """
    DESCRIPTION:
    Base model class for all database models in the application.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    class Result:

        status = False
        message = ""

        def __init__(self, status, message):
            self.status = status
            self.message = message
        #enddef

        def __repr__(self) -> tuple:
            return self.status, self.message
        #enddef
    #endclass

    def save(self) -> tuple:
        """
        DESCRIPTION:
        Saves the model instance to the database.

        PARAMETERS:
        - no parameters required

        RETURN:
        - no return
        """

        response = self.Result(True, "Object saved successfully")

        try:
            if self.id is None:
                self.created_at = db.func.current_timestamp()
                self.updated_at = db.func.current_timestamp()
            else:
                self.updated_at = db.func.current_timestamp()
            #endif

            db.session.add(self)
            db.session.commit()

            return response
        except Exception as e:
            db.session.rollback()

            response.status = False
            response.message = f"Error while saving object: {str(e)}"

            return response
        #endtry
    #enddef

    def delete(self) -> tuple:
        """
        DESCRIPTION:
        Deletes the model instance from the database.

        PARAMETERS:
        - no parameters required

        RETURN:
        - no return
        """

        response = self.Result(True, "Object deleted successfully")

        try:
            if self.id != None:
                db.session.query(self.__class__).filter_by(id=self.id).delete(synchronize_session=False)
            else:
                response.status = False
                response.message = "Object ID is None, cannot delete"
            #endif
        except Exception as e:
            db.session.rollback()

            response.status = False
            response.message = (f"Error while deleting object: {str(e)}")
        #endtry
        db.session.commit()

        return response
    #enddef

    def update(self, object: any) -> tuple:
        """
        DESCRIPTION:
        Updates the model instance with the new object's values without changing the id.

        PARAMETERS:
        - object (any): The object to update the model instance with (must be of the same type).

        RETURN:
        - dict: A dictionary containing the status and message.
        """

        response = self.Result(True, "Object updated successfully")

        if not isinstance(object, self.__class__):
            response.status = False
            response.message = "Object type mismatch"
            return response
        #endif

        try:
            for attr in dir(object):
                if not attr.startswith('_') and attr not in ['id', 'creation_date']:
                    setattr(self, attr, getattr(object, attr))
                #endif
            #endfor

            status, message = self.save()

            if status == False:
                response.status = False
                response.message = message
            #endif

        except Exception as e:
            response.status = False
            response.message = f'Error: {str(e)}'
        #endtry

        return response
    #enddef

    def to_dict(self) -> dict:
        """
        DESCRIPTION:
        Converts the model instance to a dictionary representation.

        PARAMETERS:
        - no parameters required

        RETURN:
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
            #endif
        #endfor

        return result
    #enddef

    def __repr__(self) -> str:
        return f"<{self._class__.__name__} {self.id}>"
    #enddef
#endclass
