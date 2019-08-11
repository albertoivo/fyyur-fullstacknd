# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #

import dateutil.parser
import babel
import crud
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from models import Artist, Show, Venue
from flask_migrate import Migrate
from config import Config


# ---------------------------------------------------------------------------- #
# App Config.
# ---------------------------------------------------------------------------- #

APPLICATION_NAME = "app.py"

app = Flask(__name__)
app.config.from_object(Config)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ---------------------------------------------------------------------------- #
# Filters.
# ---------------------------------------------------------------------------- #


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ---------------------------------------------------------------------------- #
# Controllers.
# ---------------------------------------------------------------------------- #

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = crud.get_all_venues()
    data = {"": [v.local for v in venues]}
    for d in data[""]:
        d["venues"] = [
            v.serialize for v in venues if v.city == d["city"] and v.state == d["state"]
        ]

    return render_template('pages/venues.html', areas=data[""])


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search = request.form.get('search_term', '')
    venues = crud.get_venue_by_partial_name(search)
    response = {"count": len(venues)}

    response["data"] = [
        venue.search for venue in venues
    ]

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = crud.get_venue_by_id(venue_id)
    data = {"": venue.complete}

    return render_template('pages/show_venue.html', venue=data[""])

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)

    try:
        new_venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website=form.website.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data
        )

        crud.create_venue(new_venue)

        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except ValueError:  # FIXME melhorar essa exception

        flash('An error occurred. Venue ' + form.name + ' could not be listed.')

    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = crud.get_all_artists()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term', '')
    artists = crud.get_artist_by_partial_name(search)
    response = {"count": len(artists)}

    response["data"] = [
        artist.search for artist in artists
    ]

    return render_template('pages/search_artists.html', results=response, search_term=search)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = crud.get_artist_by_id(artist_id)
    data = {"": artist.complete}

    return render_template('pages/show_artist.html', artist=data[""])

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm(request.form)
    artist = crud.get_artist_by_id(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    form = ArtistForm(request.form)

    try:
        new_artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website=form.website.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data
        )

        crud.create_artist(new_artist)

        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    except ValueError:  # FIXME melhorar essa exception

        flash('An error occurred. Artist ' + form.name + ' could not be listed.')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows = crud.get_all_shows()
    for show in shows:
        venue = crud.get_venue_by_id(show.venue_id)
        artist = crud.get_artist_by_id(show.artist_id)
        data.extend([{
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        }])

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    try:
        new_show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )

        crud.create_show(new_show)

        flash('Show was successfully listed!')

    except ValueError:  # FIXME melhorar essa exception

        flash('An error occurred. Show could not be listed.')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ---------------------------------------------------------------------------- #
# Launch.
# ---------------------------------------------------------------------------- #

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
