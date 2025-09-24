from beanie import Document
from pydantic import BaseModel

class CategorieCreate(BaseModel):
    nom: str

class Categorie(Document):
    nom: str

    class Settings:
        name = "categories"
