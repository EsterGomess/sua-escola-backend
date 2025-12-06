import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from backend.models.base import Base
from backend.models.address import Address
from backend.models.contact import Contact
from backend.models.guardian import Guardian
from backend.models.student import Student
from backend.models.association import student_guardian
from backend.models.user import User
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