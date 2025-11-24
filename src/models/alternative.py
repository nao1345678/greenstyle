from typing import Optional
from beanie import Document, Link
from pydantic import BaseModel

from models.brand import Brand

class AlternativeCreate(BaseModel):
    description: str
    brand_id: Optional[str] = None

class AlternativeUpdate(BaseModel):
    description: Optional[str] = None
    brand_id: Optional[str] = None

class AlternativeOut(BaseModel):
    id: str
    description: str
    brand_id: Optional[str] = None
    brand_name: Optional[str] = None

class Alternative(Document):
    description: str
    brand: Optional[Link[Brand]] = None

    class Settings:
        name = "alternatives"

    @classmethod
    async def from_create(cls, data: "AlternativeCreate") -> "Alternative":
        brand_doc: Optional[Brand] = None
        if data.brand_id:
            brand_doc = await Brand.get(data.brand_id)
        return cls(description=data.description, brand=brand_doc)
