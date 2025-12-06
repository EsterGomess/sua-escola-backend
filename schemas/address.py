from pydantic import BaseModel, Field
from typing import Optional


class SchemaAddressCreate(BaseModel):
    """
    🏠 Address creation schema

    Validation model used when creating an address. Includes required
    fields such as street, zip_code, city and state, and optional fields
    like number, complement and country. Examples are provided via
    json_schema_extra for OpenAPI/docs.
    """
    street: str = Field(..., max_length=100, json_schema_extra={"example": "Rua das Flores"})
    number: Optional[str] = Field(None, max_length=20, json_schema_extra={"example": "104B"})
    district: str = Field(..., json_schema_extra={"example": "Center"})
    complement: Optional[str] = Field(None, max_length=100, json_schema_extra={"example": "apt 104"})
    zip_code: str = Field(..., max_length=20, json_schema_extra={"example": "29877666"})
    city: str = Field(..., max_length=100, json_schema_extra={"example": "São Paulo"})
    state: str = Field(..., max_length=100, json_schema_extra={"example": "SP"})
    country: Optional[str] = Field(None, max_length=100, json_schema_extra={"example": "Brazil"})

    model_config = {
        "from_attributes": True
    }


class SchemaAddressView(BaseModel):
    """
    📍 Address view schema

    Representation returned by the API for an address record.
    """
    id: int
    street: str = Field(..., json_schema_extra={"example": "Rua das Flores"})
    number: Optional[str] = Field(None, json_schema_extra={"example": "104B"})
    district: str = Field(..., json_schema_extra={"example": "Center"})
    city: str = Field(..., json_schema_extra={"example": "Rio de Janeiro"})
    state: str = Field(..., json_schema_extra={"example": "RJ"})
    country: Optional[str] = Field(None, json_schema_extra={"example": "Brazil"})
    zip_code: str = Field(..., max_length=20, json_schema_extra={"example": "29877666"})
    complement: Optional[str] = Field(None, json_schema_extra={"example": "apt 104"})

    model_config = {
        "from_attributes": True
    }


class SchemaAddressUpdate(BaseModel):
    """Schema for partial updates — all fields optional."""
    street: Optional[str] = None
    number: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    complement: Optional[str] = None

    model_config = {"from_attributes": True}