
# flask imports
from flask import Blueprint, redirect, url_for          # type: ignore
from flask import render_template, send_from_directory  # type: ignore

# other imports
import os
import json
import typing
import importlib

# core imports
import core.system as system

from core.configs import *
from core.handlers.handlers import *
from core.models import User
from core.web.handlers import *

from core.web.widgets import *

config.read("application.cfg")

class Action:

    title: str
    type: str
    url: str
    icon: str

    def __init__(
        self,
        title: str              = "",
        action_type: typing.Any = None,
        url: str                = "#",
        icon: typing.Any        = None
    ) -> "None":
        self.title = title
        self.type  = action_type
        self.url   = url
        self.icon  = icon
    # #enddef __init__

    def render(self):
        return render_template(
            "action.html",
            action=self
        )
    # #enddef render
# #endclass

class Section:

    title: str
    subtitle: str
    fullscreen: bool

    template: "str | None"
    section_html: str

    _type: SectionTypeEnum
    context: dict

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
    ) -> "None":
        self.title = title
        self.subtitle = subtitle
        self.template = None
        self.context = {}
        self.requires_datatables = False
    # #enddef __init__

    def table(
        self,
        url     : "str",
        config  : "dict[str, typing.Any]",
        click   : "str | typing.Callable | None" = None,
        buttons : "dict | None" = None
    ) -> "Section":

        self._type = SectionTypeEnum.TABLE
        self.template = "sections/table.html"
        self.context = { "url": url }

        table = CardinalDataTable(
            url     = url,
            config  = config,
            click   = click,
            buttons = buttons
        )


        return self
    # #enddef table

    def form(
        self,
        form
        # formtype: typing.Any,
        # object: typing.Any,
        # formsave: "typing.Callable | None" = None,
        # redir: "str | None" = None
    ) -> "Section":
        self.template = "sections/form.html"
        self.context = {"form": form}

        # self._type = SectionTypeEnum.FORM

        # form = formtype(obj = object)

        # # NOTE: fix this function
        # # try to implement a funciton to save the form
        # if (form.validate_on_submit()):

        #     if (formsave != None):
        #         formsave(form, object)
        #     else:
        #         form.saveForm(object)
        #     # #endif

        #     # return redirect(url_for(redir))
        # # #endif

        # self._section_html = render_template(
        #     "sections/form.html",
        #     form=form,
        #     redirect=redirect
        # )

        return self
    # #enddef form

    def render(self) -> str:
        return render_template(
            "section.html",
            section=self
        )
    # #enddef render
# #endclass

class Card:

    # all the sections of the card
    sections: list[Section]

    # card attributes
    title: str
    subtitle: str

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        sections: "list[Section] | None" = None,
    ) -> "None":

        self.title = title
        self.subtitle = subtitle

        if isinstance(sections, NoneType):
            sections = []
        # #endif

        if isinstance(sections, Section):
            self.sections = [sections]
        elif isinstance(sections, list):
            self.sections = sections
        else:
            self.sections = []
        # #endif
    # #enddef __init__

    def addSection(self, section: Section):
        if isinstance(section, Section):
            self.sections.append(section)
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
            "card.html",
            card=self
        )
    # #enddef render
# #endclass

class Page:

    # all the cards of the page
    cards: list[Card]

    # page title
    title: str
    page_title: str
    subtitle: str

    # template items
    template: str
    icon: str

    # FIXME: temporary
    logged_user: User

    def __init__(
        self,
        page_title: str = "",
        title: str = "",
        subtitle: str = "",

        _icon: typing.Any = "/icons/cardinal/favicon.ico",
    ) -> "None":

        self.page_title = page_title
        self.title = title
        self.subtitle = subtitle

        self.cards = []
        self.icon = _icon
    # #enddef __init__

    def addCard(self, card: Card):
        if isinstance(card, Card):
            self.cards.append(card)
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

    def _get_menu_items(self):

        menu_items = []

        # with open(f'./../../app/{system.cardinal._name}/menu.json') as f:
        #     menu_items = json.load(f)
        # # #enddef

        # TODO: render the menu


        # with open(f'./../../app/{cardinal._name}menu.json') as f:
        #     menu_items = json.load(f)

        return []
    # #enddef _get_menu_items




    def render(self):
        return render_template(
            "index.html",
            page = self,
            logged_user = logged_user(),
            cardinal_version = config.get("Cardinal", "version"),
            menu_items = self._get_menu_items()
        )
    # #enddef render
# #endclass
