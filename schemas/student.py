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

    This class is used to represent the detailed view of a student, including
    identification, personal information such as name and surname, contact data,
    guardians, and timestamps for creation and updates. This schema can be used
    to exchange or expose comprehensive student information.

    :ivar id: Unique identifier for the student.
    :type id: int.
    :ivar name: First name of the student. This is a mandatory field.
    :type name: str.
    :ivar surname: Last name of the student. This is a mandatory field.
    :type surname: str.
    :ivar full_name: Full name of the student. This is an optional field that combines first
        and last name.
    :type full_name: str.
    :ivar address: Address details associated with the student.
    :type address: SchemaAddressView.
    :ivar contact: Contact information for the student.
    :type contact: SchemaContactView.
    :ivar guardians: List of guardians associated with the student.
    :type guardians: List[SchemaGuardianView].
    :ivar created_at: Timestamp when the student's data was created.
    :type created_at: datetime.
    :ivar updated_at: Timestamp when the student's data was last updated.
    :type updated_at: datetime.
    """
    id: int
    name: str = Field(..., json_schema_extra={"example": "Ana"})
    surname: str = Field(..., json_schema_extra={"example": "Costa"})
    full_name: Optional[str] = Field(None, json_schema_extra={"example": "Ana Costa"})
    address: SchemaAddressView
    contact: SchemaContactView
    guardians: List[SchemaGuardianView] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class SchemaStudentCreate(BaseModel):
    """
    Defines a data model for creating a student entity.

    This class represents the necessary information required for creating a
    student, including personal information, associated address, contact details,
    and information about guardians. Use this model for request validation when
    creating new students.

    :ivar name: The first name of the student.
    :type name: str.
    :ivar surname: The surname of the student.
    :type surname: str.
    :ivar address: The address information associated with the student.
    :type address: SchemaAddressCreate.
    :ivar contact: The contact details of the student.
    :type contact: SchemaContactCreate.
    :ivar guardians: A list of guardian details associated with the student.
    :type guardians: List[SchemaGuardianCreate].
    """
    name: str = Field(..., json_schema_extra={"example": "Ana"})
    surname: str = Field(..., json_schema_extra={"example": "Costa"})
    address: SchemaAddressCreate
    contact: SchemaContactCreate
    guardians: List[SchemaGuardianCreate]

    model_config = {
        "from_attributes": True
    }

class SchemaStudentQueryResponse(BaseModel):
    """
    Represents a response model for querying student data.

    This class encapsulates the details of a student query response and holds
    a list of student views returned by the query.

    :ivar students: The list of student view returned as a result of the query.
    :type students: List[SchemaStudentView].
    """
    students: List[SchemaStudentView] = Field(default_factory=list)
    model_config = {
        "from_attributes": True
    }

class SchemaStudentQueryParam(BaseModel):
    """
    Represents a schema for query parameters related to students.

    Use this model to validate query parameters when searching or filtering
    students by `id` or `name`.

    :ivar id: Optional unique identifier of a student.
    :type id: Optional[int].
    :ivar name: Optional name filter for the student.
    :type name: Optional[str].
    """
    id: Optional[int] = Field(None, json_schema_extra={"example": 123})
    name: Optional[str] = Field(None, json_schema_extra={"example": "Ana"})

class SchemaStudentUpdate(BaseModel):
    """
    Represents the schema for updating a student's information.

    This model supports partial updates. Only fields provided by the client
    will be included when you call `model_dump(exclude_unset=True)`.

    :ivar id: Unique identifier of the student.
    :type id: int.
    :ivar name: The first name of the student. Optional for update.
    :type name: Optional[str].
    :ivar surname: The last name of the student. Optional for update.
    :type surname: Optional[str].
    :ivar address: Structured data for the updated address of the student.
    :type address: Optional[SchemaAddressUpdate].
    :ivar contact: Structured data for the updated contact information of the student.
    :type contact: Optional[SchemaContactUpdate].
    :ivar guardians: Optional list of guardian objects to add or update.
    :type guardians: Optional[List[SchemaGuardianCreate]].
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

    This model is used when deleting a student by id.

    :ivar id: Unique identifier of the student to be deleted.
    :type id: int.
    """
    id: int