
class CardinalException(Exception):
    """
    A custom exception for Cardinal
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
    # #enddef __init__

    def __str__(self):
        return f"CardinalException: {self.message}"
    # #enddef __str__

    def __repr__(self):
        return f"CardinalException(message='{self.message}')"
    # #enddef __repr__
# #endclass CardinalException
