from beanie import Document, Link
from typing import List, Optional

class Site(Document):
    url: str
    marques: Optional[List["Link[Marque]"]]  # "Marque" en string

    class Settings:
        name = "sites"
