from models import db, Artist, Venue, Show
import datetime


def create_artist(new_artist):
    db.session.add(new_artist)
    db.session.commit()


def edit_artist(id, name, city, state, phone, genres, facebook_link, image_link, website, seeking_venue, seeking_description):
    artist = get_artist_by_id(id)

    artist.city = city
    artist.seeking_description = seeking_description
    artist.seeking_venue = seeking_venue
    artist.phone = phone
    artist.state = state
    artist.name = name
    artist.genres = genres
    artist.facebook_link = facebook_link
    artist.website = website
    artist.image_link = image_link

    db.session.commit()


def delete_artist(id):
    artist = get_artist_by_id(id)
    db.session.delete(artist)
    db.session.commit()


def get_all_artists():
    return Artist.query.all()


def get_artist_by_id(id):
    return Artist.query.filter_by(id=id).first_or_404()


def get_artist_by_partial_name(search):
    return Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()


def get_past_artist_shows(artist_id):
    return db.session.query(Show).filter(Show.start_time < datetime.datetime.now(), Show.artist_id == artist_id).all()


def get_upcoming_artist_shows(artist_id):
    return db.session.query(Show).filter(Show.start_time > datetime.datetime.now(), Show.artist_id == artist_id).all()


def create_venue(new_venue):
    db.session.add(new_venue)
    db.session.commit()


def edit_venue(id, name, genres, address, city, state, phone, facebook_link, website, image_link, seeking_talent, seeking_description):
    venue = get_venue_by_id(id)

    venue.name = name
    venue.genres = genres
    venue.address = address
    venue.city = city
    venue.phone = phone
    venue.state = state
    venue.facebook_link = facebook_link
    venue.image_link = image_link
    venue.website = website
    venue.seeking_talent = seeking_talent
    venue.seeking_description = seeking_description

    db.session.commit()


def delete_venue(id):
    venue = get_venue_by_id(id)
    db.session.delete(venue)
    db.session.commit()


def get_all_venues():
    return Venue.query.all()


def get_venue_by_id(id):
    return Venue.query.filter_by(id=id).first_or_404()


def get_venue_by_city(city):
    return Venue.query.filter_by(city=city).all()


def get_venues_locals():
    return Venue.query.distinct(Venue.city, Venue.state).all()


def get_venue_by_partial_name(search):
    return Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()


def create_show(new_show):
    db.session.add(new_show)
    db.session.commit()


def get_all_shows():
    return Show.query.order_by(Show.start_time.desc()).all()


def get_shows_by_venue_id(venue_id):
    return Show.query.filter_by(venue_id=venue_id).all()


def get_shows_by_artist_id(artist_id):
    return Show.query.filter_by(venue_id=artist_id).all()


def get_past_shows_at_venue(venue_id):
    return db.session.query(Show).filter(Show.start_time < datetime.datetime.now(), Show.venue_id == venue_id).all()


def get_upcoming_shows_at_venue(venue_id):
    return db.session.query(Show).filter(Show.start_time > datetime.datetime.now(), Show.venue_id == venue_id).all()
