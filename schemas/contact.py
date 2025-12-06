from pydantic import BaseModel, Field
from typing import Optional


class SchemaContactCreate(BaseModel):
    """
    ✉️ Contact creation schema

    Schema for creating contact information. Fields include area code (ddd), phone,
    optional email and WhatsApp. Examples are provided for documentation (OpenAPI).
    """
    ddd: int = Field(..., json_schema_extra={"example": 11})
    phone: str = Field(..., json_schema_extra={"example": "987654321"})
    email: Optional[str] = Field(None, max_length=100, json_schema_extra={"example": "user@example.com"})
    whatsapp: Optional[str] = Field(None, json_schema_extra={"example": "+5511987654321"})

    model_config = {
        "from_attributes": True
    }

class SchemaContactView(BaseModel):
    """
    📞 Contact view schema

    Representation returned by the API for contact details.
    """
    id: int
    email: Optional[str] = Field(None, json_schema_extra={"example": "user@example.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "987654321"})
    whatsapp: Optional[str] = Field(None, json_schema_extra={"example": "+5511987654321"})

    model_config = {
        "from_attributes": True
    }

class SchemaContactUpdate(BaseModel):
    phone: Optional[str] = Field(None, json_schema_extra={"example": "987654321"})
    email: Optional[str] = Field(None, json_schema_extra={"example": "user@example.com"})
    whatsapp: Optional[str] = Field(None, json_schema_extra={"example": "+5511987654321"})
    model_config = {"from_attributes": True}