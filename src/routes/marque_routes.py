from fastapi import APIRouter
from models.marque import Marque, MarqueCreate

router = APIRouter(prefix="/marques", tags=["Marques"])

@router.post("/")
async def create_marque(marque: MarqueCreate):
    marque_db = Marque(**marque.model_dump())  # Convertit le schéma en Document Beanie
    await marque_db.insert()
    return marque_db

@router.get("/")
async def list_marques():
    return await Marque.find_all().to_list()

@router.get("/{id}")
async def get_marque(id: str):
    return await Marque.get(id)
