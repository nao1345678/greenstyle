from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId

from models.alternative import (
    Alternative, AlternativeCreate, AlternativeUpdate, AlternativeOut
)
from models.brand import Brand

router = APIRouter(prefix="/alternatives", tags=["Alternatives"])

async def to_out(a: Alternative) -> AlternativeOut:
    brand_id: Optional[str] = None
    brand_name: Optional[str] = None
    category_id: Optional[str] = None

    if a.brand is not None:
        b = await a.brand.fetch() if hasattr(a.brand, "fetch") else a.brand
        if b:
            brand_id = str(b.id)
            brand_name = b.brand_name
            category_id = getattr(b, "category_id", None)

    return AlternativeOut(
        id=str(a.id),
        description=a.description,
        brand_id=brand_id,
        brand_name=brand_name,
        category_id=category_id,
    )

@router.post("/", response_model=AlternativeOut)
async def create_alternative(payload: AlternativeCreate) -> AlternativeOut:
    alt = await Alternative.from_create(payload)
    if payload.brand_id and alt.brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    await alt.insert()
    return await to_out(alt)

@router.get("/", response_model=List[AlternativeOut])
async def list_alternatives(
    brand_id: Optional[str] = Query(default=None),
    category_id: Optional[str] = Query(default=None),
) -> List[AlternativeOut]:
    """
    GET /alternatives?brand_id=...&category_id=...
    - sans param → toutes les alternatives
    - brand_id → alternatives liées à cette marque
    - category_id → alternatives dont la marque a ce category_id
    """
    if brand_id:
        brand = await Brand.get(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        alts = await Alternative.find(Alternative.brand.id == brand.id).to_list()

    elif category_id:
        brands = await Brand.find(Brand.category_id == category_id).to_list()
        brand_ids = {b.id for b in brands}
        if not brand_ids:
            return []
        alts = await Alternative.find(Alternative.brand.id.in_(list(brand_ids))).to_list()

    else:
        alts = await Alternative.find_all().to_list()

    return [await to_out(a) for a in alts]

@router.get("/category/{category_id}", response_model=List[AlternativeOut])
async def list_by_category(category_id: str) -> List[AlternativeOut]:
    brands = await Brand.find(Brand.category_id == category_id).to_list()
    brand_ids = {b.id for b in brands}
    if not brand_ids:
        return []
    alts = await Alternative.find(Alternative.brand.id.in_(list(brand_ids))).to_list()
    return [await to_out(a) for a in alts]

@router.get("/brand/{brand_id}", response_model=List[AlternativeOut])
async def list_by_brand(brand_id: str) -> List[AlternativeOut]:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    alts = await Alternative.find(Alternative.brand.id == brand.id).to_list()
    return [await to_out(a) for a in alts]

@router.get("/{alt_id}", response_model=AlternativeOut)
async def get_alternative(alt_id: PydanticObjectId) -> AlternativeOut:
    alt = await Alternative.get(alt_id)
    if not alt:
        raise HTTPException(status_code=404, detail="Alternative not found")
    return await to_out(alt)

@router.put("/{alt_id}", response_model=AlternativeOut)
async def update_alternative(alt_id: PydanticObjectId, data: AlternativeUpdate) -> AlternativeOut:
    alt = await Alternative.get(alt_id)
    if not alt:
        raise HTTPException(status_code=404, detail="Alternative not found")

    updates = {}
    if data.description is not None:
        updates["description"] = data.description

    if "brand_id" in data.model_fields_set:
        if data.brand_id:
            brand = await Brand.get(data.brand_id)
            if not brand:
                raise HTTPException(status_code=404, detail="Brand not found")
            updates["brand"] = brand
        else:
            updates["brand"] = None

    if updates:
        await alt.set(updates)

    return await to_out(alt)

@router.delete("/{alt_id}")
async def delete_alternative(alt_id: PydanticObjectId) -> dict:
    alt = await Alternative.get(alt_id)
    if not alt:
        raise HTTPException(status_code=404, detail="Alternative not found")
    await alt.delete()
    return {"message": "Alternative deleted"}
