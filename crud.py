from models import db, Artist, Venue, Show
import datetime


def create_artist(new_artist):
    db.session.add(new_artist)
    db.session.commit()


def get_all_artists():
    return Artist.query.all()


def get_artist_by_id(id):
    return Artist.query.filter_by(id=id).first_or_404()


def get_artist_by_partial_name(search):
    return Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()


def create_venue(new_venue):
    db.session.add(new_venue)
    db.session.commit()


def get_all_venues():
    return Venue.query.all()


def get_venue_by_id(id):
    return Venue.query.filter_by(id=id).first_or_404()


def get_venue_by_partial_name(search):
    return Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()


def create_show(new_show):
    db.session.add(new_show)
    db.session.commit()


def get_all_shows():
    return Show.query.all()


def get_shows_by_venue_id(venue_id):
    return Show.query.filter_by(venue_id=venue_id).all()


def get_shows_by_artist_id(artist_id):
    return Show.query.filter_by(venue_id=artist_id).all()


def get_past_shows_at_venue(venue_id):
    return db.session.query(Show).filter(Show.start_time < datetime.datetime.now(), Show.venue_id == venue_id).all()


def get_upcoming_shows_at_venue(venue_id):
    return db.session.query(Show).filter(Show.start_time > datetime.datetime.now(), Show.venue_id == venue_id).all()
