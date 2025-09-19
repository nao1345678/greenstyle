from beanie import Document
from pydantic import BaseModel, EmailStr

# ---- SCHEMA d'entrée (body JSON pour créer un user) ----
class UtilisateurCreate(BaseModel):
    nom: str
    email: EmailStr
    age: int

# ---- DOCUMENT stocké en DB ----
class Utilisateur(Document):
    nom: str
    email: EmailStr
    age: int
