from sqlalchemy import Column,  Integer


from sqlalchemy.orm import relationship
from models.association import student_guardian

from .user import User

class Student(User):
    __tablename__ = "student"

    id = Column("pk_student", Integer, primary_key=True)

    guardians = relationship(
        "Guardian",
        secondary=student_guardian,
        back_populates="students"
    )
