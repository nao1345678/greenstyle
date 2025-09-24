from beanie import Document
from pydantic import BaseModel
from typing import Optional

# ---- SCHEMA d'entrée (body JSON) ----
class MarqueCreate(BaseModel):
    nom_marque: str
    logo: Optional[str] = None
    lien_web: Optional[str] = None
    categorie_id: Optional[str] = None  

    gamme_prix: Optional[float] = None  
    matieres_resp: Optional[float] = None  
    certifications: Optional[str] = None
    pays_origine: Optional[str] = None
    pays_production: Optional[str] = None
    gestions_invendues: Optional[str] = None
    transparence_chaines: Optional[str] = None

    impact_env_global: Optional[float] = None  
    ethique_travail: Optional[float] = None  
    score_final: Optional[float] = None  

    description_courte: Optional[str] = None
    description: Optional[str] = None

    badge_excellence_planete: Optional[bool] = False
    badge_excellence_travail: Optional[bool] = False


# ---- DOCUMENT stocké en DB ----
class Marque(Document):
    nom_marque: str
    logo: Optional[str] = None
    lien_web: Optional[str] = None
    categorie_id: Optional[str] = None  

    gamme_prix: Optional[float] = None
    matieres_resp: Optional[float] = None
    certifications: Optional[str] = None
    pays_origine: Optional[str] = None
    pays_production: Optional[str] = None
    gestions_invendues: Optional[str] = None
    transparence_chaines: Optional[str] = None

    impact_env_global: Optional[float] = None
    ethique_travail: Optional[float] = None
    score_final: Optional[float] = None

    description_courte: Optional[str] = None
    description: Optional[str] = None

    badge_excellence_planete: Optional[bool] = False
    badge_excellence_travail: Optional[bool] = False

    class Settings:
        name = "marques"
