
from pydantic import BaseModel, Field
from typing import Optional


class SchemaAddressCreate(BaseModel):
    """
    Represents an address schema creation model.

    This class models the data needed to create an address, including required
    fields like street, zip code, city, state, and optional fields such as
    number, complement, and country. It ensures constraints such as maximum
    field lengths and allows for customization of attributes when creating
    instances.

    :ivar street: The name of the street.
    :ivar number: The number of the location on the street (optional).
    :ivar complement: Additional details about the address (optional).
    :ivar zip_code: The postal code for the address.
    :ivar city: The city in which the address is located.
    :ivar state: The state or region of the address.
    :ivar country: The country where the address is located (optional).
    """
    street: str = Field(..., max_length=100,example="Rua das Flores")
    number: Optional[str] = Field('', max_length=20, example="104B")
    district: str = Field(..., example="Center")
    complement: Optional[str] = Field('', max_length=100, example="apt 104")
    zip_code: str = Field(..., max_length=20,example="29877666")
    city: str = Field(..., max_length=100, example="São Paulo")
    state: str = Field(..., max_length=100, example="SP")
    country: Optional[str] = Field(..., max_length=100, example="Brazil")

    model_config = {
        "from_attributes": True
    }


class SchemaAddressView(BaseModel):
    """
    Representation of an address view model.

    This class serves as a schema model to represent address-related
    details including street, city, state, and other optional attributes.
    It can be utilized in scenarios involving address management or
    displaying address-related information.

    :ivar id: Unique identifier for the address.
    :type id: int
    :ivar street: Name of the street for the address.
    :type street: str
    :ivar number: (Optional) Number of the address.
    :type number: Optional[str]
    :ivar district: (Optional) District or neighborhood of the address.
    :type district: Optional[str]
    :ivar city: (Optional) City of the address.
    :type city: Optional[str]
    :ivar state: (Optional) State of the address.
    :type state: Optional[str]
    :ivar zipcode: (Optional) Postal/ZIP code of the address.
    :type zipcode: Optional[str]
    :ivar complement: (Optional) Additional address information or details.
    :type complement: Optional[str]
    :ivar created_at: (Optional) Timestamp when the address entry was created.
    :type created_at: Optional[datetime]
    :ivar updated_at: (Optional) Timestamp when the address entry was last updated.
    :type updated_at: Optional[datetime]
    """
    id: int
    street: str = Field(..., example="Rua das Flores")
    number: Optional[str] = ''
    district: str = Field(..., example="Center")
    city: str = Field(..., example="Rio de Janeiro")
    state: str = Field(..., example="RJ")
    country: str = Field(..., example="Brazil")
    zip_code: str = Field(..., max_length=20,example="29877666")
    complement: Optional[str] = ''

    model_config = {
        "from_attributes": True
    }