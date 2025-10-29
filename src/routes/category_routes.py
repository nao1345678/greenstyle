from typing import List
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from models.category import Category, CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])

def to_out(c: Category) -> CategoryOut:
    return CategoryOut(id=str(c.id), name=c.name)

@router.post("/", response_model=CategoryOut)
async def create_category(payload: CategoryCreate) -> CategoryOut:
    cat = Category(**payload.model_dump())
    try:
        await cat.insert()
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Category name already exists")
    return to_out(cat)

@router.get("/", response_model=List[CategoryOut])
async def list_categories() -> List[CategoryOut]:
    cats = await Category.find_all().to_list()
    return [to_out(c) for c in cats]

@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: PydanticObjectId) -> CategoryOut:
    cat = await Category.get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return to_out(cat)

@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: PydanticObjectId, data: CategoryUpdate) -> CategoryOut:
    cat = await Category.get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        await cat.set(data.model_dump(exclude_unset=True))
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Category name already exists")

    return to_out(cat)

@router.delete("/{category_id}")
async def delete_category(category_id: PydanticObjectId) -> dict:
    cat = await Category.get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    await cat.delete()
    return {"message": "Category deleted"}
