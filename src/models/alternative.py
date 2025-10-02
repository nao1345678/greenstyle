from typing import Optional

from beanie import Document, Link
from pydantic import BaseModel

from models.brand import Brand


# ---- INPUT SCHEMA ----
class AlternativeCreate(BaseModel):
    description: str
    brand_id: Optional[str] = None  # Mongo ObjectId as string (optional)


# ---- DOCUMENT stored in DB ----
class Alternative(Document):
    description: str
    brand: Optional[Link[Brand]] = None  # relation is optional

    class Settings:
        name = "alternatives"

    @classmethod
    async def from_create(cls, data: "AlternativeCreate") -> "Alternative":
        """
        Helper to build an Alternative from the input schema.
        Resolves brand_id into a Brand document (Link) if provided.
        """
        brand_doc: Optional[Brand] = None
        if data.brand_id:
            brand_doc = await Brand.get(data.brand_id)
        return cls(description=data.description, brand=brand_doc)
