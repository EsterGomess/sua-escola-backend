from logger import logger
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from services import  (delete_student_by_id,
                       update_student_by_id,
                       create_student,
                       get_students)
from schemas import (SchemaStudentView,
                     SchemaStudentCreate,
                     SchemaStudentQueryParam,
                     SchemaStudentUpdate,
                     SchemaStudentDeleteParam)

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
          responses={"201": SchemaStudentView,
                     "400": {"description": "Invalid data or unexpected error."},
                     "409": {"description": ""},
                     })
def add_student(form: SchemaStudentCreate):
    """
    Creates a new student entry from the provided form data and returns the corresponding
    student details, along with associated links for further interactions.

    This function processes the user-provided form input, validates it, and attempts
    to create a new student record in the database. Upon successful creation, it builds
    a response containing the newly created student's details, relevant links for
    resource navigation, and header metadata.

    :param form: The form data required for creating a student, validated via SchemaStudentCreate.
    :type form: SchemaStudentCreate
    :return: A tuple containing:
             - A JSON-formatted response with the newly created student's details and related links
             - HTTP status code (either 201, 400, or 409)
             - Relevant headers for the response
    :rtype: tuple
    """
    try:
        payload = form.model_dump()
        success, msg, student = create_student(payload)
        if not success:
            return {"message": msg}, 400 if "Required" in msg or "Integrity" in msg else 409

        body = SchemaStudentView.from_orm(student).model_dump()
        body["_links"] = {
            "self": {"href": f"/student?id={student.id}"},
            "get": {"href": f"/student?name={student.name}"},
            "docs": {"href": "/openapi"}
        }
        headers = {
            "Content-Type": "application/json",
            "Link": '</openapi>; rel="service-doc"'
        }
        return body, 201, headers
    except Exception as e:
        logger.exception(f"Unexpected error while creating student: {e}")
        return {"message":"Invalid data or unexpected error."}, 400


@app.get('/student', tags=[student_tag],
         responses={
             "200": {"description": "Student(s) retrieved successfully."},
             "404": {"description": "Student not found."},
             "400": {"description": "Invalid query or retrieval failure."},

         })
def get_student(query: SchemaStudentQueryParam):
    """
    Retrieves student information based on provided query parameters. The endpoint
    requires at least one of the following query parameters: id, name, or surname.
    If no query parameters are provided, a 400 Bad Request status is returned. The
    function attempts to retrieve the student(s) based on the filters specified.
    If retrieval is successful, it returns the student data, including hypermedia
    links for navigation. Else, it returns appropriate status and message.

    :param query: Query parameters for filtering student records. Should include at
        least one of the following: id, name, or surname.
    :type query: SchemaStudentQueryParam
    :return: A list of student records if retrieval is successful, with each record
        containing hypermedia links. Appropriate HTTP status codes and error
        messages returned in case of failure.
    :rtype: tuple or JSON
    """
    if not (query.id or query.name or query.surname):
        return {"message": "Provide at least one query parameter (id, name or surname)."}, 400

    try:
        filters = query.model_dump()
        success, msg, students = get_students(filters)
        if not success:
            return {"message": msg}, 404

        body = []
        for s in students:
            item = SchemaStudentView.from_orm(s).model_dump()
            item["_links"] = {
                "self": {"href": f"/student?id={s.id}"},
                "list": {"href": "/student"},
                "docs": {"href": "/openapi"}
            }
            body.append(item)

        headers = {
            "Content-Type": "application/json",
            "Link": '</openapi>; rel="service-doc"'
        }
        return body, 200, headers

    except Exception as e:
        logger.exception(f"Unexpected error while retrieving student(s): {e}")
        return {"message": "Invalid query or retrieval failure."}, 400


@app.patch('/student', tags=[student_tag],
         responses={"200": SchemaStudentView,
                    "404": {"description": "Student not found."},
                    "400": {"description": "Invalid input or update failure."},
                    "409": {"description": "Integrity constraint violated."}})
def update_student(form: SchemaStudentUpdate):
    """
    Updates the information of an existing student based on the provided data.
    This API endpoint allows partial updates for a student's record, utilizing
    the fields included in the request form. Error handling is performed
    to manage possible violations, unavailability of record, or invalid data.

    :param form: An instance of SchemaStudentUpdate containing the partial update
        data for the student.
    :type form: SchemaStudentUpdate

    :return: A tuple consisting of the updated student information, HTTP status
        code, and any necessary headers. If the update is successful, the status
        code will be 200 and the body will contain the updated student details.
        In case of failure, an appropriate HTTP error status code and message will
        be included.
    :rtype: tuple
    """
    try:
        update_payload = form.model_dump(exclude_none=True)

        success, msg, student = update_student_by_id(form.id, update_payload)
        if not success:
            return {"message": msg}, 404

        body = SchemaStudentView.from_orm(student).model_dump()
        body["_links"] = {
            "self": {"href": f"/student?id={student.id}"},
            "get": {"href": f"/student?name={student.name}"},
            "docs": {"href": "/openapi"}
        }
        headers = {
            "Content-Type": "application/json",
            "Link": '</openapi>; rel="service-doc"'
        }
        return body, 200, headers

    except IntegrityError as e:
        logger.warning(f"Integrity error while updating student: {e}")
        return {"message": "Integrity constraint violated."}, 409

    except Exception as e:
        logger.exception(f"Unexpected error while updating student: {e}")
        return {"message": "Invalid input or update failure."}, 400


@app.delete('/student',
            tags=[student_tag],
            responses={
                "200": {"description": "Student deleted successfully."},
                "404": {"description": "Student not found."},
                "400": {"description": "Invalid or missing student ID, or deletion failure."},
            }
            )
def delete_student(query: SchemaStudentDeleteParam):
    """
    Deletes a student record by student ID.

    This function handles deletion of a student record based on the provided ID. It
    validates the presence of the ID, attempts the deletion, and returns appropriate
    responses based on the operation outcome. The response includes message details
    and supplementary link headers for additional API documentation references.

    :param query: The parameters required for deleting a student, encapsulated in
        the SchemaStudentDeleteParam object. The ID within the query must be valid
        and provided.
    :type query: SchemaStudentDeleteParam
    :return: A tuple containing the response body, HTTP status code, and optional
        headers:
        - Successful deletion: HTTP 200 with a JSON message body and linking headers.
        - Not found: HTTP 404 with an error message.
        - Invalid or missing student ID, or unexpected failure: HTTP 400 with an
          error message.
    :rtype: tuple
    """

    if not query.id:
        return {"message": "Invalid or missing student ID, or deletion failure."}, 400

    try:
        success, msg = delete_student_by_id(query.id)
        if not success:
            return {"message": msg}, 404

        body = {
            "message": msg,
            "_links": {
                "self": {"href": f"/student?id={query.id}"},
                "docs": {"href": "/openapi"},
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Link": '</openapi>; rel="service-doc"'
        }
        return body, 200, headers

    except Exception as e:
        logger.exception(f"Unexpected error while deleting student: {e}")
        return {"message": "Invalid or missing student ID, or deletion failure."}, 400

