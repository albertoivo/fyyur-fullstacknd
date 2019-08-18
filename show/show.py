from flask import Blueprint, render_template, request, flash

import crud
from forms import ShowForm
from models import Show

show = Blueprint('show', __name__, template_folder='templates')


@show.route('/shows')
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


@show.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@show.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    try:
        new_show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )

        Show.create(new_show)

        flash('Show was successfully listed!')

    except ValueError:  # FIXME melhorar essa exception

        flash('An error occurred. Show could not be listed.')

    return render_template('pages/home.html')
