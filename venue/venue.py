from flask import Blueprint, render_template, request, flash, redirect, url_for

import crud
from forms import VenueForm
from models import Venue

venue = Blueprint('venue', __name__, template_folder='templates')


@venue.route('/venues')
def venues():
    data = [v.local for v in crud.get_venues_locals()]
    for d in data:
        d["venues"] = [
            v.serialize for v in crud.get_venue_by_local(d["city"], d["state"])
        ]

    return render_template('pages/venues.html', areas=data)


@venue.route('/venues/search', methods=['POST'])
def search_venues():
    search = request.form.get('search_term', '')
    venues = crud.get_venue_by_partial_name(search)
    response = {
        "count": len(venues),
        "data": [
            venue.search for venue in venues
        ]
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@venue.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = crud.get_venue_by_id(venue_id)
    data = {"": venue.complete}

    return render_template('pages/show_venue.html', venue=data[""])


#  Create Venue
#  ----------------------------------------------------------------


@venue.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@venue.route('/venues/create', methods=['POST'])
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

        Venue.create(new_venue)

        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except ValueError:  # FIXME melhorar essa exception

        flash('Error occurred. Venue ' + form.name + ' could not be listed.')

    return render_template('pages/home.html')


@venue.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it from the db then redirect
    # the user to the homepage

    try:
        venue = crud.get_venue_by_id(venue_id)
        Venue.delete(venue)
        flash('The venue has been removed together with all of its shows.')
        return render_template('pages/home.html')
    except ValueError:
        flash('It was not possible to delete this Venue')

    return None


@venue.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm(request.form)
    venue = crud.get_venue_by_id(venue_id)

    form.state.process_data(venue.state)
    form.genres.process_data(venue.genres)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@venue.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)

    try:

        crud.edit_venue(
            venue_id,
            form.name.data,
            form.genres.data,
            form.address.data,
            form.city.data,
            form.state.data,
            form.phone.data,
            form.facebook_link.data,
            form.website.data,
            form.image_link.data,
            form.seeking_talent.data,
            form.seeking_description.data
        )

        flash('Venue ' + form.name.data + ' was successfully edited!')

    except ValueError:  # FIXME melhorar essa exception

        flash(
            'An error occurred. Venue ' + form.name + ' could not be listed.')

    return redirect(url_for('venue.show_venue', venue_id=venue_id))
