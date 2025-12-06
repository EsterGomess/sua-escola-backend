from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship, declared_attr

from backend.models import Base

class User(Base):
    __abstract__ = True

    created_at= Column(DateTime, default=datetime.now())
    updated_at= Column(DateTime, default=datetime.now())

    @declared_attr
    def name(cls):
        return Column(String(100), nullable=False)

    @declared_attr
    def surname(cls):
        return Column(String(100), nullable=False)

    @declared_attr
    def address_id(cls):
        return Column(Integer, ForeignKey("address.id"))

    @declared_attr
    def address(cls):
        return relationship("Address")

    @declared_attr
    def contact_id(cls):
        return Column(Integer, ForeignKey("contact.id"))

    @declared_attr
    def contact(cls):
        return relationship("Contact")
