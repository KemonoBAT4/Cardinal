
from .base import *

class User(UserMixin, BaseModel):

    __tablename__ = "users"

    name            = db.Column(db.String(80) , nullable=False)
    surname         = db.Column(db.String(80) , nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.LargeBinary, nullable=False)

    @classmethod
    def register(cls, email: str, name: str, surname: str, password: str) -> "User | tuple":
        """
        #### DESCRIPTION:
        Adds a new user with the provided password.

        #### PARAMETERS:
        - email (str): The email address of the user.
        - name (str): The name of the user.
        - surname (str): The surname of the user.
        - password (str): The password to set for the user.

        #### RETURN:
        - tuple: A tuple containing the status and message of the operation.
        """

        found_user: "User | None" = User.query.filter(User.email == email).first()

        if (found_user is not None):
            return User.Result(False, "User already exists").result()
        # #endif

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user: "User" = User(
            name            = name,
            surname         = surname,
            email           = email,
            hashed_password = hashed_password
        )
        user.save()

        return user
    #enddef

    @classmethod
    def login(cls, email: str, password: str) -> "User | tuple":

        user: "User | None" = User.query.filter(User.email == email).first()

        if user is None:
            return cls.Result(False, "User not found").result()
        # #endif

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            return cls.Result(False, "Invalid password").result()
        # #endif
        return user
    #enddef

    def get_id(self):
        return str(self.uname)
    # #enddef

    def save(self) -> tuple:

        if (self.hashed_password is None):
            return self.Result(False, "Password is required").result()
        #endif

        return super().save()
    # #enddef save
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

class CardinalSystem(BaseModel):
    pass