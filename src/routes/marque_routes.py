from fastapi import APIRouter
from models.marque import Marque

router = APIRouter(prefix="/marques", tags=["Marques"])

@router.post("/")
async def create_marque(marque: Marque):
    await marque.insert()
    return marque

@router.get("/")
async def list_marques():
    return await Marque.find_all().to_list()

@router.get("/{id}")
async def get_marque(id: str):
    return await Marque.get(id)
