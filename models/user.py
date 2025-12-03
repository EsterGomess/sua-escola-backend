from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
import abc
from  model import Base


class User(Base, abc.ABC):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    address = Column(Integer, ForeignKey("adress.pk_adress"), nullable=False)
    contact = Column(Integer, ForeignKey("contact.pk_contact"), nullable=True)

    def get_full_name(self) -> str:
        return f"{self.name} {self.surname}"

    def get_address(self) -> Union[str, None]:
        return self.address.get_full_address()

    def get_contact(self) -> Union[str, None]:
        return self.contact.get_full_contact()