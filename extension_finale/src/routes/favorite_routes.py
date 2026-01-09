from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId, Link
from models.favorite import Favorite, FavoriteCreate
from models.user import User
from models.brand import Brand

router = APIRouter(prefix="/favorites", tags=["Favorites"])


async def to_out(fav: Favorite) -> dict:
    """Convertit un Favorite en dictionnaire pour la réponse"""
    # Charger les relations si nécessaire
    await fav.fetch_all_links()
    
    return {
        "id": str(fav.id),
        "user_id": str(fav.user.id) if fav.user else None,
        "brand_id": str(fav.brand.id) if fav.brand else None,
        "brand_name": fav.brand.brand_name if fav.brand else None,
        "name": fav.brand.brand_name if fav.brand else None,
        "cover_url": fav.brand.logo if fav.brand else None,
    }


@router.post("/", response_model=dict)
async def create_favorite(payload: FavoriteCreate) -> dict:
    """Ajoute une marque aux favoris d'un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = await User.get(PydanticObjectId(payload.user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Vérifier que la marque existe
    brand = await Brand.get(PydanticObjectId(payload.brand_id))
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Vérifier si le favori existe déjà
    existing = await Favorite.find_one(
        Favorite.user.id == PydanticObjectId(payload.user_id),
        Favorite.brand.id == PydanticObjectId(payload.brand_id)
    )
    
    if existing:
        raise HTTPException(status_code=400, detail="Favorite already exists")
    
    # Créer le favori
    favorite = Favorite(user=Link(user), brand=Link(brand))
    await favorite.insert()
    
    return await to_out(favorite)


@router.get("/", response_model=List[dict])
async def list_favorites(user_id: Optional[str] = Query(None)) -> List[dict]:
    """Liste les favoris, optionnellement filtrés par user_id"""
    if user_id:
        try:
            user_obj_id = PydanticObjectId(user_id)
            favorites = await Favorite.find(
                Favorite.user.id == user_obj_id
            ).to_list()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user_id")
    else:
        favorites = await Favorite.find_all().to_list()
    
    return [await to_out(fav) for fav in favorites]


@router.get("/{favorite_id}", response_model=dict)
async def get_favorite(favorite_id: PydanticObjectId) -> dict:
    """Récupère un favori par son ID"""
    favorite = await Favorite.get(favorite_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    return await to_out(favorite)


@router.delete("/{favorite_id}")
async def delete_favorite(favorite_id: PydanticObjectId) -> dict:
    """Supprime un favori"""
    favorite = await Favorite.get(favorite_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    await favorite.delete()
    return {"message": "Favorite deleted"}

