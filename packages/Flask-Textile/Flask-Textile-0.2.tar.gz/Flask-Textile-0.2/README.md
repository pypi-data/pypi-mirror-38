The [Python port](https://github.com/textile/python-textile) of Dean Allen's [humane web text generator](https://www.textile-lang.com) packaged for use with [Flask](http://flask.pocoo.org).

    pip install flask-textile

Import into your project:

    from flask_textile import Textile

And then...

    app = Flask(__name__)
    textile = Textile(app)

Or, if one prefers, with a factory:

    textile = Textile()
    ...
    textile.init_app(app)

Simple usage within a Jinja2 template:

    {{ text|textile }}

Or use as a filter:

    {% filter textile %}
    h2. Textile

    * is a _shorthand syntax_ used to generate valid HTML
    * is *easy* to read and *easy* to write
    * can generate complex pages, including: headings, quotes, lists, tables and figures

    Textile integrations are available for "a wide range platforms":/article/.
    {% endfilter %}
