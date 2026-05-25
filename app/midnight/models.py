
from ._common import *
from core.models.base import *

class Task(BaseModel):

    __tablename__ = "task"

    title       = db.Column(db.String(255)     , unique=True , nullable=False)
    description = db.Column(db.Text            , unique=False, nullable=False)

    from_date   = db.Column(db.DateTime        , nullable=True)
    to_date     = db.Column(db.DateTime        , nullable=True)

    user_id     = db.Column(db.Integer         , db.ForeignKey('users.id') , nullable=False)
    user        = db.relationship('User'       , backref=db.backref('tasks', lazy=True))

    status      = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.OPEN)

    @classmethod
    def open(
        cls,
        title       : "str",
        user_id     : "int",
        description : "str"                      = "",
        from_date   : "datetime.datetime | None" = None,
        to_date     : "datetime.datetime | None" = None,
        _save       : "bool"                     = False
    ) -> "Task":

        task: Task = cls(
            title       = title,
            user_id     = user_id,
            description = description,
            from_date   = from_date,
            to_date     = to_date
        )

        task.status = TaskStatus.OPEN

        if _save:
            task.save()
        # #endif

        return task
    # #enddef new

    def close(self) -> tuple:
        self.status = TaskStatus.CLOSED
        return self.save()
    # #enddef close
# #endclass

class Note(BaseModel):

    __tablename__ = "note"

    title   = db.Column(db.String(255), nullable=False)
    text    = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user    = db.relationship('User', backref=db.backref('notes', lazy=True))

# #endclass Note