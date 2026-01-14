
# flask imports
from flask import Blueprint, redirect, url_for
from flask import render_template, send_from_directory

from typing import Any

# other imports
import os
from json import *
import typing

# core imports
from core.configs import config
from core.handlers.handlers import *
from core.models import User
from core.web.handlers import *
import typing

config.read("application.cfg")

class Action:

    _title: str
    _type: str
    _url: str
    _icon: str

    _template: str

    def __init__(
            self,
            title: str               = "",
            action_type: typing.Any = None,
            url: str                = "#",
            icon: typing.Any        = None,

            _template: str = "action.html"
        ) -> "Action":

        self._title = title
        self._type = action_type
        self._url = url
        self._icon = icon
    # #enddef __init__

    def render(self):
        return render_template(
            self._template,
            title = self._title,
            type = self._type,
            url  = self._url,
            icon = self._url
        )
    # #enddef render
# #endclass

class Section:
    _actions: list[Action]

    _title: str
    _subtitle: str
    _fullscreen: bool

    _template: str
    _section_html: str

    _type: SectionTypeEnum
    _attributes: dict

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",

        _template: str = "section.html",
        _fullscreen: bool = False
    ) -> "Section":

        self._title = title
        self._subtitle = subtitle

        self._actions = []

        self._template = _template
        self._fullscreen = _fullscreen
    # #enddef __init__

    def table(
        self,
        url: str
    ) -> "Section":

        self._type = SectionTypeEnum.TABLE
        self._attributes = {"url": url}

        self._section_html = render_template(
            "sections/table.html",
            url=url
        )

        return self
    # #enddef table

    def form(
        self,
        formtype: typing.Any,
        object: typing.Any,
        formsave: typing.Callable = None,
        redir: str = None
    ) -> "Section":

        self._type = SectionTypeEnum.FORM

        form = formtype(obj = object)

        if (form.validate_on_submit()):

            if (formsave != None):
                formsave(form, object)
            else:
                form.saveForm(object)
            # #endif

            return redirect(url_for(redir))
        # #endif

        self._section_html = render_template(
            "sections/form.html",
            form=form,
            redirect=redirect
        )

        return self
    # #enddef form

    def addAction(self, action):
        if isinstance(action, Action):
            self._actions.append(action)
        else:
            raise TypeError("action must be an instance of Action")
        #endif
    # #enddef addAction

    def addActions(self, actions):
        for action in actions:
            if isinstance(action, Action):
                self.addAction(action)
            else:
                raise TypeError("action must be an instance of Action")
            #endif
        #endfor
    # #enddef addActions

    def render(self):
        return render_template(
            self._template,
            section_html=self._section_html,
            title=self._title,
            subtitle=self._subtitle,
            actions=[action.html() for action in self._actions]
        )
    # #enddef render
# #endclass

class Card:

    # all the sections of the card
    _sections: list[Section]

    # card attributes
    _title: str
    _subtitle: str

    def __init__(
            self,
            title: str = "",
            subtitle: str = "",
            sections: list[Section] = [],

            _template: str = "card.html"
        ) -> "Card":

        self._title = title
        self._subtitle = subtitle

        self._template = _template

        if isinstance(sections, Section):
            self._sections = [sections]
        elif isinstance(sections, list):
            self._sections = sections
        # #endif
    # #enddef __init__

    def addSection(self, section: Section):
        if isinstance(section, Section):
            self._sections.append(section)
        else:
            raise TypeError("section must be an instance of Section")
        # #endif
    # #enddef addSection

    def addSections(self, sections: list[Section]):
        for section in sections:
            if isinstance(section, Section):
                self.addSection(section)
            else:
                raise TypeError("section must be an instance of Section")
            # #endif
        # #endfor
    # #enddef addSections

    def render(self):
        return render_template(
            self._template,
            title=self._title,
            subtitle=self._subtitle,
            sections=[section.render() for section in self._sections]
        )
    # #enddef render
# #endclass

