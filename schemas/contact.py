
from pydantic import BaseModel, Field
from typing import Optional


class SchemaContactCreate(BaseModel):
    """
    SchemaContactCreate class inherits from BaseModel and is intended to represent a schema for creating
    contact information. This schema specifies mandatory and optional fields, such as phone number, email,
    and WhatsApp details. It also includes configuration for attribute handling.

    :ivar ddd: Represents the area code of the phone number.
    :type ddd: int
    :ivar phone: Represents the contact phone number.
    :type phone: int
    :ivar email: Optional field representing the email address associated with the contact.
    :type email: Optional[str]
    :ivar whatsapp: Optional field representing the WhatsApp number associated with the contact.
    :type whatsapp: Optional[int]
    """
    ddd: int = Field(..., example=11)
    phone: str = Field(..., example=987654321)
    email: Optional[str] = Field(None, max_length=100)
    whatsapp: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class SchemaContactView(BaseModel):
    """
    Represents a schema for viewing contact details.

    This class models the structure for contact details including email, phone,
    WhatsApp, and timestamps for creation and updates. It is used for handling
    and viewing contact information efficiently.

    :ivar id: Unique identifier of the contact.
    :type id: int
    :ivar email: Email address of the contact. Default is None.
    :type email: Optional[str]
    :ivar phone: Phone number of the contact. Default is None.
    :type phone: Optional[str]
    :ivar whatsapp: WhatsApp number of the contact. Default is None.
    :type whatsapp: Optional[str]
    :ivar created_at: Timestamp for when the contact was created. Default is None.
    :type created_at: Optional[datetime]
    :ivar updated_at: Timestamp for when the contact was last updated. Default is None.
    :type updated_at: Optional[datetime]
    """
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class SchemaContactUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    model_config = {"from_attributes": True}