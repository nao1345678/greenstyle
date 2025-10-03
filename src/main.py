from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import models
from config import MONGO_URL
from routes.brand_routes import router as brand_router
from routes.user_routes import router as user_router

app = FastAPI()

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=models.__all__,
    )

# brancher les routes ici
app.include_router(brand_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB is running 🚀"}