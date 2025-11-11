from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

import os
import configparser

config = configparser.ConfigParser()
config.read("application.cfg")

class Page:

    _cards = []

    _title = ""
    _page_title = ""
    _subtitle = ""

    _template = "index.html"
    _icon = "/icons/cardinal/favicon.ico"

    _logged_user = ""

    def __init__(self, page_title="", title="", subtitle="", icon=None, template=None):
        self._page_title = page_title
        self._title = title
        self._subtitle = subtitle
        self._template = template if template is not None else self._template
        self._icon = icon if icon is not None else self._icon
        self._logged_user = "Not logged in"
    #enddef

    def addCard(self, card):
        if isinstance(card, Card):
            self._cards.append(card)
        else:
            raise TypeError("card must be an instance of Card")
        #endif
    #enddef

    def render(self):
        return render_template(
            self._template,
            icon=self._icon,
            website_title=self._page_title,
            page_title=self._title,
            logged_user=self._logged_user,
            # cards=[card.html() for card in self._cards],
            cardinal_version=config.get("Cardinal", "version")
        )
    #enddef
#endclass

class Card:

    _title = ""
    _subtitle = ""
    _sections = []

    _template = "card.html"

    def __init__(self, title="", subtitle=""):
        self._title = title
        self._subtitle = subtitle
    #enddef

    def addSection(self, section):
        if isinstance(section, Section):
            self._sections.append(section)
        else:
            raise TypeError("section must be an instance of Section")
        #endif
    #enddef

    def html(self):
        return render_template(
            self._template,
            self._title,
            self._subtitle,
            sections=[section.html() for section in self._sections]
        )
    #enddef
#endclass

class Section:
    _actions = []

    _title = None
    _subtitle = None
    _fullscreen = False

    _template = "section.html"

    def __init__(self, fullscreen: bool = False):
        self._fullscreen = fullscreen
    #enddef

    def table(self):
        pass
    #enddef

    def grid(self):
        pass
    #enddef

    def form(self):
        pass
    #enddef

    def initialPage( console: bool = False, logs: bool = False,  applications: bool = False, users: bool = False) -> None:
        pass
    #enddef

    def addAction(self, action):
        if isinstance(action, Action):
            self._actions.append(action)
        else:
            raise TypeError("action must be an instance of Action")
        #endif
    #enddef

    def getActions(self):
        return self._actions
    #enddef

    def html(self):
        return render_template(
            self._template,
            self._title,
            self._subtitle,
            actions=[action.html() for action in self._actions]
        )
    #enddef
#endclass

class Action:
    _name = None
    _type = None
    _url = None
    _icon = None

    def __init__(self, name, action_type, url, icon=None):
        self._name = name
        self._type = action_type
        self._url = url
        self._icon = icon
    #enddef

    def getName(self):
        return self._name
    #enddef

    def getType(self):
        return self._type
    #enddef

    def getUrl(self):
        return self._url
    #enddef

    def getIcon(self):
        return self._icon
    #enddef
#endclass