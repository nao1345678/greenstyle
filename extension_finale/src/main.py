"""
Application FastAPI principale pour l'API GreenStyle
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from models.brand import Brand
from models.user import User
from models.favorite import Favorite
from routes.brand_routes import router as brand_router
from routes.user_routes import router as user_router
from routes.favorite_routes import router as favorite_router
from routes.demo_routes import router as demo_router
from routes.auth_routes import router as auth_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application
    Initialise MongoDB et Beanie au démarrage
    """
    # Connexion MongoDB
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/greenstyle")
    db_name = os.getenv("MONGO_DB", "greenstyle_DB")
    
    print(f"🔌 Connexion à MongoDB: {mongo_url}")
    print(f"📦 Base de données: {db_name}")
    
    client = None
    db = None
    try:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=10000)
        await client.admin.command('ping')
        print("✅ MongoDB connecté")
        
        # Initialiser Beanie
        db = client.get_database(db_name)
        await init_beanie(database=db, document_models=[Brand, User, Favorite])
        print("✅ Beanie initialisé")
    except Exception as e:
        print(f"⚠️  Erreur de connexion MongoDB: {e}")
        print("⚠️  L'application démarre mais MongoDB n'est pas disponible")
        print("⚠️  Certaines fonctionnalités peuvent ne pas fonctionner")
        # Ne pas lever d'exception, permettre à l'app de démarrer
        client = None
        db = None
    
    yield
    
    # Nettoyage à l'arrêt
    if client:
        client.close()
        print("🔌 Connexion MongoDB fermée")


# Créer l'application FastAPI
app = FastAPI(
    title="GreenStyle API",
    description="API pour la détection de durabilité des marques de mode",
    version="2.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routes
app.include_router(brand_router)
app.include_router(user_router)
app.include_router(favorite_router)
app.include_router(auth_router)
app.include_router(demo_router)  # Routes de démonstration


@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "GreenStyle API",
        "version": "2.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Endpoint de santé"""
    return {"status": "healthy"}

