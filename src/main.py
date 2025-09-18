from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import models
from config import MONGO_URL
from routes.brand_routes import router as brand_router
from routes.user_routes import router as user_router
from routes.favorite_routes import router as favorite_router
from routes.category_routes import router as category_router
from routes.alternative_routes import router as alternative_router
from routes.site_routes import router as site_router
from routes.admin_routes import router as admin_router

app = FastAPI()

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=models.__all__,
    )

app.include_router(brand_router)
app.include_router(user_router)
app.include_router(favorite_router)
app.include_router(category_router)
app.include_router(alternative_router)
app.include_router(site_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB is running"}
