from sqlalchemy import Column, Integer, String

from backend.models import Base

class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    ddd = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    whatsapp = Column(String(100), nullable=True)

    def get_full_contact(self) -> str:
        contact_info = f"({self.ddd}) {self.phone}"
        if self.email:
            contact_info += f", Email: {self.email}"
        if self.whatsapp:
            contact_info += f", WhatsApp: {self.whatsapp}"
        return contact_info
