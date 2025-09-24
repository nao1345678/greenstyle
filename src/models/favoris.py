from beanie import Document, Link
from pydantic import BaseModel
from models.utilisateur import Utilisateur
from models.marque import Marque

# ---- SCHEMA d'entrée (body JSON) ----
class FavorisCreate(BaseModel):
    utilisateur_id: str  # ObjectId sous forme de string
    marque_id: str       # ObjectId sous forme de string

# ---- DOCUMENT stocké en DB ----
class Favoris(Document):
    utilisateur: Link[Utilisateur]
    marque: Link[Marque]

    class Settings:
        name = "favoris"
