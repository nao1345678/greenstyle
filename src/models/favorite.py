from beanie import Document, Link
from pydantic import BaseModel
from models.user import User
from models.brand import Brand

# ---- INPUT SCHEMA ----
class FavoriteCreate(BaseModel):
    user_id: str   # ObjectId as string
    brand_id: str  # ObjectId as string

# ---- DOCUMENT stored in DB ----
class Favorite(Document):
    user: Link[User]
    brand: Link[Brand]

    class Settings:
        name = "favorites"
