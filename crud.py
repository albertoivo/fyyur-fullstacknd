from models import db


def create_artist(new_artist):
    db.session.add(new_artist)
    db.session.commit()
