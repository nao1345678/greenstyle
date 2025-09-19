from fastapi import APIRouter, HTTPException
from models.utilisateur import Utilisateur, UtilisateurCreate

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

@router.post("/")
async def create_utilisateur(user: UtilisateurCreate):
    user_db = Utilisateur(**user.model_dump())
    await user_db.insert()
    return user_db

@router.get("/")
async def list_utilisateurs():
    return await Utilisateur.find_all().to_list()

@router.get("/{id}")
async def get_utilisateur(id: str):
    return await Utilisateur.get(id)

@router.put("/{id}", response_model=Utilisateur)
async def update_utilisateur(id: str, data: Utilisateur):
    utilisateur = await Utilisateur.get(id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur not found")
    await utilisateur.set(data.dict(exclude_unset=True))
    return utilisateur

@router.delete("/{id}")
async def delete_utilisateur(id: str):
    utilisateur = await Utilisateur.get(id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur not found")
    await utilisateur.delete()
    return {"message": "Utilisateur deleted"}
