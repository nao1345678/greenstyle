from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import models
from config import MONGO_URL
from routes.brand_routes import router as brand_router
from routes.user_routes import router as user_router

app = FastAPI(
    title="GreenStyle API",
    description="API pour les données de durabilité des marques de mode",
    version="2.0.0"
)

# Configuration CORS pour permettre les requêtes depuis l'extension Chrome
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En développement - restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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