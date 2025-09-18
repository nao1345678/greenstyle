from typing import Optional, List
from beanie import Document, Link
from .marque import Marque
from .produit import Produit

class Alternative(Document):
    description: str
    marque: Optional[Link[Marque]] = None
    produits: Optional[List[Link[Produit]]] = None

    class Settings:
        name = "alternatives"
