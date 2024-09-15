from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Provider

from db.env import db_url

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def create_providers():
    session.add_all([Provider("ugz"), Provider("innet"), Provider("meteoblue")])
    session.commit()


def delete_records():
    session.query(Provider).delete()
    session.commit()
