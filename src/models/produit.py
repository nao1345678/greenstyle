from typing import Optional
from beanie import Document, Link
from .alternative import Alternative

class Produit(Document):
    nom_produit: str
    description_produit: str
    alternative: Optional[Link[Alternative]] = None

    class Settings:
        name = "produits"
