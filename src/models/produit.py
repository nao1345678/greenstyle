from beanie import Document, Link
from typing import Optional

class Produit(Document):
    nom: str
    marque: Optional["Link[Marque]"]

    class Settings:
        name = "produits"
