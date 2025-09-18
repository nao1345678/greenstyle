from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import models  # ton dossier models

from config import MONGO_URL

app = FastAPI()

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=models.__all__
    )
    