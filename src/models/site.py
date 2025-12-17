from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel

from models.brand import Brand


class SiteCreate(BaseModel):
    url: str
    brand_ids: Optional[List[str]] = None


class Site(Document):
    url: str
    brands: Optional[List[Link[Brand]]] = None

    class Settings:
        name = "sites"

    @classmethod
    async def from_create(cls, data: "SiteCreate") -> "Site":
        """
        Helper to build a Site from the input schema.
        Resolves brand_ids into Brand documents if provided.
        """
        brand_docs: Optional[List[Brand]] = None
        if data.brand_ids:
            brand_docs = []
            for bid in data.brand_ids:
                brand = await Brand.get(bid)
                if brand:
                    brand_docs.append(brand)
        return cls(url=data.url, brands=brand_docs)
