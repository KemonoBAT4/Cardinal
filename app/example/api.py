
from flask import Blueprint

api = Blueprint('Example_api', __name__)

@api.route('/test')
def apiTest():
    return {"test": "test"}
    # page = Page(title="Home")
    # card = Card(title="Card 1")
    # section = Section().table(url="api_url")

    # card.addSection(section)
    # page.addCard(card)

    # return page.render()
#enddef