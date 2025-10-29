from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId

from models.favorite import Favorite, FavoriteCreate, FavoriteUpdate, FavoriteOut
from models.user import User
from models.brand import Brand

router = APIRouter(prefix="/favorites", tags=["Favorites"])

async def to_out(f: Favorite) -> FavoriteOut:
    user = await f.user.fetch() if hasattr(f.user, "fetch") else f.user
    brand = await f.brand.fetch() if hasattr(f.brand, "fetch") else f.brand
    return FavoriteOut(
        id=str(f.id),
        user_id=str(user.id),
        brand_id=str(brand.id),
        name=f.name,
        cover_url=f.cover_url,
        content=f.content,
        brand_name=getattr(brand, "brand_name", None),
    )

@router.post("/", response_model=FavoriteOut)
async def create_favorite(payload: FavoriteCreate) -> FavoriteOut:
    user = await User.get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    brand = await Brand.get(payload.brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    fav = Favorite(user=user, brand=brand,
                   name=payload.name, cover_url=payload.cover_url, content=payload.content)
    await fav.insert()
    return await to_out(fav)

@router.get("/", response_model=List[FavoriteOut])
async def list_favorites(
    user_id: Optional[str] = Query(default=None),
    brand_id: Optional[str] = Query(default=None),
) -> List[FavoriteOut]:
    query = {}
    if user_id:
        u = await User.get(user_id)
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        query["user.$id"] = u.id
    if brand_id:
        b = await Brand.get(brand_id)
        if not b:
            raise HTTPException(status_code=404, detail="Brand not found")
        query["brand.$id"] = b.id

    favs = await Favorite.find(query or {}).to_list()
    return [await to_out(f) for f in favs]

@router.get("/{fav_id}", response_model=FavoriteOut)
async def get_favorite(fav_id: PydanticObjectId) -> FavoriteOut:
    fav = await Favorite.get(fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return await to_out(fav)

@router.put("/{fav_id}", response_model=FavoriteOut)
async def update_favorite(fav_id: PydanticObjectId, data: FavoriteUpdate) -> FavoriteOut:
    fav = await Favorite.get(fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    updates = data.model_dump(exclude_unset=True)
    if updates:
        await fav.set(updates)
    return await to_out(fav)

@router.delete("/{fav_id}")
async def delete_favorite(fav_id: PydanticObjectId) -> dict:
    fav = await Favorite.get(fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    await fav.delete()
    return {"message": "Favorite deleted"}
