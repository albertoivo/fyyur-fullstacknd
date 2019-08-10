from models import db, Artist, Venue


def create_artist(new_artist):
    db.session.add(new_artist)
    db.session.commit()


def get_all_artists():
    return Artist.query.all()


def create_venue(new_venue):
    db.session.add(new_venue)
    db.session.commit()


def get_all_venues():
    return Venue.query.all()


def get_venue_by_id(id):
    return Venue.query.filter_by(id=id).first_or_404()
