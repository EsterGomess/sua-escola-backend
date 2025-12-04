from sqlalchemy import Column, Integer,  String

from models import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    number = Column(String(20), nullable=True)
    district = Column(String(50), nullable=True)
    complement = Column(String(100), nullable=True)
    zip_code = Column(String, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)

    def get_full_address(self):
        return f"{self.street}, {self.number} - {self.complement}, {self.zip_code} - {self.city}/{self.state}"