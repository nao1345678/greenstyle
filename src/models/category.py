from typing import Optional
from beanie import Document
from pydantic import BaseModel
from pymongo import IndexModel, ASCENDING

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryOut(BaseModel):
    id: str
    name: str

class Category(Document):
    name: str

    class Settings:
        name = "categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True, name="uniq_category_name")
        ]