class Page:

    # all the cards of the page
    _cards: list[Card]

    # page title
    _title: str
    _page_title: str
    _subtitle: str

    # template items
    _template: str
    _icon: str

    # FIXME: temporary
    _logged_user: User

    def __init__(
            self,
            page_title: str = "",
            title: str = "",
            subtitle: str = "",
            cards: list[Card] = [],

            _icon: Any = "/icons/cardinal/favicon.ico",
            _template: str = "index.html",
            _sections: list[Section] = [],
        ) -> "Page":

        self._page_title = page_title
        self._title = title
        self._subtitle = subtitle

        # template & and icon settings
        self._icon = _icon
        self._template = _template

        if isinstance(cards, Card):
            self._cards = [cards]
        elif isinstance(cards, list):
            self._cards = cards
        # #endif

        if isinstance(_sections, Section):
            self._sections = [_sections]
        elif isinstance(_sections, list):
            self._sections = _sections
        # #endif

        self._logged_user = getLoggedUser()
    # #enddef __init__

    def addCard(self, card: Card):
        if isinstance(card, Card):
            self._cards.append(card)
        else:
            raise TypeError("card must be an instance of Card")
        # #endif
    # #enddef addCard

    def addCards(self, cards: list[Card]):
        for card in cards:
            if isinstance(card, Card):
                self.addCard(card)
            else:
                raise TypeError("card must be an instance of Card")
            # #endif
        # #endfor
    # #enddef addCards

    def render(self):
        return render_template(
            self._template,
            icon             = self._icon,
            website_title    = self._page_title,
            page_title       = self._title,
            logged_user      = self._logged_user,
            cards            = [card.render() for card in self._cards],
            menu_items       = [],
            cardinal_version = config.get("Cardinal", "version")
        )
    # #enddef render
# #endclass


# from flask import Blueprint, redirect, url_for
# from flask import render_template, send_from_directory

# import os
# import configparser

# config = configparser.ConfigParser()
# config.read("application.cfg")

# class Page:

#     _cards = []

#     _title = ""
#     _page_title = ""
#     _subtitle = ""

#     _template = "index.html"
#     _icon = "/icons/cardinal/favicon.ico"

#     _logged_user = ""

#     def __init__(self, page_title="", title="", subtitle="", icon=None, template=None):
#         self._page_title = page_title
#         self._title = title
#         self._subtitle = subtitle
#         self._template = template if template is not None else self._template
#         self._icon = icon if icon is not None else self._icon
#         self._logged_user = "Not logged in"
#     #enddef

#     def addCard(self, card):
#         if isinstance(card, Card):
#             self._cards.append(card)
#         else:
#             raise TypeError("card must be an instance of Card")
#         #endif
#     #enddef

#     def render(self):
#         return render_template(
#             self._template,
#             icon=self._icon,
#             website_title=self._page_title,
#             page_title=self._title,
#             logged_user=self._logged_user,
#             # cards=[card.html() for card in self._cards],
#             cardinal_version=config.get("Cardinal", "version")
#         )
#     #enddef
# #endclass

# class Card:

#     _title: str = ""
#     _subtitle: str = ""
#     _sections: list[Section] = []

#     _template = "card.html"

#     def __init__(self, title="", subtitle=""):
#         self._title = title
#         self._subtitle = subtitle
#     #enddef

#     def addSection(self, section):
#         if isinstance(section, Section):
#             self._sections.append(section)
#         else:
#             raise TypeError("section must be an instance of Section")
#         #endif
#     #enddef

#     def html(self):
#         return render_template(
#             self._template,
#             self._title,
#             self._subtitle,
#             sections=[section.html() for section in self._sections]
#         )
#     #enddef
# #endclass

# class Section:
#     _actions = []

#     _title = None
#     _subtitle = None
#     _fullscreen = False

#     _template = "section.html"

#     _section_html = ""

#     def __init__(self, fullscreen: bool = False):
#         self._fullscreen = fullscreen
#     #enddef

#     def table(self, url: str):

#         code = """
#         <table id="table" class="display">
#         </table>

#         <script>
#             $(document).ready(function () {
#                 $('#table').DataTable({
#                     ajax: "{{ url }}"
#                 })
#             })
#         </script>
#         """
#         self._section_html = "<h1>Test</h1>"
#     #enddef

#     def grid(self):
#         pass
#     #enddef

#     def form(self):
#         pass
#     #enddef

#     def initialPage( console: bool = False, logs: bool = False,  applications: bool = False, users: bool = False) -> None:
#         pass
#     #enddef

#     def addAction(self, action):
#         if isinstance(action, Action):
#             self._actions.append(action)
#         else:
#             raise TypeError("action must be an instance of Action")
#         #endif
#     #enddef

#     def getActions(self):
#         return self._actions
#     #enddef

#     def html(self):
#         return render_template(
#             self._template,
#             section_html=self.section_html,
#             title=self._title,
#             subtitle=self._subtitle,
#             actions=[action.html() for action in self._actions]
#         )
#     #enddef
# #endclass

# class Action:
#     _name = None
#     _type = None
#     _url = None
#     _icon = None

#     def __init__(self, name, action_type, url, icon=None):
#         self._name = name
#         self._type = action_type
#         self._url = url
#         self._icon = icon
#     #enddef

#     def getName(self):
#         return self._name
#     #enddef

#     def getType(self):
#         return self._type
#     #enddef

#     def getUrl(self):
#         return self._url
#     #enddef

#     def getIcon(self):
#         return self._icon
#     #enddef
# #endclass