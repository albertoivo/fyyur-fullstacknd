from models import db, Artist


def create_artist(new_artist):
    db.session.add(new_artist)
    db.session.commit()


def get_all_artists():
    return Artist.query.all()