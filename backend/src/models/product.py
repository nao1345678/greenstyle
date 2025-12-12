from typing import Optional

from beanie import Document, Link
from pydantic import BaseModel

from models.brand import Brand


# ---- INPUT SCHEMA ----
class ProductCreate(BaseModel):
    name: str
    brand_id: Optional[str] = None  # Mongo ObjectId as string (optional)


# ---- DOCUMENT stored in DB ----
class Product(Document):
    name: str
    brand: Optional[Link[Brand]] = None

    class Settings:
        name = "products"

    @classmethod
    async def from_create(cls, data: "ProductCreate") -> "Product":
        """
        Build a Product from the input schema.
        Resolves brand_id into a Brand document if provided.
        """
        brand_doc = await Brand.get(data.brand_id) if data.brand_id else None
        return cls(name=data.name, brand=brand_doc)
