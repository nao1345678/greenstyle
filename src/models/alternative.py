from beanie import Document, Link
from typing import Optional

class Alternative(Document):
    description: str
    produit: Optional["Link[Produit]"]

    class Settings:
        name = "alternatives"
