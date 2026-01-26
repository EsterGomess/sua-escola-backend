from backend.models import Student, Guardian, Address, Contact, Session
from sqlalchemy.exc import IntegrityError
from typing import Tuple, List, Optional, Dict
from sqlalchemy.orm import joinedload

def delete_student_by_id(student_id: int):
    """
    Service layer: delete a student by id.
    Returns: (success: bool, message: str)
    Raises unexpected exceptions for the caller to log/handle.
    """
    session = Session()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return False, "Student not found."

        session.delete(student)
        session.commit()
        return True, f"Student with id {student_id} deleted successfully."
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def update_student_by_id(student_id: int, update_data: dict):
    session = Session()
    try:
        student = (
            session.query(Student)
            .options(
                joinedload(Student.address),
                joinedload(Student.contact),
                joinedload(Student.guardians),
            )
            .filter(Student.id == student_id)
            .first()
        )
        if not student:
            return False, "Student not found.", None

        if update_data.get("name") is not None or "":
            student.name = update_data["name"]
        if update_data.get("surname") is not None or "":
            student.surname = update_data["surname"]

        addr = update_data.get("address")
        if addr:
            if student.address is None or addr == {}:
                student.address = Address()
            for field, value in addr.items():
                if value is not None:
                    setattr(student.address, field, value)

        contact = update_data.get("contact")
        if contact:
            if student.contact is None or "":
                student.contact = Contact()
            for field, value in contact.items():
                if value is not None or "":
                    setattr(student.contact, field, value)

        guardian = update_data.get("guardian") or update_data.get("guardians")
        if guardian:
            guardians_to_add = guardian if isinstance(guardian, list) else [guardian]
            for gd in guardians_to_add:
                guardian_addr = Address(**gd["address"]) if gd.get("address") else None
                guardian_contact = Contact(**gd["contact"]) if gd.get("contact") else None
                guardian_obj = Guardian(
                    name=gd.get("name"),
                    surname=gd.get("surname"),
                    address=guardian_addr,
                    contact=guardian_contact,
                )
                student.guardians.append(guardian_obj)

        session.commit()
        session.refresh(student)

        _ = student.address
        _ = student.contact
        _ = list(student.guardians)

        return True, "Student updated successfully.", student

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def create_student(data: dict):
    session = Session()
    try:
        student_address = Address(**data["address"])
        student_contact = Contact(**data["contact"])

        if isinstance(data["guardians"], dict):
            guardians_list = [data["guardians"]]
        else:
            guardians_list = data["guardians"]

        guardians_objs = []
        for gd in guardians_list:
            gd_address = Address(**gd["address"])
            gd_contact = Contact(**gd["contact"])
            guardian_obj = Guardian(
                name=gd["name"],
                surname=gd.get("surname"),
                address=gd_address,
                contact=gd_contact,
            )
            guardians_objs.append(guardian_obj)

        student = Student(
            name=data["name"],
            surname=data.get("surname"),
            address=student_address,
            contact=student_contact,
            guardians=guardians_objs,
        )

        session.add(student)
        session.commit()
        session.refresh(student)

        _ = student.address
        _ = student.contact
        _ = list(student.guardians)

        return True, "Student created successfully.", student

    except IntegrityError as e:
        session.rollback()
        error_msg = str(e.orig)
        if "NOT NULL constraint failed" in error_msg:
            field = error_msg.split(":")[-1].strip()
            return False, f"Required field missing: {field}", None
        if "UNIQUE constraint failed" in error_msg:
            return False, "A record with this unique data already exists.", None
        return False, f"Integrity error: {error_msg}", None

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

def get_students(filters: Dict) -> Tuple[bool, str, Optional[List[Student]]]:
    session = Session()
    try:
        q = session.query(Student).options(
            joinedload(Student.address),
            joinedload(Student.contact),
            joinedload(Student.guardians)
        )

        student_id = filters.get("id")
        if student_id is not None:
            student = q.filter(Student.id == int(student_id)).first()
            if not student:
                return False, "Student not found.", None
            return True, "Student found.", [student]

        name = filters.get("name")
        if name:
            q = q.filter(Student.name.ilike(f"%{name}%"))

        surname = filters.get("surname")
        if surname:
            q = q.filter(Student.surname.ilike(f"%{surname}%"))

        try:
            limit = int(filters.get("limit", 50))
            offset = int(filters.get("offset", 0))
        except (TypeError, ValueError):
            limit = 50
            offset = 0

        students = q.offset(offset).limit(limit).all()

        for s in students:
            _ = s.address
            _ = s.contact
            _ = list(s.guardians)

        return True, f"{len(students)} student(s) found.", students

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()