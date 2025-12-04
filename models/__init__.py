import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from models.base import Base
from models.address import Address
from models.contact import Contact
from models.guardian import Guardian
from models.student import Student
from models.association import student_guardian
from models.user import User
db_path = "database/"

if not os.path.exists(db_path):
   os.makedirs(db_path)

db_url = 'sqlite:///%s/suaescola.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)


__all__ = [
    "engine",
    "Session",
    "Base",
    "Student",
    "Guardian",
    "Address",
    "Contact",
    "User",
    "student_guardian",
]


if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)