
from ._common import *

# NOTE: this class is not yet implemented
# TODO: implement this class
# the class should create a grid of items
class CardinalGrid:

    _items_list: "list[dict[str, str | typing.Any ]]"

    def __init__(
        self,
        title: "str | None" = None,
        items_list: "list[dict[str, str | typing.Any ]]" = []
    ) -> "None":
        """
        #### DESCRIPTION:
        Creates a grid with the given title and items

        #### PARAMETERS:
        - title: str | None -> the title of the grid
        - items_list: list[dict[str, str | typing.Any]] -> the list of items to add in the grid

        #### RETURNS:
        - no return
        """

        if not isinstance(title, str):
            raise CardinalException(message = f"Title must be a type of {type(str)}, not {type(items_list)}")
        # #endif

        if not isinstance(items_list, list):
            raise CardinalException(message = f"Items list must be a type of {type(list)}, not {type(items_list)}")
        # #endif

        self._items_list = items_list
    # #enddef __init__

    #region -------- METHODS -------- #
    def add_item(self, item: "dict[str, str | typing.Any]") -> "None":
        """
        #### DESCRIPTION:
        Adds an item to the grid

        #### PARAMETERS:
        - item: dict[str, str | typing.Any] -> the item to add in the grid

        #### RETURNS:
        - no return
        """

        if not isinstance(item, dict):
            raise CardinalException(message = f"Item must be a type of {type(dict)}, not {type(item)}")
        # #endif

        self._items_list.append(item)
    # #enddef add_item

    def add_items(self, items_list: "list[dict[str, str | typing.Any]]") -> "None":
        """
        #### DESCRIPTION:
        Adds multiple items to the grid

        #### PARAMETERS:
        - items_list: list[dict[str, str | typing.Any]] -> the list of items to add in the grid

        #### RETURNS:
        - no return
        """

        if not isinstance(items_list, list):
            raise CardinalException(message = f"Items list must be a type of {type(list)}, not {type(items_list)}")
        # #endif

        _items_list_length : int = len(self._items_list)
        _items_length      : int = len(items_list)

        # NOTE: this is not the best way to append items, since there is the function (extends)
        # but this will avoid any errors thanks to the type checking of the 2 functions
        for item in items_list:
            self.add_item(item=item)
        # #endfor

        # NOTE: idk if this is useful
        if ((_items_list_length + _items_length) != len(self._items_list)):
            raise CardinalException(message = f"An error occured while adding items to the grid, only added {(len(self._items_list) - _items_list_length)} new items instead of {_items_length}")
        # #endif
    # #enddef add_items
    #endregion ----- METHODS -------- #

    #region -------- PROPERTIES -------- #
    @property
    def items(self) -> "list[dict[str, str | typing.Any]]":
        return self._items_list
    # #enddef items
    #endregion ----- PROPERTIES -------- #

    def __cardinal__(self) -> "str":
        """
        #### DESCRIPTION:
        Renders the grid

        #### PARAMETERS:
        - no parameters

        #### RETURNS:
        - str
        """
        return ""
    # #enddef __cardinal__
# #endclass CardinalGrid
