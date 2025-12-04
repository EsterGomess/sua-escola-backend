from sqlalchemy import Column, Integer

from sqlalchemy.orm import relationship
from models.association import student_guardian
from .user import User

class Guardian(User):
    __tablename__ = "guardian"

    id = Column("pk_guardian", Integer, primary_key=True)

    students = relationship(
        "Student",
        secondary=student_guardian,
        back_populates="guardians"
    )