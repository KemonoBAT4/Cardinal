
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

import os
import configparser

from core.models.base import db
from core.models.models import *

config = configparser.ConfigParser()
config.read("application.cfg")

class Page:

    sections = []

    website_title = ""
    title = None
    subtitle = None

    template = "index.html"
    icon = "/icons/cardinal/favicon.ico"

    def __init__( self, website_title="", title="", subtitle="", icon=None):

        self.title = title
        self.subtitle = subtitle
        self.website_title = website_title if website_title != "" else title
        self.icon = icon if icon is not None else self.icon
        self.logged_user = "Not logged in"  # This should be replaced with the actual logged-in user, e.g., current_user.username
    #enddef

    def card(self):
        pass
    #enddef

    def addSection(self, section):
        if isinstance(section, Section):
            self._sections.append(section)
        else:
            raise TypeError("section must be an instance of Section")
        #endif
    #enddef

    def render(self):
        return render_template(
            self.template,
            icon=self.icon,
            website_title=self.website_title,
            page_title=self.title,
            logged_user=self.logged_user,
            sections=[section.html() for section in self.sections],
            cardinal_version=config.get("Cardinal", "version")
        )
    #enddef
#endclass

class Section:

    _actions = []

    _title = None
    _subtitle = None

    html = None

    def __init__(self):
        pass
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
        return ""
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