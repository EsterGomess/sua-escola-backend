from logger import logger
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from models import Student, Address, Contact, Guardian, Session
from schemas import (SchemaStudentView,
                     SchemaStudentCreate,
                     SchemaStudentQueryResponse,
                     SchemaStudentQueryParam,
                     SchemaStudentUpdate)

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
student_tag = Tag(name="Student", description="Addition, viewing, and removal of students in the database")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/student', tags=[student_tag],
          responses={"200": SchemaStudentView})
def add_student(form: SchemaStudentCreate):
    """
    Handles the addition of a new student and their associated data to the database.

    This function accepts a `SchemaStudentCreate` form, processes and validates the data,
    and creates new instances of `Student`, `Address`, `Contact`, and `Guardian` records
    based on the provided information. It also commits these records to the database.

    In case of an error during the creation process, appropriate responses with
    error messages are returned to inform about the failure. Specifically, it handles
    `IntegrityError` for database constraints as well as any other unexpected exceptions.

    :param form: The data schema containing details about the student, their guardians,
        address, and contact information
    :type form: SchemaStudentCreate
    :return: A tuple containing the created student's data in dictionary form and the
        HTTP status code 200 upon success, or an error message and corresponding HTTP
        status code upon failure
    :rtype: tuple[dict, int]
    """
    session = Session()
    logger.debug("Inicializing session")
    try:
        student_address = Address(**form.address.dict())
        student_contact = Contact(**form.contact.dict())

        guardians_objs = []
        for gd in form.guardians:
            gd_address = Address(**gd.address.dict())
            gd_contact = Contact(**gd.contact.dict())

            guardian_obj = Guardian(
                name=gd.name,
                surname=gd.surname,
                address=gd_address,
                contact=gd_contact,
            )

            logger.debug("Created guardian:", guardian_obj)
            guardians_objs.append(guardian_obj)

        student = Student(
            name=form.name,
            surname=form.surname,
            address=student_address,
            contact=student_contact,
            guardians=guardians_objs,
        )

        session.add(student)
        session.commit()
        session.refresh(student)

        return SchemaStudentView.from_orm(student).dict(), 200

    except IntegrityError as e:
        session.rollback()
        error_msg = str(e.orig)

        if "NOT NULL constraint failed" in error_msg:
            field = error_msg.split(":")[-1].strip()
            logger.warning(f"NOT NULL constraint failed {error_msg} ")
            return {
                "message": f"Required field missing: {field}"
            }, 400

        if "UNIQUE constraint failed" in error_msg:
            logger.warning(f"UNIQUE constraint failed {error_msg} ")
            return {
                "message": "A record with this unique data already exists."
            }, 409

        return {
            "message": f"Integrity error: {error_msg}"
        }, 400

    except Exception as e:
        session.rollback()
        logger.exception(f"Unexpect error : {e}")
        return {"message": "Was not possible created a new student :/"}, 400

    finally:
        session.close()


@app.get('/student', tags=[student_tag],
         responses={"200": SchemaStudentQueryResponse})
def get_student(query: SchemaStudentQueryParam):
    """
    Fetches student information by name using a query parameter.

    Example: GET /student?name=John

    :return: A tuple containing a list of student details or a message
        if the student is not found, and an HTTP status code
    :rtype: tuple
    """

    if not query.name:
        return {"message": "Please provide a student name using the 'name' query parameter."}, 400

    session = Session()
    logger.debug("Initializing session")
    try:
        students = session.query(Student).filter(Student.name == query.name).all()

        if not students:
            logger.info(f"Student name {query.name} not found")
            return {"message": "Student not found."}, 404

        student_views = [SchemaStudentView.from_orm(s) for s in students]

        return SchemaStudentQueryResponse(students=student_views).model_dump(), 200

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"message": "Was not possible to get the student :/"}, 400

    finally:
        session.close()


@app.put('/student', tags=[student_tag],
         responses={"200": SchemaStudentView})
def update_student(form: SchemaStudentUpdate):
    """
    Updates a student's information.

    Allows updating the student's name, surname, address, contact, and adding new guardians.

    - **id**: Required, identifies which student to update.
    - **name**: Optional, new student name.
    - **surname**: Optional, new student surname.
    - **address**: Optional, new address fields.
    - **contact**: Optional, new contact fields.
    - **guardians**: Optional, list of new guardians to add.

    Example payload:
    ```json
    {
        "id": 1,
        "name": "João",
        "surname": "Pereira",
        "address": {
            "street": "Rua Nova",
            "city": "São Paulo"
        },
        "contact": {
            "phone": "+551199999999"
        }
    }
    ```
    """
    session = Session()
    try:
        student = session.query(Student).filter(Student.id == form.id).first()
        if not student:
            return {"message": "Student not found."}, 404

        if form.name is not None:
            student.name = form.name
        if form.surname is not None:
            student.surname = form.surname

        if form.address:
            for field, value in form.address.model_dump().items():
                if value is not None:
                    setattr(student.address, field, value)

        if form.contact:
            for field, value in form.contact.model_dump().items():
                if value is not None:
                    setattr(student.contact, field, value)

        session.commit()
        session.refresh(student)

        return SchemaStudentView.from_orm(student).model_dump(), 200

    except Exception as e:
        session.rollback()
        logger.exception(f"Unexpected error while updating student: {e}")
        return {"message": "Was not possible to update the student :/"}, 400

    finally:
        session.close()
