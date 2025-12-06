from pydantic import BaseModel, Field
from typing import Optional
from schemas.address import SchemaAddressCreate
from schemas.contact import SchemaContactCreate

class SchemaGuardianCreate(BaseModel):
    """
    Represents a schema for creating a new guardian entity.

    This class contains the necessary information to define a guardian, including
    personal details, address, and contact information. It is used as part of
    validation and data structure representation when creating a guardian record.

    :ivar name: The first name of the guardian.
    :type name: str
    :ivar surname: The last name of the guardian.
    :type surname: str
    :ivar address: The address details of the guardian.
    :type address: SchemaAddressCreate
    :ivar contact: The contact details of the guardian.
    :type contact: SchemaContactCreate
    """
    name: str = Field(..., example="João")
    surname: str = Field(..., example="Silva")
    address: SchemaAddressCreate
    contact: SchemaContactCreate

    model_config = {
        "from_attributes": True
    }

class SchemaGuardianView(BaseModel):
    """
    Represents a view model for a guardian schema entity.

    Provides a structured way to handle the representation of
    guardian information in the system, ensuring consistency and
    validations.

    :ivar id: Unique identifier for the guardian entity.
    :type id: int
    :ivar name: First name of the guardian.
    :type name: str
    :ivar surname: Surname of the guardian.
    :type surname: str
    :ivar relationship: The relationship of the guardian to the entity they are responsible for
        (e.g., parent, legal guardian). This field is optional.
    :type relationship: Optional[str]
    :ivar phone: Contact phone number of the guardian. This field is optional.
    :type phone: Optional[str]
    """
    id: int
    name: str = Field(..., example="João")
    surname: str = Field(..., example="Silva")
    phone: Optional[str] = None


    model_config = {
        "from_attributes": True
    }

