from beanie import Document, Link
from pydantic import BaseModel
from models.user import User
from models.brand import Brand

class FavoriteCreate(BaseModel):
    user_id: str
    brand_id: str

class Favorite(Document):
    user: Link[User]
    brand: Link[Brand]

    class Settings:
        name = "favorites"
