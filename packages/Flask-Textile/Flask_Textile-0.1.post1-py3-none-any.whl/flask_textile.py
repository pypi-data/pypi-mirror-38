from flask import Markup
from textile import textile as parser

def textile(text):
    return Markup(parser(text))

class Textile:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.filters.setdefault('textile', self.parse)

    def parse(self, text):
        return parser(text)
