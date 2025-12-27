from typing import List, Optional
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId

from models.alternative import (
    Alternative, AlternativeCreate, AlternativeUpdate, AlternativeOut
)
from models.brand import Brand

router = APIRouter(prefix="/alternatives", tags=["Alternatives"])

async def to_out(a: Alternative) -> AlternativeOut:
    brand_id: Optional[str] = None
    brand_name: Optional[str] = None

    if a.brand is not None:
        # Link[Brand] → fetch si nécessaire
        b = await a.brand.fetch() if hasattr(a.brand, "fetch") else a.brand
        if b:
            brand_id = str(b.id)
            brand_name = b.brand_name

    return AlternativeOut(
        id=str(a.id),
        description=a.description,
        brand_id=brand_id,
        brand_name=brand_name,
    )

@router.post("/", response_model=AlternativeOut)
async def create_alternative(payload: AlternativeCreate) -> AlternativeOut:
    alt = await Alternative.from_create(payload)
    # Optionnel: si brand_id fourni mais introuvable → 404 explicite
    if payload.brand_id and alt.brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")

    await alt.insert()
    return await to_out(alt)

@router.get("/", response_model=List[AlternativeOut])
async def list_alternatives() -> List[AlternativeOut]:
    alts = await Alternative.find_all().to_list()
    # évite le N+1 en fetchant les brands (simple et robuste)
    out: List[AlternativeOut] = []
    for a in alts:
        out.append(await to_out(a))
    return out

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

    # Pour savoir si "brand_id" a été fourni (même si None),
    # on vérifie le set des champs fournis par le client.
    if "brand_id" in data.model_fields_set:
        brand_doc = None
        if data.brand_id:  # string non vide -> associer
            brand_doc = await Brand.get(data.brand_id)
            if not brand_doc:
                raise HTTPException(status_code=404, detail="Brand not found")
        # None -> dissocier la brand
        updates["brand"] = brand_doc

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
