from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from typing import Optional

from schemas.address import SchemaAddressCreate, SchemaAddressView, SchemaAddressUpdate
from schemas.contact import SchemaContactCreate, SchemaContactView, SchemaContactUpdate
from schemas.guardian import SchemaGuardianCreate, SchemaGuardianView

class SchemaStudentView(BaseModel):
    """
    Representation of a student's data in a structured schema.

    This class is used to represent the detailed view of a student including their
    identification, personal information such as name and surname, contact data,
    guardians, and timestamps for creation and updates. This schema can be used
    to exchange or expose comprehensive student information.

    :ivar id: Unique identifier for the student.
    :type id: int
    :ivar name: First name of the student. This is a mandatory field.
    :type name: str
    :ivar surname: Last name of the student. This is a mandatory field.
    :type surname: str
    :ivar full_name: Full name of the student. Optional field that combines first
        and last name.
    :type full_name: str
    :ivar address: Address details associated with the student.
    :type address: SchemaAddressView
    :ivar contact: Contact information for the student.
    :type contact: SchemaContactView
    :ivar guardians: List of guardians associated with the student.
    :type guardians: List[SchemaGuardianView]
    :ivar created_at: Timestamp when the student's data was created.
    :type created_at: datetime
    :ivar updated_at: Timestamp when the student's data was last updated.
    :type updated_at: datetime
    """
    id: int
    name: str = Field(..., example="Ana")
    surname: str = Field(..., example="Costa")
    full_name: str = Field(None, example="Ana Costa")
    address: SchemaAddressView
    contact: SchemaContactView
    guardians: List[SchemaGuardianView] = []
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class SchemaStudentCreate(BaseModel):
    """
    Defines a data model for creating a student entity.

    This class represents the necessary information required for creating a
    student, including their personal information, associated address,
    contact details, and details of their guardians. It is a subclass of
    BaseModel to enable validation and configuration.

    :ivar name: The first name of the student.
    :type name: str
    :ivar surname: The surname of the student.
    :type surname: str
    :ivar address: The address information associated with the student.
    :type address: SchemaAddressCreate
    :ivar contact: The contact details of the student.
    :type contact: SchemaContactCreate
    :ivar guardians: A list of guardian details associated with the student.
    :type guardians: List[SchemaGuardianCreate]
    """
    name: str = Field(..., example="Ana")
    surname: str = Field(..., example="Costa")
    address: SchemaAddressCreate
    contact: SchemaContactCreate
    guardians: List[SchemaGuardianCreate]

    model_config = {
        "from_attributes": True
    }

class SchemaStudentQueryResponse(BaseModel):
    """
    Represents a response model for querying student data.

    This class encapsulates the details of a student query response, where
    multiple student views can be stored. It is designed to provide a
    structured way to manage and interact with student data in the context
    of a query response.

    :ivar students: List of student views returned as a result of the query.
    :type students: List[SchemaStudentView]
    """
    students: List[SchemaStudentView] = []
    model_config = {
        "from_attributes": True
    }

class SchemaStudentQueryParam(BaseModel):
    """
    Represents a schema for query parameters related to a student.

    This class is intended to define the structure and validation
    of query parameters that can be used to filter or query student
    data. It leverages Pydantic's BaseModel for validation and type
    definition.

    :ivar id: Represents the optional unique identifier of a student.
    :type id: Optional[int]
    :ivar name: Represents the optional name of a student.
    :type name: Optional[str]
    """
    id: Optional[int] = Field(None, example=123)
    name: Optional[str] = Field(None, example="Ana")

class SchemaStudentUpdate(BaseModel):
    """
    Represents the schema for updating a student's information.

    This class is designed to handle partial updates for a student's record
    in a structured and validated manner. Each attribute corresponds to a
    specific part of the student's information that can be updated. It uses
    Pydantic's features to ensure type safety and data validation.

    :ivar id: Unique identifier of the student.
    :type id: int
    :ivar name: The first name of the student, optional for update.
    :type name: Optional[str]
    :ivar surname: The last name of the student, optional for update.
    :type surname: Optional[str]
    :ivar address: Structured data for the updated address of the student.
    :type address: Optional[SchemaAddressUpdate]
    :ivar contact: Structured data for the updated contact information of
                   the student.
    :type contact: Optional[SchemaContactUpdate]
    """
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    address: Optional[SchemaAddressUpdate] = None
    contact: Optional[SchemaContactUpdate] = None
    guardians: Optional[SchemaGuardianCreate] = None
    model_config = {"from_attributes": True}

class SchemaStudentDeleteParam(BaseModel):
    """
    Represents the structure for deletion parameters of a student.

    This class is used as a model for defining the required parameters
    when attempting to delete a student's record. It enforces strict
    typing and validation of the `id` attribute, which represents the
    unique identifier of the student to be deleted.

    :ivar id: Unique identifier of the student to be deleted.
    :type id: int
    """
    id: int