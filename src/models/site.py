from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, AnyUrl
from pymongo import IndexModel, ASCENDING
from models.brand import Brand

class SiteCreate(BaseModel):
    url: AnyUrl | str
    brand_ids: Optional[List[str]] = None

class SiteUpdate(BaseModel):
    url: Optional[AnyUrl | str] = None
    brand_ids: Optional[List[str]] = None

class SiteOut(BaseModel):
    id: str
    url: str
    brand_ids: List[str]
    brand_names: List[str]

class Site(Document):
    url: str
    brands: Optional[List[Link[Brand]]] = None

    class Settings:
        name = "sites"
        indexes = [
            IndexModel([("url", ASCENDING)], unique=True, name="uniq_site_url"),
        ]

    @classmethod
    async def from_create(cls, data: "SiteCreate") -> "Site":
        brand_docs: Optional[List[Brand]] = None
        if data.brand_ids:
            brand_docs = []
            for bid in data.brand_ids:
                b = await Brand.get(bid)
                if b:
                    brand_docs.append(b)
        return cls(url=str(data.url), brands=brand_docs)
