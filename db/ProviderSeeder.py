from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Provider

from sk_env import db_url

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def create_providers():
    session.add_all([Provider("ugz_intern"), Provider("innet"), Provider("meteoblue")])
    session.commit()


def delete_records():
    session.query(Provider).delete()
    session.commit()
