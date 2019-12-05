# -------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------- #
import logging
import os
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from artist.artist import artist
from config import Config
from show.show import show
from venue.venue import venue

# -------------------------------------------------------------------------- #
# App Config.
# -------------------------------------------------------------------------- #

APPLICATION_NAME = "app.py"

app = Flask(__name__)
app.config.from_object(Config)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------------------------------------------------------------------------- #
# Blueprints register.
# -------------------------------------------------------------------------- #

app.register_blueprint(artist)
app.register_blueprint(venue)
app.register_blueprint(show)


# -------------------------------------------------------------------------- #
# Filters.
# -------------------------------------------------------------------------- #


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# -------------------------------------------------------------------------- #
# Controllers.
# -------------------------------------------------------------------------- #

@app.route('/')
def index():
    return render_template('pages/home.html')


# -------------------------------------------------------------------------- #
# Errors and Logs.
# -------------------------------------------------------------------------- #

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# -------------------------------------------------------------------------- #
# Launch.
# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
