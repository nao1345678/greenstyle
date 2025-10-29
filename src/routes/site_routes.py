from typing import List, Optional
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from models.site import Site, SiteCreate, SiteUpdate, SiteOut
from models.brand import Brand

router = APIRouter(prefix="/sites", tags=["Sites"])

async def to_out(s: Site) -> SiteOut:
    brand_ids: List[str] = []
    brand_names: List[str] = []
    if s.brands:
        fetched = []
        for link in s.brands:
            b = await link.fetch() if hasattr(link, "fetch") else link
            if b:
                fetched.append(b)
        brand_ids = [str(b.id) for b in fetched]
        brand_names = [b.brand_name for b in fetched]
    return SiteOut(id=str(s.id), url=s.url, brand_ids=brand_ids, brand_names=brand_names)

@router.get("/", response_model=List[SiteOut])
async def list_sites() -> List[SiteOut]:
    sites = await Site.find_all().to_list()
    return [await to_out(s) for s in sites]

@router.post("/", response_model=SiteOut)
async def create_site(payload: SiteCreate) -> SiteOut:
    site = await Site.from_create(payload)
    try:
        await site.insert()
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Site URL already exists")
    return await to_out(site)

@router.put("/{site_id}", response_model=SiteOut)
async def update_site(site_id: PydanticObjectId, data: SiteUpdate) -> SiteOut:
    site = await Site.get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    updates: dict = {}

    if data.url is not None:
        updates["url"] = str(data.url)

    if "brand_ids" in data.model_fields_set:
        new_links: Optional[List[Brand]] = None
        if data.brand_ids is not None:
            new_links = []
            for bid in data.brand_ids:
                b = await Brand.get(bid)
                if not b:
                    raise HTTPException(status_code=404, detail=f"Brand not found: {bid}")
                new_links.append(b)
        updates["brands"] = new_links

    if updates:
        try:
            await site.set(updates)
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail="Site URL already exists")

    return await to_out(site)

@router.delete("/{site_id}")
async def delete_site(site_id: PydanticObjectId) -> dict:
    site = await Site.get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await site.delete()
    return {"message": "Site deleted"}
