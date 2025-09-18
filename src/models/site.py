from typing import Optional, List
from beanie import Document, Link
from .marque import Marque

class Site(Document):
    nom_site: str
    url: str
    marques: Optional[List[Link[Marque]]] = None

    class Settings:
        name = "sites"
