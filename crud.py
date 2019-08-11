from models import db, Artist, Venue, Show


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


def create_show(new_show):
    db.session.add(new_show)
    db.session.commit()


def get_all_shows():
    return Show.query.all()