from typing import Optional, List
from beanie import Document, Link
from .site import Site
from .alternative import Alternative

class Marque(Document):
    nom_marque: str
    description_marque: Optional[str] = None
    score_final: Optional[int] = None
    sites: Optional[List[Link[Site]]] = None
    alternatives: Optional[List[Link[Alternative]]] = None

    class Settings:
        name = "marques"
