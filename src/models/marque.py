from beanie import Document
from pydantic import BaseModel

# ---- SCHEMA d'entrée (reçoit les données du body JSON via Postman) ----
class MarqueCreate(BaseModel):
    nom: str
    pays: str

# ---- DOCUMENT (ce qui est stocké en DB) ----
class Marque(Document):
    nom: str
    pays: str
