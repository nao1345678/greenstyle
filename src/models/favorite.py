from typing import Optional
from beanie import Document, Link
from pydantic import BaseModel
from models.user import User
from models.brand import Brand
from pymongo import IndexModel, ASCENDING

class FavoriteCreate(BaseModel):
    user_id: str
    brand_id: str
    name: Optional[str] = None
    cover_url: Optional[str] = None
    content: Optional[str] = None

class FavoriteUpdate(BaseModel):
    name: Optional[str] = None
    cover_url: Optional[str] = None
    content: Optional[str] = None

class FavoriteOut(BaseModel):
    id: str
    user_id: str
    brand_id: str
    name: Optional[str] = None
    cover_url: Optional[str] = None
    content: Optional[str] = None
    brand_name: Optional[str] = None

class Favorite(Document):
    user: Link[User]
    brand: Link[Brand]
    name: Optional[str] = None
    cover_url: Optional[str] = None
    content: Optional[str] = None

    class Settings:
        name = "favorites"
        indexes = [
            IndexModel([("user.$id", ASCENDING)], name="idx_user"),
            IndexModel([("brand.$id", ASCENDING)], name="idx_brand"),
        ]
