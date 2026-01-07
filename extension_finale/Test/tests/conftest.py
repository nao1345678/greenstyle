"""
Configuration pytest pour les tests
"""
import pytest
import sys
import os
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Ajouter le répertoire src au path (depuis Test/tests vers extension_finale/src)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from src.main import app
    from src.models.brand import Brand
except ImportError:
    # Fallback si l'import direct ne fonctionne pas
    from main import app
    from models.brand import Brand


@pytest.fixture(scope="function")
async def test_db():
    """Base de données de test MongoDB"""
    # Utiliser une base de données de test
    mongo_url = os.getenv("MONGO_TEST_URL", "mongodb://localhost:27017")
    db_name = "greenstyle_test"
    
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
    try:
        await client.admin.command('ping')
        db = client.get_database(db_name)
        await init_beanie(database=db, document_models=[Brand])
        yield db
        # Nettoyage après les tests
        try:
            await db.drop_collection("brands")
        except:
            pass
        client.close()
    except Exception:
        # Si MongoDB n'est pas disponible, on continue sans base de données
        yield None
        if client:
            client.close()


@pytest.fixture
async def client(test_db) -> AsyncGenerator[AsyncClient, None]:
    """Client HTTP pour les tests d'API"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_brand_data():
    """Données de test pour une marque"""
    return {
        "brand_name": "test_brand",
        "sustainable_materials": 75.0,
        "certifications": "B-Corp, Fair Trade",
        "country_origin": "France",
        "country_production": "France",
        "unsold_management": "Recyclage, Réparation",
        "supply_chain_transparency": "Élevée",
        "labor_ethics": 85.0,
        "description": "Marque de test durable"
    }


@pytest.fixture
def sample_brand_data_veja():
    """Données de test pour Veja (marque engagée)"""
    return {
        "brand_name": "veja",
        "sustainable_materials": 85.0,
        "certifications": "Fair Trade, Organic Cotton, B-Corp",
        "country_origin": "France",
        "country_production": "Brazil",
        "unsold_management": "Recyclage, Réparation",
        "supply_chain_transparency": "Totale",
        "labor_ethics": 85.0,
        "description": "Marque française de baskets éthiques"
    }

