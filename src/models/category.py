from beanie import Document
from pydantic import BaseModel

# ---- INPUT SCHEMA ----
class CategoryCreate(BaseModel):
    name: str

# ---- DOCUMENT stored in DB ----
class Category(Document):
    name: str

    class Settings:
        name = "categories"  # match Mongo collection
