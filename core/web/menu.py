
class MenuItem:

    _name = None
    _url = None
    _icon = None

    def __init__(self, name: str, url: str, icon: str = None):
        name = name.upper()

        self._name = name
        self._url = url
        self._icon = icon
    #enddef

    def getName(self):
        return self._name
    #enddef

    def getUrl(self):
        return self._url
    #enddef

    def getIcon(self):
        return self._icon
    #enddef

    def setName(self, name: str):
        self._name = name
    #enddef

    def setUrl(self, url: str):
        self._url = url
    #enddef

    def setIcon(self, icon: str):
        self._icon = icon
    #enddef

    def render(self):
        html = ""

        return html
    #enddef
#endclass

class Menu:

    _children = []

    def __init__(self):
        pass
    #enddef

    def addMenuItem(self, item: MenuItem):
        """
        #### DESCRIPTION:
        Adds a menu item to the menu

        #### PARAMTERES:
        - item: MenuItem -> The menu item to add

        #### RETURN:
        - no return
        """
        if not isinstance(item, MenuItem):
            raise TypeError(f"item must be an instance of {MenuItem.__name__}")
        #endif

        self._children.append(item)
    #enddef

    def getMenuItems(self):
        """
        DESCRIPTION:
        Returns the menu items

        PARAMETERS:
        - no parameters required

        RETURN:
        - list -> The menu items
        """
        return self._children
    #enddef

    def render(self):
        """
        DESCRIPTION:
        Renders the menu

        PARAMETERS:
        - no parameters required

        RETURN:
        - str -> The rendered menu html
        """
        html = ""

        for child in self._children:
            # html += child.render()
            pass
        #endfor

        return html
    #enddef
#endclass
