from logger import logger
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from models import Student, Address, Contact, Guardian, Session
from schemas import SchemaStudentView, SchemaStudentCreate


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


@app.post('/student', tags=[student_tag], responses={"200": SchemaStudentView})
def add_student(form: SchemaStudentCreate):
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
