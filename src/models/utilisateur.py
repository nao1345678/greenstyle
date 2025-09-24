from beanie import Document
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- SCHEMA d'entrée (body JSON) ----
class UtilisateurCreate(BaseModel):
    nom_utilisateur: str
    prenom: str
    email: EmailStr
    mot_de_passe: str

    def hash_password(self):
        self.mot_de_passe = pwd_context.hash(self.mot_de_passe)

# ---- DOCUMENT stocké en DB ----
class Utilisateur(Document):
    nom_utilisateur: str
    prenom: str
    email: EmailStr
    mot_de_passe: str

    class Settings:
        name = "utilisateurs"

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.mot_de_passe)
