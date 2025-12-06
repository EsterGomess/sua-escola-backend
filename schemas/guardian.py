from pydantic import BaseModel, Field
from typing import Optional
from schemas.address import SchemaAddressCreate
from schemas.contact import SchemaContactCreate

class SchemaGuardianCreate(BaseModel):
    """
    👪 Guardian creates schema

    Schema used when creating a guardian. Includes personal details,
    address and contact information. Designed for validation and
    clear API documentation.
    """
    name: str = Field(..., json_schema_extra={"example": "John"})
    surname: str = Field(..., json_schema_extra={"example": "Doe"})
    address: SchemaAddressCreate
    contact: SchemaContactCreate

    model_config = {
        "from_attributes": True
    }


class SchemaGuardianView(BaseModel):
    """
    🧾 Guardian view schema

    Representation returned by the API for a guardian.
    """
    id: int = Field(..., description="Unique guardian id", json_schema_extra={"example": 1})
    name: str = Field(..., json_schema_extra={"example": "John"})
    surname: str = Field(..., json_schema_extra={"example": "Doe"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-202-555-0123"})

    model_config = {
        "from_attributes": True
    }
