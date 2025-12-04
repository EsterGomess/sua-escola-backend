from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

student_guardian = Table(
    "student_guardian",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("student.pk_student"), primary_key=True),
    Column("guardian_id", Integer, ForeignKey("guardian.pk_guardian"), primary_key=True)
)
