from typing import Optional, List
from beanie import Document, Link
from .marque import Marque

class Utilisateur(Document):
    nom_utilisateur: str
    prénom: str
    mail: str
    mot_de_passe: str
    marques: Optional[List[Link[Marque]]] = None

    class Settings:
        name = "utilisateurs"
