from typing import List
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId

from models.brand import Brand, BrandCreate, BrandUpdate, BrandOut

router = APIRouter(prefix="/brands", tags=["Brands"])


def to_out(b: Brand) -> BrandOut:
    return BrandOut(
        id=str(b.id),
        brand_name=b.brand_name,
        logo=b.logo,
        website=b.website,
        category_id=b.category_id,
        price_range=b.price_range,
        sustainable_materials=b.sustainable_materials,
        certifications=b.certifications,
        country_origin=b.country_origin,
        country_production=b.country_production,
        unsold_management=b.unsold_management,
        supply_chain_transparency=b.supply_chain_transparency,
        global_env_impact=b.global_env_impact,
        labor_ethics=b.labor_ethics,
        final_score=b.final_score,
        short_description=b.short_description,
        description=b.description,
        planet_badge=b.planet_badge,
        labor_badge=b.labor_badge,
    )


@router.post("/", response_model=BrandOut)
async def create_brand(payload: BrandCreate) -> BrandOut:
    brand = Brand(**payload.model_dump())
    await brand.insert()
    return to_out(brand)


@router.get("/", response_model=List[BrandOut])
async def list_brands() -> List[BrandOut]:
    brands = await Brand.find_all().to_list()
    return [to_out(b) for b in brands]


@router.get("/{brand_id}", response_model=BrandOut)
async def get_brand(brand_id: PydanticObjectId) -> BrandOut:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return to_out(brand)


@router.put("/{brand_id}", response_model=BrandOut)
async def update_brand(brand_id: PydanticObjectId, data: BrandUpdate) -> BrandOut:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    await brand.set(data.model_dump(exclude_unset=True))
    return to_out(brand)


@router.delete("/{brand_id}")
async def delete_brand(brand_id: PydanticObjectId) -> dict:
    brand = await Brand.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    await brand.delete()
    return {"message": "Brand deleted"}
